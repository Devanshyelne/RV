"""Streamlit web app for removing duplicate entries.

Run with:  streamlit run app.py
"""
import io
from pathlib import Path

import pandas as pd
import streamlit as st

from dedup import find_duplicates, remove_duplicates, summarize

st.set_page_config(page_title="Duplicate Remover", page_icon="🧹", layout="wide")


# ------------------------------------------------------------ helpers
@st.cache_data(show_spinner=False)
def read_upload(name: str, content: bytes) -> pd.DataFrame:
    ext = Path(name).suffix.lower()
    buf = io.BytesIO(content)
    if ext == ".csv":
        return pd.read_csv(buf)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(buf)
    if ext == ".json":
        return pd.read_json(buf)
    raise ValueError(f"Unsupported file type: {ext}")


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()


# ----------------------------------------------------------------- UI
st.title("🧹 Duplicate Entry Remover")
st.caption("Upload a CSV, Excel or JSON file, choose how duplicates are detected, and download the clean file.")

# ---- sidebar: settings
with st.sidebar:
    st.header("⚙️ Settings")
    uploaded = st.file_uploader("Upload file", type=["csv", "xlsx", "xls", "json"])
    keep_label = st.radio(
        "Which duplicate to keep?",
        ["First occurrence", "Last occurrence", "None (drop all duplicated rows)"],
    )
    keep = {"First occurrence": "first", "Last occurrence": "last"}.get(keep_label, False)
    ignore_case = st.checkbox("Ignore upper/lower case", value=True)
    strip_ws = st.checkbox("Ignore extra spaces", value=True)

if uploaded is None:
    st.info("👈 Upload a file from the sidebar to get started. "
            "No file handy? Run `python generate_sample.py` to create `data/sample.csv`.")
    st.stop()

# ---- load data
try:
    df = read_upload(uploaded.name, uploaded.getvalue())
except Exception as exc:  # noqa: BLE001
    st.error(f"Could not read the file: {exc}")
    st.stop()

if df.empty:
    st.warning("The file has no rows.")
    st.stop()

st.subheader("1. Preview")
c1, c2 = st.columns(2)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", len(df.columns))
st.dataframe(df.head(50), use_container_width=True)

# ---- column choice
st.subheader("2. Choose columns that define a duplicate")
mode = st.radio("Compare by", ["All columns", "Selected columns"], horizontal=True)
subset = None
if mode == "Selected columns":
    subset = st.multiselect("Columns", list(df.columns), default=[df.columns[0]])
    if not subset:
        st.warning("Select at least one column.")
        st.stop()

opts = dict(subset=subset, case_insensitive=ignore_case, strip_whitespace=strip_ws)

# ---- run
st.subheader("3. Remove duplicates")
if st.button("🚀 Remove duplicates", type="primary"):
    try:
        clean = remove_duplicates(df, keep=keep, **opts)
        dupes = find_duplicates(df, keep=keep, **opts)
        st.session_state["result"] = (clean, dupes, summarize(df, clean))
    except Exception as exc:  # noqa: BLE001
        st.error(f"Something went wrong: {exc}")

if "result" in st.session_state:
    clean, dupes, stats = st.session_state["result"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows before", f"{stats['rows_before']:,}")
    m2.metric("Rows after", f"{stats['rows_after']:,}")
    m3.metric("Removed", f"{stats['duplicates_removed']:,}")
    m4.metric("% removed", f"{stats['percent_removed']}%")

    if stats["duplicates_removed"] == 0:
        st.success("No duplicates found. 🎉")

    tab1, tab2 = st.tabs(["✅ Clean data", "🔍 Duplicate rows (for review)"])
    with tab1:
        st.dataframe(clean, use_container_width=True)
    with tab2:
        if dupes.empty:
            st.write("No duplicated rows.")
        else:
            st.caption("Every row that has at least one duplicate, grouped together.")
            st.dataframe(dupes, use_container_width=True)

    st.subheader("4. Download")
    stem = Path(uploaded.name).stem
    d1, d2, d3 = st.columns(3)
    d1.download_button("⬇️ Clean CSV", to_csv_bytes(clean), f"{stem}_clean.csv", "text/csv")
    try:
        d2.download_button(
            "⬇️ Clean Excel", to_excel_bytes(clean), f"{stem}_clean.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except ImportError:
        d2.caption("Install `openpyxl` for Excel export.")
    if not dupes.empty:
        d3.download_button("⬇️ Duplicates report (CSV)", to_csv_bytes(dupes),
                           f"{stem}_duplicates.csv", "text/csv")
