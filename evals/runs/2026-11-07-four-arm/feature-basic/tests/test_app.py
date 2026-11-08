import unittest

from app import paginate


class PaginateTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(paginate(list(range(25))), {
            "items": list(range(20)), "total": 25,
            "page": 1, "page_size": 20, "pages": 2,
        })

    def test_page_boundaries(self):
        for total in (0, 1, 19, 20, 21, 40, 41):
            items = list(range(total))
            for page in (1, 2, 3, 4, 10**100):
                with self.subTest(total=total, page=page):
                    start = (page - 1) * 20
                    self.assertEqual(paginate(items, page), {
                        "items": items[start:start + 20], "total": total,
                        "page": page, "page_size": 20,
                        "pages": total // 20 + bool(total % 20),
                    })

    def test_custom_size_preserves_order_and_input(self):
        items = ["z", "a", "z", "b", "c"]
        original = items.copy()
        result = paginate(items, page=2, page_size=2)
        self.assertEqual(result, {
            "items": ["z", "b"], "total": 5,
            "page": 2, "page_size": 2, "pages": 3,
        })
        self.assertEqual(items, original)
        result["items"].append("new")
        self.assertEqual(items, original)

    def test_invalid_parameters_including_empty_input(self):
        for items in ([], [1, 2]):
            for name in ("page", "page_size"):
                for value in (True, False, 0, -1, 1.0, 1.5, "1", None, [], {}):
                    with self.subTest(items=items, name=name, value=value):
                        with self.assertRaises(ValueError):
                            paginate(items, **{name: value})

    def test_size_one_and_large_integers(self):
        self.assertEqual(paginate([3, 2, 1], 3, 1), {
            "items": [1], "total": 3, "page": 3,
            "page_size": 1, "pages": 3,
        })
        self.assertEqual(paginate([1], page_size=10**100)["pages"], 1)


if __name__ == "__main__":
    unittest.main()
