import unittest

from app import paginate


class PaginateTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(paginate(list(range(25))), {
            "items": list(range(20)), "total": 25,
            "page": 1, "page_size": 20, "pages": 2,
        })

    def test_page_boundaries(self):
        for page, expected in ((1, [0, 1]), (2, [2, 3]), (3, [4]), (4, [])):
            with self.subTest(page=page):
                self.assertEqual(paginate(list(range(5)), page, 2), {
                    "items": expected, "total": 5,
                    "page": page, "page_size": 2, "pages": 3,
                })

    def test_exact_multiple_and_single_item_pages(self):
        self.assertEqual(paginate([1, 2, 3, 4], 2, 2)["pages"], 2)
        self.assertEqual(paginate([1, 2, 3], 3, 1), {
            "items": [3], "total": 3, "page": 3, "page_size": 1, "pages": 3,
        })

    def test_empty(self):
        for page in (1, 5):
            with self.subTest(page=page):
                self.assertEqual(paginate([], page, 7), {
                    "items": [], "total": 0,
                    "page": page, "page_size": 7, "pages": 0,
                })

    def test_invalid_parameters_even_for_empty_input(self):
        invalid = (True, False, 0, -1, 1.0, 1.5, "1", None, [], {}, complex(1))
        for items in ([], [1, 2]):
            for name in ("page", "page_size"):
                for value in invalid:
                    with self.subTest(items=items, parameter=name, value=value):
                        with self.assertRaises(ValueError):
                            paginate(items, **{name: value})

    def test_preserves_order_and_original_list(self):
        items = ["z", None, "a", "z"]
        original = items.copy()
        result = paginate(items, 1, 10)
        self.assertEqual(result["items"], original)
        self.assertIsInstance(result["items"], list)
        self.assertIsNot(result["items"], items)
        result["items"].append("extra")
        self.assertEqual(items, original)

    def test_arbitrarily_large_positive_integers(self):
        huge = 10 ** 100
        self.assertEqual(paginate([1, 2], huge, 1)["items"], [])
        self.assertEqual(paginate([1, 2], 1, huge)["pages"], 1)


if __name__ == "__main__":
    unittest.main()
