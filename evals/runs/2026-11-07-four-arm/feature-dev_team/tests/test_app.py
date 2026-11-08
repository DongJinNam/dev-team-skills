import unittest

from app import paginate


class PaginateTests(unittest.TestCase):
    def test_defaults_and_exact_keys(self):
        self.assertEqual(paginate(list(range(25))), {
            "items": list(range(20)), "total": 25, "page": 1,
            "page_size": 20, "pages": 2,
        })

    def test_page_boundaries(self):
        for page, expected in ((1, [0, 1]), (2, [2, 3]), (3, [4]), (4, [])):
            with self.subTest(page=page):
                self.assertEqual(paginate(list(range(5)), page, 2), {
                    "items": expected, "total": 5, "page": page,
                    "page_size": 2, "pages": 3,
                })

    def test_empty_input(self):
        for page in (1, 5):
            with self.subTest(page=page):
                self.assertEqual(paginate([], page, 3), {
                    "items": [], "total": 0, "page": page,
                    "page_size": 3, "pages": 0,
                })

    def test_exact_multiple_and_single_item_pages(self):
        self.assertEqual(paginate([1, 2, 3, 4], 2, 2)["pages"], 2)
        self.assertEqual(paginate([1, 2, 3, 4], 3, 2)["items"], [])
        self.assertEqual(paginate([1, 2], 2, 1)["items"], [2])
        self.assertEqual(paginate([1, 2], 2, 1)["pages"], 2)

    def test_invalid_arguments_even_for_empty_input(self):
        invalid_values = (True, False, 0, -1, 1.0, 1.5, "1", None, [], {}, 1j)
        for items in ([], [1, 2]):
            for name in ("page", "page_size"):
                for value in invalid_values:
                    with self.subTest(items=items, name=name, value=value):
                        with self.assertRaises(ValueError):
                            paginate(items, **{name: value})

    def test_order_and_input_preserved_with_separate_result_list(self):
        items = ["c", "a", "b"]
        result = paginate(items)
        self.assertEqual(result["items"], ["c", "a", "b"])
        self.assertIsInstance(result["items"], list)
        self.assertIsNot(result["items"], items)
        result["items"].append("d")
        self.assertEqual(items, ["c", "a", "b"])

    def test_arbitrarily_large_positive_integers(self):
        huge = 10 ** 100
        self.assertEqual(paginate([1], huge)["items"], [])
        self.assertEqual(paginate([1], page_size=huge)["pages"], 1)
        self.assertEqual(paginate([1], page_size=huge)["items"], [1])


if __name__ == "__main__":
    unittest.main()
