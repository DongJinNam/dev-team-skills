import unittest

from app import paginate


class PaginateTests(unittest.TestCase):
    def test_defaults(self):
        result = paginate(list(range(25)))
        self.assertEqual(result, {
            "items": list(range(20)), "total": 25,
            "page": 1, "page_size": 20, "pages": 2,
        })

    def test_page_boundaries(self):
        cases = [
            (["a", "b", "c", "d", "e"], 1, 2, ["a", "b"], 3),
            (["a", "b", "c", "d", "e"], 2, 2, ["c", "d"], 3),
            (["a", "b", "c", "d", "e"], 3, 2, ["e"], 3),
            (["a", "b", "c", "d", "e"], 4, 2, [], 3),
            ([1, 2, 3, 4], 2, 2, [3, 4], 2),
            ([1, 2], 2, 1, [2], 2),
            ([1, 2], 1, 10**100, [1, 2], 1),
            ([1, 2], 10**100, 2, [], 1),
            ([], 1, 20, [], 0),
            ([], 5, 3, [], 0),
        ]
        for items, page, size, expected_items, pages in cases:
            with self.subTest(items=items, page=page, size=size):
                self.assertEqual(paginate(items, page, size), {
                    "items": expected_items, "total": len(items),
                    "page": page, "page_size": size, "pages": pages,
                })

    def test_invalid_parameters_even_with_empty_input(self):
        invalid = [True, False, 0, -1, 1.0, 1.5, "1", None, [], {}, 1j]
        for items in ([], [1, 2]):
            for parameter in ("page", "page_size"):
                for value in invalid:
                    with self.subTest(items=items, parameter=parameter, value=value):
                        with self.assertRaises(ValueError):
                            paginate(items, **{parameter: value})

    def test_preserves_input_order_and_returns_new_list(self):
        items = ["c", "a", "b", "a"]
        result = paginate(items)
        self.assertEqual(items, ["c", "a", "b", "a"])
        self.assertEqual(result["items"], ["c", "a", "b", "a"])
        self.assertIsInstance(result["items"], list)
        self.assertIsNot(result["items"], items)
        result["items"].append("new")
        self.assertEqual(items, ["c", "a", "b", "a"])


if __name__ == "__main__":
    unittest.main()
