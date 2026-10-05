import numpy as np
import pandas as pd
import pytest

from dedup import find_duplicates, remove_duplicates, remove_duplicates_numpy, summarize


@pytest.fixture
def df():
    return pd.DataFrame({
        "name": ["Alice", "alice ", "Bob", "Bob", "Carol"],
        "email": ["a@x.com", "A@X.COM", "b@x.com", "b@x.com", "c@x.com"],
        "age": [30, 30, 25, 25, 40],
    })


def test_removes_messy_duplicates(df):
    out = remove_duplicates(df)
    assert len(out) == 3
    assert out["name"].tolist() == ["Alice", "Bob", "Carol"]  # original values kept


def test_case_sensitive_keeps_variants(df):
    out = remove_duplicates(df, case_insensitive=False)
    assert len(out) == 4


def test_subset(df):
    assert len(remove_duplicates(df, subset=["email"])) == 3


def test_keep_last(df):
    out = remove_duplicates(df, subset=["email"], keep="last")
    assert out["name"].tolist()[0] == "alice "


def test_keep_none(df):
    assert remove_duplicates(df, keep=False)["name"].tolist() == ["Carol"]


def test_find_duplicates(df):
    assert len(find_duplicates(df)) == 4


def test_bad_column(df):
    with pytest.raises(KeyError):
        remove_duplicates(df, subset=["nope"])


def test_bad_keep(df):
    with pytest.raises(ValueError):
        remove_duplicates(df, keep="middle")


def test_numpy_1d_preserves_order():
    assert remove_duplicates_numpy(np.array([3, 1, 3, 2, 1]), axis=None).tolist() == [3, 1, 2]


def test_numpy_2d_rows():
    a = np.array([[1, 2], [3, 4], [1, 2], [5, 6]])
    assert remove_duplicates_numpy(a).tolist() == [[1, 2], [3, 4], [5, 6]]


def test_summary(df):
    s = summarize(df, remove_duplicates(df))
    assert s["duplicates_removed"] == 2 and s["percent_removed"] == 40.0
