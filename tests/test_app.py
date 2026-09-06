"""Тесты обработки данных и интерфейса."""

from io import BytesIO
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from app import daily_summary, read_diary


TEST_CSV = """Дата,Головная боль,Интенсивность боли,Комментарии
2026-08-01,Нет,,
2026-08-02,Да,6,
2026-08-03,Да,4,
2026-08-05,Нет,,
2026-08-06,Да,,Автоматическая запись
2026-08-07,Нет,,
2026-08-09,Да,7,
2026-08-10,Нет,,
""".encode("utf-8")


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def pass_welcome(app, name="Анна"):
    app.text_input[0].input(name)
    app.button[0].click()
    return app.run(timeout=15)


class DiaryTests(unittest.TestCase):
    def test_days_are_not_rows_and_missing_is_not_no_pain(self):
        source = (
            "Дата,Головная боль\n"
            "2026-08-01,Нет\n2026-08-01,Да\n"
            "2026-08-03,Нет\n2026-08-04,\n"
        ).encode("utf-8")
        frame, _ = read_diary(source)
        days = daily_summary(frame, "2026-08-01", "2026-08-04")
        self.assertEqual(days["Состояние"].tolist(), ["Была боль", "Нет данных", "Без боли", "Нет данных"])

    def test_automatic_records_leave_unknown_days(self):
        frame, _ = read_diary(TEST_CSV)
        filtered = frame.loc[~frame["_automatic"]]
        days = daily_summary(filtered, "2026-08-01", "2026-08-10")
        self.assertEqual(days["Состояние"].value_counts().to_dict(), {"Без боли": 4, "Была боль": 3, "Нет данных": 3})
        empty = daily_summary(filtered.iloc[:0], "2026-08-06", "2026-08-06")
        self.assertEqual(empty["Состояние"].tolist(), ["Нет данных"])

    def test_encoding_and_intensity_validation(self):
        source = (
            "Дата;Головная боль;Интенсивность боли\n"
            "2026-08-01;Да;5,5\n2026-08-02;Да;\n"
            "2026-08-03;Да;11\n2026-08-04;Да;текст\n"
        ).encode("cp1251")
        frame, notices = read_diary(source)
        self.assertEqual(frame["_intensity"].dropna().tolist(), [5.5])
        self.assertIn("2", notices[0])

    def test_invalid_uploads_are_rejected(self):
        cases = [
            "", "Дата,Головная боль\n", "День,Головная боль\n2026-08-01,Да\n",
            "Дата,Головная боль\n2026-02-30,Да\n",
            "Дата,Головная боль\n2026-08-01,Может быть\n",
            "Дата,Головная боль\n2026-08-01,Да,лишнее\n",
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                read_diary(source.encode("utf-8"))

    def test_upload_dashboard_filters_and_empty_period(self):
        with patch("streamlit.file_uploader", return_value=BytesIO(TEST_CSV)):
            app = AppTest.from_file(str(APP_PATH)).run(timeout=15)
            self.assertFalse(app.exception)
            self.assertEqual(len(app.file_uploader), 0)
            app = pass_welcome(app)
            self.assertFalse(app.exception)
            self.assertEqual([metric.value for metric in app.metric[:4]], ["3", "4", "3", "43%"])
            app.checkbox[1].check().run()
            self.assertFalse(app.exception)
            self.assertEqual([metric.value for metric in app.metric[:4]], ["4", "4", "2", "50%"])
            from datetime import date
            app.date_input[0].set_value((date(2026, 8, 4), date(2026, 8, 4))).run()
            self.assertFalse(app.exception)
            self.assertEqual([metric.value for metric in app.metric[:4]], ["0", "0", "1", "—"])

    def test_empty_page_demo_and_invalid_file(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=15)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric), 0)
        self.assertEqual(len(app.text_input), 1)
        app = pass_welcome(app)
        app.checkbox[0].check().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].label, "Дни с болью")
        self.assertEqual(len(app.get("plotly_chart")), 2)
        with patch("streamlit.file_uploader", return_value=BytesIO(b"")):
            app = AppTest.from_file(str(APP_PATH)).run(timeout=15)
            app = pass_welcome(app)
            self.assertFalse(app.exception)
            self.assertEqual(len(app.error), 1)


if __name__ == "__main__":
    unittest.main()
