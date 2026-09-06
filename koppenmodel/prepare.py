"""Offline seed audit and optional view plan. No network or ML dependencies."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re


def game_code(code):
    return "Aw/As" if code in ("Aw", "As") else code


def selectable_codes(script):
    match = re.search(r"const KOPPEN_CLASSES\s*=\s*\[(.*?)\];", script, re.S)
    if not match:
        raise ValueError("Cannot find KOPPEN_CLASSES; review changed game schema")
    codes = re.findall(r"\bcode:\s*'([^']+)'", match[1])
    if not codes or len(codes) != len(set(codes)):
        raise ValueError("Empty or duplicate selectable codes")
    return codes


def validate(rows, codes):
    if not isinstance(rows, list) or not rows:
        raise ValueError("Expected a nonempty locations array")
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Row {i}: expected object")
        for key in ("id", "koppen_code"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f"Row {i}: invalid {key}")
        if game_code(row["koppen_code"]) not in codes:
            raise ValueError(f"Row {i}: unsupported climate {row['koppen_code']}")
        for key, limit in (("lat", 90), ("lng", 180)):
            value = row.get(key)
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or not -limit <= value <= limit):
                raise ValueError(f"Row {i}: invalid {key}")
        pano = row.get("pano_id")
        if pano is not None and (not isinstance(pano, str) or not pano.strip()):
            raise ValueError(f"Row {i}: invalid pano_id")


def duplicate_counts(values):
    counts = Counter(values)
    return {"groups": sum(n > 1 for n in counts.values()),
            "excess_rows": sum(n - 1 for n in counts.values())}


def audit(rows, codes):
    validate(rows, codes)
    raw = Counter(row["koppen_code"] for row in rows)
    normalized = Counter(game_code(row["koppen_code"]) for row in rows)
    pano_labels = defaultdict(set)
    class_sites = defaultdict(set)
    for row in rows:
        class_sites[game_code(row["koppen_code"])].add((row["lat"], row["lng"]))
        if row.get("pano_id"):
            pano_labels[row["pano_id"]].add(game_code(row["koppen_code"]))
    return {
        "schema_version": 1,
        "status": "metadata_only_no_imagery_verified",
        "rows": len(rows),
        "selectable_codes": codes,
        "raw_class_counts": dict(sorted(raw.items())),
        "game_class_counts": {code: normalized[code] for code in codes},
        "absent_game_classes": [code for code in codes if not normalized[code]],
        "classes_below_three_sites": {
            code: len(class_sites[code]) for code in codes
            if 0 < len(class_sites[code]) < 3
        },
        "missing_pano_ids": sum(not row.get("pano_id") for row in rows),
        "duplicates": {
            "id": duplicate_counts(row["id"] for row in rows),
            "pano_id": duplicate_counts(row["pano_id"] for row in rows
                                        if row.get("pano_id")),
            "coordinates": duplicate_counts((row["lat"], row["lng"]) for row in rows),
        },
        "contradictory_pano_labels": {
            pano: sorted(labels) for pano, labels in sorted(pano_labels.items())
            if len(labels) > 1
        },
        "four_view_budget": {
            "images_before_deduplication": len(rows) * 4,
            "estimated_bytes_at_200kb": len(rows) * 4 * 200_000,
            "estimated_bytes_at_500kb": len(rows) * 4 * 500_000,
        },
        "limitations": [
            "Exact identity audit only; no near-duplicate or geographic split check.",
            "Coordinates, labels, panorama availability and imagery rights unverified.",
            "No imagery acquired; no train/validation/test assignment made.",
        ],
    }


def load_land_use(path, source_bytes):
    manifest = json.loads(path.read_text())
    if (manifest.get("schema_version") != 1
            or manifest.get("source_sha256") != hashlib.sha256(source_bytes).hexdigest()):
        raise ValueError("Unsupported or stale land-use manifest; regenerate annotations")
    sites = manifest["sites"]
    index = {site["id"]: site for site in sites}
    expected = {row["id"] for row in json.loads(source_bytes)}
    if len(index) != len(sites) or set(index) != expected:
        raise ValueError("Land-use manifest must cover every source site exactly once")
    for site in sites:
        weight = site["train_sampling_weight"]
        if (isinstance(weight, bool) or not isinstance(weight, (int, float))
                or not math.isfinite(weight) or weight <= 0
                or site["land_use"] not in ("rural", "mixed", "urban", "unknown")):
            raise ValueError("Invalid land-use annotation or training weight")
    return index


def planned_views(rows, land_use=None):
    for index, row in enumerate(rows):
        annotation = land_use[row["id"]] if land_use is not None else None
        for heading in (0, 90, 180, 270):
            yield {
                "view_id": f"seed_{index:06d}_{heading:03d}",
                "source_record_id": row["id"],
                "pano_id": row.get("pano_id"),
                "lat": row["lat"], "lng": row["lng"],
                "raw_code": row["koppen_code"],
                "game_code": game_code(row["koppen_code"]),
                "heading": heading, "pitch": 0, "fov": 90,
                "split": None, "rights_ref": None,
                "status": "blocked_pending_rights_and_label_review",
                "land_use": annotation["land_use"] if annotation else "unknown",
                "train_sampling_weight": annotation["train_sampling_weight"] if annotation else 1.0,
                "evaluation_weight": 1.0,
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--views-output", type=Path)
    parser.add_argument("--land-use", type=Path, help="Shared sampling manifest; weights are training-only")
    args = parser.parse_args()
    sources = [args.game / "locations.json", args.game / "app.js"]
    outputs = [p for p in (args.output, args.views_output) if p is not None]
    resolved = [p.resolve() for p in outputs]
    if len(set(resolved)) != len(resolved) or set(resolved) & {
            p.resolve() for p in sources}:
        parser.error("Outputs must be distinct and must not overwrite source files")
    # Refuse overwrites, including previously generated reports.
    if any(p.exists() for p in outputs):
        parser.error("Output already exists; choose a new path")
    try:
        locations_bytes, app_bytes = (p.read_bytes() for p in sources)
        rows = json.loads(locations_bytes)
        codes = selectable_codes(app_bytes.decode("utf-8"))
        report = audit(rows, codes)
        land_use = load_land_use(args.land_use, locations_bytes) if args.land_use else None
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    report["source_sha256"] = {
        "locations.json": hashlib.sha256(locations_bytes).hexdigest(),
        "app.js": hashlib.sha256(app_bytes).hexdigest(),
    }
    if land_use is not None:
        report["land_use_counts"] = dict(Counter(s["land_use"] for s in land_use.values()))
        report["source_sha256"]["land_use_manifest"] = hashlib.sha256(args.land_use.read_bytes()).hexdigest()
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")
    if args.views_output:
        with args.views_output.open("x") as stream:
            for view in planned_views(rows, land_use):
                stream.write(json.dumps(view) + "\n")
    print(f"Audited {len(rows)} sites; {len(codes)} selectable classes; "
          f"{len(report['absent_game_classes'])} absent. No imagery downloaded.")


if __name__ == "__main__":
    main()
