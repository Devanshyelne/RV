# Duplicate Entry Remover

A Python project (pandas + NumPy) that finds and removes duplicate entries from
CSV, Excel and JSON files.

## Features
- Remove duplicates across all columns or only chosen columns (`--subset`)
- Smart matching: ignores case and extra whitespace (`"Alice "` == `"alice"`)
- Keep `first`, `last`, or drop every duplicated row
- Export a review file of all duplicated rows
- NumPy helper for order-preserving de-duplication of arrays
- Summary report + unit tests

## Structure
```
duplicate_remover/
├── dedup/
│   ├── __init__.py
│   └── core.py            # all logic
├── tests/test_dedup.py
├── data/                  # sample data goes here
├── generate_sample.py     # creates data/sample.csv
├── app.py                 # Streamlit web app
├── main.py                # command-line interface
└── requirements.txt
```

## Setup
```bash
pip install -r requirements.txt
python generate_sample.py
```

## Run the web app (Streamlit)
```bash
streamlit run app.py
```
It opens at http://localhost:8501. Upload a file in the sidebar, pick columns,
click **Remove duplicates**, then download the clean file.

## Usage (command line)
```bash
python main.py data/sample.csv
python main.py data/sample.csv -o data/clean.csv --subset email
python main.py data/sample.csv --subset name email --keep last --case-sensitive
python main.py data/sample.csv --report-duplicates data/dupes.csv
```

## Use as a library
```python
from dedup import load_data, remove_duplicates, remove_duplicates_numpy
import numpy as np

df = load_data("data/sample.csv")
clean = remove_duplicates(df, subset=["email"], keep="first")

remove_duplicates_numpy(np.array([3, 1, 3, 2, 1]), axis=None)   # [3, 1, 2]
```

## Tests
```bash
pytest -v
```
