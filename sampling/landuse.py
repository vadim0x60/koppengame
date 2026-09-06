"""Annotate sites from GHSL; export game selection and a manual audit queue.

No imagery acquisition. Raster values must be built-up square metres in the
100 m Mollweide GHS-BUILT-S product, not categorical land cover or population.
"""

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import random

import numpy as np
from pyproj import Geod
import rasterio
from rasterio.features import geometry_mask, geometry_window
from rasterio.warp import transform
from rasterio.errors import WindowError

SOURCE_URL = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_BUILT_S_GLOBE_R2023A/GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100/"
    "V1-0/GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_V1_0.zip"
)
RASTER_SHA256 = "10178632291d09c905cd294ab0ed3e6f66df90b4cfe297a95dcee3a5b90a69f2"
GEOD = Geod(ellps="WGS84")
WEIGHTS = {"rural": 1.0, "mixed": 0.5, "urban": 0.25, "unknown": 1.0}


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def built_fraction(src, lat, lng, radius):
    """Mean of cells touching a geodesic circle; missing cells remain unknown.

    This is a raster-resolution approximation, not a subpixel building mask.
    Require >=90% valid coverage; never turn nodata into rural evidence.
    """
    bearings = list(range(0, 360, 5))
    lons, lats, _ = GEOD.fwd([lng] * len(bearings), [lat] * len(bearings),
                            bearings, [radius] * len(bearings))
    # A dateline-crossing window would span the world in this projection.
    if max(lons) - min(lons) > 180:
        return None
    xs, ys = transform("EPSG:4326", src.crs, lons, lats)
    ring = list(zip(xs, ys))
    polygon = {"type": "Polygon", "coordinates": [ring + [ring[0]]]}
    try:
        window = geometry_window(src, [polygon], boundless=True)
        values = src.read(1, window=window, masked=True, boundless=True)
    except WindowError:
        return None
    inside = geometry_mask([polygon], values.shape, src.window_transform(window),
                           all_touched=True, invert=True)
    valid = inside & ~np.ma.getmaskarray(values)
    if not inside.any() or valid.sum() / inside.sum() < 0.9:
        return None
    samples = values.data[valid]
    if np.any((samples < 0) | (samples > 10000)):
        raise ValueError("Not a 100 m GHSL built-surface raster: values outside 0–10000")
    return round(float(samples.mean() / 10000), 6)


def land_use(near, far):
    if near is None or far is None:
        return "unknown"
    # Pilot thresholds, not official GHSL settlement classes.
    if near >= 0.2 or far >= 0.2:
        return "urban"
    if near >= 0.05 or far >= 0.05:
        return "mixed"
    return "rural"


def stratum(site):
    # Country is an explicit first-pass region proxy; not a geographic split.
    return site["koppen_code"], site.get("country") or "Unknown"


def policies(sites, seed=42):
    """Preserve climate×country support; normalize training weights per stratum.

    Game retains rural/unknown sites, half of mixed sites, and a small urban
    quota. All-urban strata retain one site rather than disappearing silently.
    """
    groups = defaultdict(list)
    for site in sites:
        groups[stratum(site)].append(site)
    rng = random.Random(seed)
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda s: s["id"])
        urban = [s for s in group if s["land_use"] == "urban"]
        mixed = [s for s in group if s["land_use"] == "mixed"]
        keep = [s for s in group if s["land_use"] in ("rural", "unknown")]
        rng.shuffle(mixed)
        keep += mixed[:math.ceil(len(mixed) * 0.5)]
        rng.shuffle(urban)
        quota = max(1, math.floor(len(keep) * 0.15 / 0.85)) if urban else 0
        keep += urban[:quota]
        ids = {s["id"] for s in keep}
        mean_weight = sum(WEIGHTS[s["land_use"]] for s in group) / len(group)
        for site in group:
            site["game_selected"] = site["id"] in ids
            site["train_sampling_weight"] = WEIGHTS[site["land_use"]] / mean_weight
            site["evaluation_weight"] = 1.0


def audit_queue(sites, size=300, seed=42):
    """Round-robin climate×country×land-use buckets, not a prevalence sample."""
    groups = defaultdict(list)
    for site in sorted(sites, key=lambda s: s["id"]):
        groups[(*stratum(site), site["land_use"])].append(site)
    rng = random.Random(seed)
    buckets = [groups[key] for key in sorted(groups)]
    for bucket in buckets:
        rng.shuffle(bucket)
    rng.shuffle(buckets)
    result = []
    while buckets and len(result) < size:
        for bucket in buckets:
            result.append(bucket.pop())
            if len(result) == size:
                break
        buckets = [bucket for bucket in buckets if bucket]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locations", type=Path, required=True)
    parser.add_argument("--raster", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True,
                        help="New directory for manifest.json, game-selection.json and audit.csv")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output directory exists; choose a new path")
    raster_digest = sha256(args.raster)
    if raster_digest != RASTER_SHA256:
        parser.error("Raster checksum mismatch: use the pinned 2020 R2023A 100 m product")
    rows = json.loads(args.locations.read_text())
    if not rows or len({r["id"] for r in rows}) != len(rows):
        parser.error("Locations must be nonempty with unique IDs")
    sites = []
    with rasterio.open(args.raster) as src:
        if (src.crs != rasterio.crs.CRS.from_string("ESRI:54009")
                or src.res != (100, 100) or src.count != 1):
            parser.error("Expected single-band GHSL 100 m Mollweide raster")
        for row in rows:
            lat, lng = row["lat"], row["lng"]
            if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                parser.error(f"Invalid coordinates for {row['id']}")
            near = built_fraction(src, lat, lng, 100)
            far = built_fraction(src, lat, lng, 500)
            sites.append({
                "id": row["id"], "lat": lat, "lng": lng,
                "pano_id": row.get("pano_id"),
                "koppen_code": row["koppen_code"], "country": row.get("country"),
                "coordinate_status": "source_coordinate_unverified",
                "built_fraction_100m": near, "built_fraction_500m": far,
                "land_use": land_use(near, far),
            })
    policies(sites)
    counts = Counter(s["land_use"] for s in sites)
    retained = Counter(s["land_use"] for s in sites if s["game_selected"])
    strata = defaultdict(lambda: {"total": 0, "selected": 0})
    for site in sites:
        key = " / ".join(stratum(site))
        strata[key]["total"] += 1
        strata[key]["selected"] += int(site["game_selected"])
    digest = sha256(args.locations)
    manifest = {
        "schema_version": 1, "policy_version": "ghsl-pilot-v1", "seed": 42,
        "source_sha256": digest,
        "raster": {"file": args.raster.name, "sha256": raster_digest,
                   "url": SOURCE_URL, "epoch": 2020,
                   "credit": "European Commission, Joint Research Centre (JRC), "
                             "Pesaresi & Politis (2023), GHS-BUILT-S R2023A",
                   "doi": "10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA"},
        "summary": {"before": dict(counts), "game_after": dict(retained),
                    "climate_country_retention": dict(sorted(strata.items()))},
        "sites": sites,
    }
    args.output.mkdir(parents=True)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.output / "game-selection.json").write_text(json.dumps({
        "policy_version": manifest["policy_version"], "source_sha256": digest,
        "selected_ids": [s["id"] for s in sites if s["game_selected"]],
    }, indent=2) + "\n")
    fields = ["id", "lat", "lng", "pano_id", "koppen_code", "country", "land_use",
              "built_fraction_100m", "built_fraction_500m", "game_selected",
              "environment_visibility", "cultural_dominance", "irrigated_or_ornamental",
              "headings_reviewed", "reviewer", "notes"]
    with (args.output / "audit.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(audit_queue(sites))
    print(json.dumps(manifest["summary"], indent=2))


if __name__ == "__main__":
    main()
