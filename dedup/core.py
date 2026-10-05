"""Core logic for detecting and removing duplicate entries."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd


# ---------------------------------------------------------------- I/O
def load_data(path: str | Path) -> pd.DataFrame:
    """Load CSV, Excel or JSON into a DataFrame based on file extension."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    if ext == ".json":
        return pd.read_json(path)
    raise ValueError(f"Unsupported file type '{ext}'. Use .csv, .xlsx or .json")


def save_data(df: pd.DataFrame, path: str | Path) -> Path:
    """Save a DataFrame to CSV, Excel or JSON based on file extension."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    if ext == ".csv":
        df.to_csv(path, index=False)
    elif ext in (".xlsx", ".xls"):
        df.to_excel(path, index=False)
    elif ext == ".json":
        df.to_json(path, orient="records", indent=2)
    else:
        raise ValueError(f"Unsupported output type '{ext}'")
    return path


# ---------------------------------------------------------- cleaning
def normalize(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    case_insensitive: bool = True,
    strip_whitespace: bool = True,
) -> pd.DataFrame:
    """Return a copy where text columns are trimmed / lower-cased and
    empty strings are turned into NaN, so near-identical rows match.
    """
    out = df.copy()
    cols = list(columns) if columns else list(out.columns)
    for col in cols:
        if col not in out.columns:
            raise KeyError(f"Column '{col}' not found. Available: {list(out.columns)}")
        if pd.api.types.is_object_dtype(out[col]) or pd.api.types.is_string_dtype(out[col]):
            s = out[col].astype("string")
            if strip_whitespace:
                s = s.str.strip().str.replace(r"\s+", " ", regex=True)
            if case_insensitive:
                s = s.str.lower()
            out[col] = s.replace("", pd.NA)
    return out


# --------------------------------------------------------- detection
def find_duplicates(
    df: pd.DataFrame,
    subset: Optional[Sequence[str]] = None,
    keep: str | bool = "first",
    case_insensitive: bool = True,
    strip_whitespace: bool = True,
) -> pd.DataFrame:
    """Return all rows that are involved in a duplication (keep=False view),
    sorted so duplicates sit next to each other.
    """
    _validate_keep(keep)
    key_df = normalize(df, subset, case_insensitive, strip_whitespace)
    mask = key_df.duplicated(subset=subset, keep=False)
    dupes = df[mask]
    if dupes.empty:
        return dupes
    sort_cols = list(subset) if subset else list(df.columns)
    order = key_df.loc[dupes.index, sort_cols].astype(str).apply(tuple, axis=1)
    return dupes.loc[order.sort_values(kind="stable").index]


# ----------------------------------------------------------- removal
def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[Sequence[str]] = None,
    keep: str | bool = "first",
    case_insensitive: bool = True,
    strip_whitespace: bool = True,
    reset_index: bool = True,
) -> pd.DataFrame:
    """Remove duplicate rows using pandas.

    Matching is done on a normalized copy, but the ORIGINAL values
    (original capitalisation / spacing) are what get returned.

    keep: 'first' | 'last' | False (drop every row that has a duplicate)
    """
    _validate_keep(keep)
    key_df = normalize(df, subset, case_insensitive, strip_whitespace)
    mask = key_df.duplicated(subset=subset, keep=keep)
    result = df[~mask]
    return result.reset_index(drop=True) if reset_index else result


def remove_duplicates_numpy(arr: np.ndarray, axis: Optional[int] = 0) -> np.ndarray:
    """Remove duplicates from a NumPy array while PRESERVING original order.

    axis=None -> unique elements of a flattened array
    axis=0    -> unique rows of a 2D array
    """
    arr = np.asarray(arr)
    if arr.size == 0:
        return arr
    _, idx = np.unique(arr, axis=axis, return_index=True)
    idx.sort()  # np.unique sorts values; sorting indices restores input order
    return arr[idx] if axis is None or arr.ndim == 1 else np.take(arr, idx, axis=axis)


# ----------------------------------------------------------- reporting
def summarize(original: pd.DataFrame, cleaned: pd.DataFrame) -> dict:
    """Small stats dictionary describing what was removed."""
    before, after = len(original), len(cleaned)
    removed = before - after
    return {
        "rows_before": before,
        "rows_after": after,
        "duplicates_removed": removed,
        "percent_removed": round(100 * removed / before, 2) if before else 0.0,
    }


def _validate_keep(keep) -> None:
    if keep not in ("first", "last", False):
        raise ValueError("keep must be 'first', 'last' or False")
