"""Аналитика дневника головной боли."""

import csv
from hashlib import sha256
from io import StringIO

import pandas as pd
import plotly.express as px
import streamlit as st

from welcome import show_main_header, show_steps, show_welcome_gate

# Локализация дат Plotly.
PLOTLY_CONFIG = {
    "locale": "ru",
    "locales": {
        "ru": {
            "format": {
                "days": ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"],
                "shortDays": ["вс", "пн", "вт", "ср", "чт", "пт", "сб"],
                "months": [
                    "января", "февраля", "марта", "апреля", "мая", "июня",
                    "июля", "августа", "сентября", "октября", "ноября", "декабря",
                ],
                "shortMonths": ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"],
                "date": "%d.%m.%Y",
                "time": "%H:%M:%S",
                "dateTime": "%d.%m.%Y %H:%M:%S",
            },
        },
    },
}

STATUSES = ["Была боль", "Без боли", "Нет данных"]
COLORS = {
    "Была боль": "#E87662",
    "Без боли": "#FFBC87",
    "Нет данных": "#FCDCC7",
}

DEMO_CSV = """Дата,Головная боль,Интенсивность боли,Комментарии
2026-08-01,Нет,,
2026-08-02,Да,6,
2026-08-03,Да,4,
2026-08-05,Нет,,
2026-08-06,Да,,Автоматическая запись
2026-08-07,Нет,,
2026-08-09,Да,7,
2026-08-10,Нет,,
2026-07-01,Да,,Автоматическая запись
2026-07-07,Да,,
2026-07-12,Да,9,
2026-07-13,Нет,,
2026-06-01,Да,,Автоматическая запись
2026-06-07,Нет,,
2026-06-24,Да,4,
2026-05-10,Да,3,
""".encode("utf-8")


def read_diary(content: bytes) -> tuple[pd.DataFrame, list[str]]:
    """Чтение, проверка и нормализация CSV."""
    if len(content) > 5 * 1024 * 1024:
        raise ValueError("Файл слишком большой. Загрузите CSV размером до 5 МБ.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            text = content.decode("cp1251")
        except UnicodeDecodeError as error:
            raise ValueError("Не удалось прочитать текст. Нужна кодировка UTF-8 или Windows-1251.") from error
    if not text.strip():
        raise ValueError("Файл пуст. Выберите CSV с записями из бота.")
    try:
        header_line = next(line for line in text.splitlines() if line.strip())
        dialect = csv.Sniffer().sniff(header_line, delimiters=",;\t")
        rows = [row for row in csv.reader(StringIO(text), dialect, strict=True) if row]
    except csv.Error as error:
        raise ValueError("Не удалось разобрать CSV. Загрузите исходную выгрузку из бота.") from error
    header = [name.strip() for name in rows[0]]
    if len(header) != len(set(header)) or any(not name for name in header):
        raise ValueError("В CSV есть пустые или повторяющиеся названия столбцов.")
    missing = {"Дата", "Головная боль"} - set(header)
    if missing:
        raise ValueError("В файле не хватает столбцов: " + ", ".join(sorted(missing)))
    if len(rows) < 2:
        raise ValueError("В файле есть заголовки, но нет записей.")
    if any(len(row) != len(header) for row in rows[1:]):
        raise ValueError("В строках CSV разное число полей. Попробуйте заново выгрузить файл из бота.")

    frame = pd.DataFrame(rows[1:], columns=header)
    frame = frame.apply(lambda column: column.str.strip())
    frame["_date"] = pd.to_datetime(frame["Дата"], format="%Y-%m-%d", errors="coerce")
    if frame["_date"].isna().any():
        raise ValueError("В столбце «Дата» есть пустые или неверные даты. Нужен формат ГГГГ-ММ-ДД.")
    if (frame["_date"].max() - frame["_date"].min()).days > 36600:
        raise ValueError("Проверьте годы в датах: период файла превышает 100 лет.")
    pain = frame["Головная боль"].str.lower()
    if not pain.isin(["да", "нет", ""]).all():
        raise ValueError("В столбце «Головная боль» допустимы «Да», «Нет» или пустое поле.")
    frame["_pain"] = pain.map({"да": 1.0, "нет": 0.0})
    comments = frame.get("Комментарии", pd.Series("", index=frame.index))
    frame["_automatic"] = comments.str.contains("автоматическая запись", case=False, regex=False)
    intensity = frame.get("Интенсивность боли", pd.Series("", index=frame.index))
    values = pd.to_numeric(intensity.str.replace(",", ".", regex=False), errors="coerce")
    valid = values.between(0, 10)
    frame["_intensity"] = values.where(valid)
    invalid_count = int((intensity.ne("") & ~valid).sum())
    notices = []
    if invalid_count:
        notices.append(f"Не учтены некорректные оценки интенсивности: {invalid_count}. Ожидается число от 0 до 10.")
    return frame.sort_values("_date"), notices


def daily_summary(frame: pd.DataFrame, start, end) -> pd.DataFrame:
    """Одна дата = один день. Если хотя бы одна запись «Да», в этот день была боль."""
    dates = pd.date_range(start, end, name="Дата")
    pain_by_day = frame.groupby("_date")["_pain"].max().reindex(dates)
    result = pain_by_day.map({1.0: "Была боль", 0.0: "Без боли"}).fillna("Нет данных")
    return result.rename("Состояние").reset_index()


def show_dashboard(frame: pd.DataFrame, file_key: str) -> None:
    """Фильтры, показатели, графики и исходные записи."""
    first = frame["_date"].min().date()
    last = frame["_date"].max().date()
    controls = st.columns([2, 1])
    with controls[0]:
        period = st.date_input(
            "Период", value=(first, last), min_value=first, max_value=last,
            format="DD.MM.YYYY", key=f"period_{file_key}",
        )
    automatic_count = int(frame["_automatic"].sum())
    with controls[1]:
        include_automatic = st.checkbox(
            "Учитывать автоматические записи", value=False,
        )
    if len(period) != 2:
        st.info("Выберите начало и конец периода.")
        return
    start, end = period
    selected = frame.loc[frame["_date"].between(pd.Timestamp(start), pd.Timestamp(end))]
    excluded = int(selected["_automatic"].sum()) if not include_automatic else 0
    if not include_automatic:
        selected = selected.loc[~selected["_automatic"]]
    if automatic_count:
        st.caption(f"Автоматических записей в файле: {automatic_count}. Исключено в выбранном периоде: {excluded}.")

    daily = daily_summary(selected, start, end)
    counts = daily["Состояние"].value_counts()
    pain_days = int(counts.get("Была боль", 0))
    no_pain_days = int(counts.get("Без боли", 0))
    missing_days = int(counts.get("Нет данных", 0))
    recorded_days = pain_days + no_pain_days
    cards = st.columns(4)
    cards[0].metric("Дни с болью", pain_days)
    cards[1].metric("Дни без боли", no_pain_days)
    cards[2].metric("Дни без данных", missing_days)
    share = f"{pain_days / recorded_days:.0%}" if recorded_days else "—"
    cards[3].metric("Доля дней с болью", share, help="Дни с болью / дни с ответом «Да» или «Нет».")
    st.caption(f"Данные есть за {recorded_days} из {len(daily)} календарных дней. Считаем дни, а не отдельные приступы.")
    if selected.empty:
        st.info("За этот период нет записей с учётом выбранных настроек.")
    if selected["_date"].duplicated().any():
        st.info("На некоторые даты приходится несколько записей. Каждый день считается один раз; «Да» имеет приоритет.")

    st.subheader("Дни по месяцам")
    monthly = daily.assign(Месяц=daily["Дата"].dt.strftime("%Y-%m"))
    monthly = monthly.groupby(["Месяц", "Состояние"]).size().reset_index(name="Дни")
    chart = px.bar(
        monthly, x="Месяц", y="Дни", color="Состояние", barmode="stack",
        color_discrete_map=COLORS, category_orders={"Состояние": STATUSES},
    )
    chart.update_layout(legend_title_text="", margin=dict(l=0, r=0, t=10, b=0))
    chart.update_xaxes(type="category")
    chart.update_yaxes(dtick=5)
    st.plotly_chart(chart, width="stretch", config=PLOTLY_CONFIG)
    st.caption("На границах периода учитываются только выбранные даты, а не весь месяц.")

    st.subheader("Интенсивность боли")
    rated = selected.loc[selected["_pain"].eq(1) & selected["_intensity"].notna()]
    if rated.empty:
        st.info("В выбранных записях с болью нет заполненных оценок интенсивности.")
    else:
        st.metric("Средняя оценка", f"{rated['_intensity'].mean():.1f} / 10")
        st.caption(f"По заполненным оценкам в записях с болью: {len(rated)}. Пустые значения не заменяются нулями.")
        intensity_chart = px.scatter(
            rated, x="_date", y="_intensity",
            labels={"_date": "Дата", "_intensity": "Интенсивность"},
            color_discrete_sequence=[COLORS["Была боль"]],
        )
        intensity_chart.update_traces(marker_size=10)
        intensity_chart.update_yaxes(range=[-0.5, 10.5], dtick=1)
        intensity_chart.update_xaxes(tickformat="%d %b\n%Y", hoverformat="%d %B %Y")
        st.plotly_chart(intensity_chart, width="stretch", config=PLOTLY_CONFIG)

    with st.expander("Посмотреть дни и записи"):
        st.write("**Сводка по дням**")
        st.dataframe(daily, hide_index=True, width="stretch")
        st.write("**Записи, включённые в расчёт**")
        original_columns = [column for column in selected.columns if not column.startswith("_")]
        st.dataframe(selected[original_columns], hide_index=True, width="stretch")


def main() -> None:
    st.set_page_config(page_title="Дневник головной боли", page_icon="🧠", layout="wide")
    if "visitor_name" not in st.session_state:
        name, submitted = show_welcome_gate()
        if submitted:
            clean_name = " ".join(name.split())
            if clean_name:
                st.session_state["visitor_name"] = clean_name
                st.rerun()
            else:
                st.error("Введите имя, чтобы продолжить.")
        return

    show_main_header(st.session_state["visitor_name"])
    with st.container(border=True, key="diary-upload"):
        st.subheader("Начните со своего дневника")
        st.write("Выберите CSV-файл, который вы выгрузили из бота.")
        st.markdown("""
            <style>
            div[data-testid="stFileUploader"] button {
                font-size: 0 !important;
            }
            div[data-testid="stFileUploader"] button::before {
                content: 'ЗАГРУЗИТЬ ';
                font-size: 14px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Загрузите CSV из бота", type=["csv"], max_upload_size=5,
            key="diary_upload",
        )
        use_demo = st.checkbox("Посмотреть пример на вымышленных данных", value=False, key="show_demo")
        st.caption("CSV до 5 МБ · Без регистрации")
    if uploaded_file is not None:
        content = uploaded_file.getvalue()
    elif use_demo:
        content = DEMO_CSV
        st.warning("Показан вымышленный пример. Загрузите свой CSV, чтобы увидеть свои показатели.")
    else:
        show_steps()
        return

    try:
        frame, notices = read_diary(content)
    except ValueError as error:
        st.error(str(error))
        return
    for notice in notices:
        st.warning(notice)
    st.caption(f"Прочитано записей: {len(frame)}. Файл обрабатывается в памяти и не сохраняется приложением на диск.")
    show_dashboard(frame, sha256(content).hexdigest()[:12])


if __name__ == "__main__":
    main()
