import json
import unittest

from app import summarize


def jsonl(*rows):
    return "\n".join(json.dumps(row) for row in rows)


class SummarizeTests(unittest.TestCase):
    def test_empty_and_blank_lines(self):
        for text in ("", "\n \t\r\n", "\u2003\n"):
            with self.subTest(text=text):
                self.assertEqual(summarize(text), {})
        row = {"id": "a", "category": "food", "amount": 2}
        self.assertEqual(summarize("\n \t\n" + jsonl(row) + "\n\n"), {"food": 2})

    def test_totals_zero_large_amounts_and_extra_fields(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "food", "amount": 3, "extra": [1]},
            {"id": "b", "category": "food", "amount": 10**100},
            {"id": "c", "category": "other", "amount": 0},
        )), {"food": 10**100 + 3, "other": 0})

    def test_first_id_wins_across_categories(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "food", "amount": 2},
            {"id": "a", "category": "food", "amount": 10},
            {"id": "a", "category": "other", "amount": 20},
            {"id": "b", "category": "other", "amount": 3},
        )), {"food": 2, "other": 3})

    def test_preserves_id_and_category_strings(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": " food ", "amount": 2},
            {"id": " a ", "category": "food", "amount": 3},
            {"id": " a ", "category": "ignored", "amount": 9},
            {"id": "\tb", "category": "\tfood", "amount": 4},
        )), {" food ": 2, "food": 3, "\tfood": 4})

    def test_invalid_json(self):
        for text in (
            "{", "not json", '{"id": "a",}', '{} {}',
            '{"id":"a","category":"food","amount":1,"extra":NaN}',
            '{"id":"a","category":"food","amount":1,"extra":Infinity}',
            '{"id":"a","category":"food","amount":1,"extra":-Infinity}',
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                summarize(text)

    def test_unicode_strings_are_preserved(self):
        row = {"id": "a\u2028b", "category": "food\u0085drink", "amount": 1}
        self.assertEqual(summarize(json.dumps(row, ensure_ascii=False)),
                         {"food\u0085drink": 1})

    def test_rows_must_be_objects(self):
        for row in (None, True, 3, 1.5, "text", [], [1]):
            with self.subTest(row=row), self.assertRaises(ValueError):
                summarize(jsonl(row))

    def test_missing_fields(self):
        valid = {"id": "a", "category": "food", "amount": 1}
        for field in valid:
            row = {key: value for key, value in valid.items() if key != field}
            with self.subTest(field=field), self.assertRaises(ValueError):
                summarize(jsonl(row))

    def test_invalid_strings(self):
        for field in ("id", "category"):
            for value in (None, True, 1, 1.5, [], {}, "", " \t\n", "\u2003"):
                row = {"id": "a", "category": "food", "amount": 1}
                row[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    summarize(jsonl(row))

    def test_invalid_amounts(self):
        for value in (None, True, False, -1, 1.0, 0.0, "2", [], {}):
            row = {"id": "a", "category": "food", "amount": value}
            with self.subTest(value=value), self.assertRaises(ValueError):
                summarize(jsonl(row))

    def test_invalid_duplicate_rows_are_validated(self):
        first = {"id": "a", "category": "food", "amount": 1}
        invalid = [
            {"id": "a", "amount": 2},
            {"id": "a", "category": "other"},
            {"id": "a", "category": " ", "amount": 2},
            {"id": "a", "category": [], "amount": 2},
            {"id": "a", "category": "other", "amount": -1},
            {"id": "a", "category": "other", "amount": True},
        ]
        for row in invalid:
            with self.subTest(row=row), self.assertRaises(ValueError):
                summarize(jsonl(first, row))


if __name__ == "__main__":
    unittest.main()
