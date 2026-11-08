import json
import unittest

from app import summarize


class SummarizeTests(unittest.TestCase):
    def test_empty_and_blank_lines(self):
        for text in ("", "\n \t\r\n", '\n{"id":"a","category":"x","amount":2}\n \t\n'):
            with self.subTest(text=text):
                self.assertEqual(summarize(text), {"x": 2} if "id" in text else {})

    def test_totals_zero_and_extra_fields(self):
        rows = [
            {"id": "a", "category": "x", "amount": 2, "extra": []},
            {"id": "b", "category": "x", "amount": 3},
            {"id": "c", "category": "y", "amount": 0},
        ]
        self.assertEqual(summarize("\n".join(map(json.dumps, rows))), {"x": 5, "y": 0})

    def test_first_id_wins_across_categories(self):
        rows = [
            {"id": "a", "category": "x", "amount": 0},
            {"id": "a", "category": "y", "amount": 8},
            {"id": "b", "category": "x", "amount": 3},
            {"id": "b", "category": "x", "amount": 9},
        ]
        self.assertEqual(summarize("\n".join(map(json.dumps, rows))), {"x": 3})

    def test_strings_preserved_exactly(self):
        rows = [
            {"id": "a", "category": "x", "amount": 1},
            {"id": " a ", "category": " x ", "amount": 2},
            {"id": "a ", "category": "x", "amount": 4},
            {"id": "b\u2028c", "category": "y\u2029z", "amount": 8},
        ]
        text = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
        self.assertEqual(summarize(text), {"x": 5, " x ": 2, "y\u2029z": 8})

    def test_non_objects_raise_value_error(self):
        for row in (None, [], [1], True, 2, "text"):
            with self.subTest(row=row), self.assertRaises(ValueError):
                summarize(json.dumps(row))

    def test_missing_fields_raise_value_error(self):
        valid = {"id": "a", "category": "x", "amount": 1}
        for field in valid:
            row = valid.copy()
            del row[field]
            for prefix in ("", json.dumps(valid) + "\n"):
                with self.subTest(field=field, duplicate=bool(prefix)), self.assertRaises(ValueError):
                    summarize(prefix + json.dumps(row))

    def test_invalid_values_including_duplicates_raise_value_error(self):
        valid = {"id": "a", "category": "x", "amount": 1}
        invalid = {
            "id": [None, False, 0, [], {}, "", " \t\n", "\u2003"],
            "category": [None, False, 0, [], {}, "", " \t\n", "\u2003"],
            "amount": [None, True, False, -1, 1.0, "1", [], {}],
        }
        for field, values in invalid.items():
            for value in values:
                row = dict(valid, **{field: value})
                for prefix in ("", json.dumps(valid) + "\n"):
                    with self.subTest(field=field, value=value, duplicate=bool(prefix)):
                        with self.assertRaises(ValueError):
                            summarize(prefix + json.dumps(row))

    def test_invalid_json_including_duplicates_raises_value_error(self):
        valid = '{"id":"a","category":"x","amount":1}'
        for row in ('{', valid + ' trailing', valid + ',',
                    '{"id":"a","category":"x","amount":1,"extra":NaN}',
                    '{"id":"a","category":"x","amount":1,"extra":Infinity}',
                    '{"id":"a","category":"x","amount":1,"extra":-Infinity}'):
            for prefix in ("", valid + "\n"):
                with self.subTest(row=row, duplicate=bool(prefix)), self.assertRaises(ValueError):
                    summarize(prefix + row)


if __name__ == "__main__":
    unittest.main()
