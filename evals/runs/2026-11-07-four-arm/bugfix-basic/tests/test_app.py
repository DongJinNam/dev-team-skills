import json
import unittest

from app import summarize


def jsonl(*rows):
    return "\n".join(json.dumps(row) for row in rows)


class SummarizeTests(unittest.TestCase):
    def test_empty_and_blank_lines(self):
        for text in ("", "\n", " \t\r\n\n  "):
            with self.subTest(text=text):
                self.assertEqual(summarize(text), {})
        text = '\n \t\n{"id":"a","category":"x","amount":2}\r\n  \n'
        self.assertEqual(summarize(text), {"x": 2})

    def test_totals_zero_and_extra_fields(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "x", "amount": 2, "extra": None},
            {"id": "b", "category": "x", "amount": 3},
            {"id": "c", "category": "y", "amount": 0},
        )), {"x": 5, "y": 0})

    def test_first_id_wins_across_categories(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "x", "amount": 0},
            {"id": "a", "category": "x", "amount": 5},
            {"id": "a", "category": "y", "amount": 9},
            {"id": "b", "category": "y", "amount": 2},
        )), {"x": 0, "y": 2})

    def test_strings_are_preserved(self):
        self.assertEqual(summarize(jsonl(
            {"id": "a", "category": "x", "amount": 1},
            {"id": " a ", "category": "x", "amount": 2},
            {"id": "b", "category": " x ", "amount": 4},
            {"id": "\tc\t", "category": "\ty\t", "amount": 8},
        )), {"x": 3, " x ": 4, "\ty\t": 8})

    def test_invalid_json_and_nonobjects(self):
        for text in ('{', '{"id":}', '{} {}', 'null', '[]', '1', 'true', '"row"'):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    summarize(text)

    def test_missing_fields(self):
        for field in ("id", "category", "amount"):
            row = {"id": "a", "category": "x", "amount": 1}
            del row[field]
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    summarize(jsonl(row))

    def test_invalid_values_including_duplicates(self):
        valid = {"id": "a", "category": "x", "amount": 1}
        invalid_values = {
            "id": [None, True, 1, [], {}, "", " \t\n", "\u2003"],
            "category": [None, False, 1, [], {}, "", " \t\n", "\u2003"],
            "amount": [None, True, False, -1, 1.0, "1", [], {}, float("inf"), float("nan")],
        }
        for field, values in invalid_values.items():
            for value in values:
                row = dict(valid, **{field: value})
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        summarize(jsonl(row))
                    with self.assertRaises(ValueError):
                        summarize(jsonl(valid, row))
        for field in ("category", "amount"):
            row = dict(valid)
            del row[field]
            with self.subTest(missing_duplicate_field=field):
                with self.assertRaises(ValueError):
                    summarize(jsonl(valid, row))


if __name__ == "__main__":
    unittest.main()
