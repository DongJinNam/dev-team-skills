import json
import unittest

from app import summarize


def jsonl(*rows):
    return "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)


class SummarizeTests(unittest.TestCase):
    def test_empty_and_blank_lines(self):
        for text in ("", "\n", " \t\r\n\n\u2003"):
            with self.subTest(text=text):
                self.assertEqual(summarize(text), {})

    def test_totals_blank_lines_extra_fields_and_zero(self):
        text = jsonl(
            {"id": "a", "category": "food", "amount": 2, "extra": [1]},
            {"id": "b", "category": "food", "amount": 3},
            {"id": "c", "category": "other", "amount": 0},
        ).replace("\n", "\r\n \t\r\n")
        self.assertEqual(summarize("\n" + text + "\n"), {"food": 5, "other": 0})

    def test_first_id_wins_across_categories(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "first", "amount": 0},
            {"id": "a", "category": "second", "amount": 8},
            {"id": "a", "category": "first", "amount": 9},
            {"id": "b", "category": "first", "amount": 2},
        )), {"first": 2})

    def test_preserves_strings_exactly(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": " food ", "amount": 1},
            {"id": " a ", "category": "food", "amount": 2},
            {"id": "a\u2028b", "category": "x\u0085y", "amount": 3},
        )), {" food ": 1, "food": 2, "x\u0085y": 3})

    def test_missing_fields(self):
        for field in ("id", "category", "amount"):
            row = {"id": "a", "category": "food", "amount": 1}
            del row[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                summarize(jsonl(row))

    def test_invalid_strings(self):
        for field in ("id", "category"):
            for value in (None, True, 1, 1.5, [], {}, "", " \t\r\n", "\u2003"):
                row = {"id": "a", "category": "food", "amount": 1}
                row[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    summarize(jsonl(row))

    def test_invalid_amounts(self):
        for amount in (None, True, False, -1, 1.0, 1.5, "1", [], {}):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                summarize(jsonl({"id": "a", "category": "food", "amount": amount}))

    def test_non_objects(self):
        for row in (None, True, 1, 1.5, "text", [], [1]):
            with self.subTest(row=row), self.assertRaises(ValueError):
                summarize(jsonl(row))

    def test_invalid_json(self):
        for text in ("{", "not json", '{} {}', '{"id":"a",}',
                     '{"id":"a","category":"food","amount":1,"extra":NaN}',
                     '{"id":"a","category":"food","amount":Infinity}',
                     '{"id":"a","category":"food","amount":-Infinity}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                summarize(text)

    def test_invalid_duplicates_raise(self):
        first = {"id": "a", "category": "food", "amount": 1}
        invalid_rows = [
            {"id": "a", "category": "food", "amount": value}
            for value in (True, False, -1, 1.0, None, "2", [], {})
        ] + [
            {"id": "a", "category": value, "amount": 2}
            for value in (None, "", " \t", 1, [], {})
        ] + [{"id": "a", "amount": 2}, {"id": "a", "category": "food"}]
        for row in invalid_rows:
            with self.subTest(row=row), self.assertRaises(ValueError):
                summarize(jsonl(first, row))

    def test_large_integer(self):
        amount = 10 ** 100
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "food", "amount": amount},
            {"id": "b", "category": "food", "amount": amount},
        )), {"food": 2 * amount})


if __name__ == "__main__":
    unittest.main()
