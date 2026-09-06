import unittest
from collections import defaultdict
from contextlib import contextmanager
import csv
import json
import tempfile
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from landuse import audit_queue, built_fraction, land_use, policies, sha256, stratum


@contextmanager
def raster(value):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "test.tif"
        with rasterio.open(path, "w", driver="GTiff", width=40, height=40,
                           count=1, dtype="uint16", nodata=65535,
                           crs="ESRI:54009", transform=from_origin(-2000, 2000, 100, 100)) as dst:
            dst.write(np.full((40, 40), value, dtype="uint16"), 1)
        with rasterio.open(path) as src:
            yield src


class LandUseTests(unittest.TestCase):
    def test_raster_units_and_missing_coverage(self):
        for value, expected in ((0, 0), (2500, 0.25), (10000, 1), (65535, None)):
            with self.subTest(value=value), raster(value) as src:
                for radius in (100, 500):
                    self.assertEqual(built_fraction(src, 0, 0, radius), expected)
                self.assertIsNone(built_fraction(src, 10, 10, 500))
                self.assertIsNone(built_fraction(src, 0, 180, 500))
                self.assertIsNone(built_fraction(src, 0, 0.02, 500))

    def test_invalid_raster_values(self):
        with raster(15000) as src, self.assertRaises(ValueError):
            built_fraction(src, 0, 0, 100)

    def test_thresholds_and_no_greenery_requirement(self):
        for near, far, expected in ((0, 0, "rural"), (0.049, 0, "rural"),
                                    (0.05, 0, "mixed"), (0, 0.2, "urban"),
                                    (0.2, 0, "urban"), (None, 0, "unknown"),
                                    (1, None, "unknown")):
            self.assertEqual(land_use(near, far), expected)

    def test_policy_support_weights_and_determinism(self):
        sites = [{"id": str(i), "country": "A", "koppen_code": "Af", "land_use": use}
                 for i, use in enumerate(["rural"] * 20 + ["mixed"] * 10 + ["urban"] * 20)]
        sites += [{"id": "rare", "country": "B", "koppen_code": "EF", "land_use": "urban"},
                  {"id": "unknown", "country": "C", "koppen_code": "ET", "land_use": "unknown"}]
        policies(sites)
        selected = [s for s in sites if s["game_selected"]]
        self.assertEqual(len(selected), 31)  # 20 rural, 5 mixed, 4 urban, two rare strata
        self.assertEqual({stratum(s) for s in sites}, {stratum(s) for s in selected})
        groups = defaultdict(list)
        for site in sites:
            self.assertEqual(site["evaluation_weight"], 1)
            groups[stratum(site)].append(site["train_sampling_weight"])
        for weights in groups.values():
            self.assertAlmostEqual(sum(weights), len(weights))
        self.assertAlmostEqual(sites[30]["train_sampling_weight"] / sites[0]["train_sampling_weight"], 0.25)
        reversed_sites = [dict(s) for s in reversed(sites)]
        policies(reversed_sites)
        self.assertEqual(sites, list(reversed(reversed_sites)))

    def test_audit_queue_is_unique_stratified_and_bounded(self):
        sites = [{"id": str(i), "country": "A", "koppen_code": "Af",
                  "land_use": "rural" if i < 20 else "urban"} for i in range(30)]
        queue = audit_queue(sites, size=2)
        self.assertEqual({s["land_use"] for s in queue}, {"rural", "urban"})
        self.assertEqual(queue, audit_queue(list(reversed(sites)), size=2))
        self.assertEqual(len(audit_queue(sites)), 30)
        self.assertEqual(audit_queue(sites, size=0), [])

    def test_checked_in_pilot_matches_source_and_both_consumers(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "sampling/pilot/manifest.json").read_text())
        selection = json.loads((root / "game/game-selection.json").read_text())
        rows = json.loads((root / "game/locations.json").read_text())
        self.assertEqual(manifest["source_sha256"], sha256(root / "game/locations.json"))
        self.assertEqual(selection["source_sha256"], manifest["source_sha256"])
        sites = manifest["sites"]
        self.assertEqual({s["id"] for s in sites}, {r["id"] for r in rows})
        original = [dict(s) for s in sites]
        policies(sites)
        self.assertEqual(sites, original)
        self.assertEqual(selection["selected_ids"], [s["id"] for s in sites if s["game_selected"]])
        self.assertEqual({stratum(s) for s in sites},
                         {stratum(s) for s in sites if s["game_selected"]})
        for site, row in zip(sites, rows):
            self.assertEqual((site["lat"], site["lng"]), (row["lat"], row["lng"]))
            self.assertEqual(site["land_use"], land_use(site["built_fraction_100m"], site["built_fraction_500m"]))
        with (root / "sampling/pilot/audit.csv").open() as stream:
            queue = list(csv.DictReader(stream))
        self.assertEqual([s["id"] for s in queue], [s["id"] for s in audit_queue(sites)])


if __name__ == "__main__":
    unittest.main()
