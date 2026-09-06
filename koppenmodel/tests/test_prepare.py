import unittest

from prepare import audit, game_code, planned_views, selectable_codes


def site(code="Af", **changes):
    return {"id": "a", "koppen_code": code, "lat": 0, "lng": 0,
            "pano_id": "p", **changes}


class PrepareTests(unittest.TestCase):
    def test_game_taxonomy(self):
        self.assertEqual(game_code("As"), "Aw/As")
        self.assertEqual(game_code("Aw"), "Aw/As")
        script = "const KOPPEN_CLASSES = [{ code: 'Af'}, {code: 'Aw/As'}];"
        self.assertEqual(selectable_codes(script), ["Af", "Aw/As"])
        with self.assertRaises(ValueError):
            selectable_codes("const renamed = [];")

    def test_support_duplicates_and_conflicts(self):
        rows = [site(), site("Aw"), site("As", id="b", pano_id="q", lat=1)]
        result = audit(rows, ["Af", "Aw/As", "EF"])
        self.assertEqual(result["game_class_counts"], {"Af": 1, "Aw/As": 2, "EF": 0})
        self.assertEqual(result["absent_game_classes"], ["EF"])
        self.assertEqual(result["duplicates"]["coordinates"]["excess_rows"], 1)
        self.assertEqual(result["contradictory_pano_labels"], {"p": ["Af", "Aw/As"]})
        self.assertEqual(result["four_view_budget"]["images_before_deduplication"], 12)

    def test_aliases_are_not_conflicting_labels(self):
        result = audit([site("As"), site("Aw")], ["Aw/As"])
        self.assertEqual(result["contradictory_pano_labels"], {})
        self.assertEqual(result["classes_below_three_sites"], {"Aw/As": 1})

    def test_invalid_input(self):
        for rows in ([], [None], [site("XYZ")], [site(lat=91)],
                     [site(lng=float("nan"))], [site(lat=True)],
                     [site(id="")], [site(pano_id=4)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                audit(rows, ["Af"])

    def test_missing_pano_and_no_split_or_permission(self):
        rows = [site(pano_id=None)]
        self.assertEqual(audit(rows, ["Af"])["missing_pano_ids"], 1)
        views = list(planned_views(rows))
        self.assertEqual([v["heading"] for v in views], [0, 90, 180, 270])
        self.assertEqual(len({v["view_id"] for v in views}), 4)
        self.assertTrue(all(v["split"] is None and v["rights_ref"] is None for v in views))
        self.assertEqual(views, list(planned_views(rows)))


if __name__ == "__main__":
    unittest.main()
