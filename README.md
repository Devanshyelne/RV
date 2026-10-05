# 🔄 Duplicate Entry Remover

A Python-based data cleaning tool that detects and removes duplicate entries from **CSV, Excel, and JSON files**.

The project provides both a **Command-Line Interface (CLI)** and an interactive **Streamlit web application**, making it useful for quickly cleaning datasets and preparing them for analysis or machine learning workflows.

## ✨ Features

- 📂 Supports **CSV, Excel, and JSON** files
- 🔍 Detects duplicate rows across all columns
- 🎯 Remove duplicates based on **specific columns**
- 🔤 Smart matching:
  - Ignores case differences
  - Handles extra whitespace
  - Example: `"Alice "` and `"alice"` are treated as the same value
- 🔢 Multiple duplicate-handling strategies:
  - Keep the first occurrence
  - Keep the last occurrence
  - Remove all duplicated entries
- 📊 Generates a summary of the cleaning process
- 📄 Export duplicated records for review
- 🌐 Interactive **Streamlit web interface**
- 💻 Command-Line Interface for programmatic usage
- 🧮 NumPy-based helper for order-preserving array deduplication
- 🧪 Includes unit tests

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🐼 Pandas | Data processing and duplicate detection |
| 🔢 NumPy | Array operations and deduplication |
| 🎈 Streamlit | Interactive web application |
| 🧪 Pytest | Unit testing |

---

## 📁 Project Structure

```text
PS-II/
│
├── dedup/
│   ├── __init__.py
│   └── core.py
│
├── data/
│   └── sample data files
│
├── tests/
│   └── test_dedup.py
│
├── app.py
├── main.py
├── generate_sample.py
├── requirements.txt
└── README.md
```

### Important Files

**`dedup/core.py`**  
Contains the main duplicate-removal and data-processing logic.

**`app.py`**  
Streamlit-based graphical web interface.

**`main.py`**  
Command-line interface for running the duplicate-removal process.

**`generate_sample.py`**  
Generates sample data for testing the project.

**`tests/test_dedup.py`**  
Contains unit tests for validating the duplicate-removal functionality.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/rudrapratapvarma/PS-II.git
cd PS-II
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Generate Sample Data

```bash
python generate_sample.py
```

---

# 🌐 Run the Streamlit Web App

Start the application using:

```bash
streamlit run app.py
```

The application will open in your browser.

### Using the Web App

1. Upload your dataset.
2. Select the columns that should be considered for duplicate detection.
3. Choose how duplicates should be handled.
4. Run the duplicate-removal process.
5. Review the results and summary.
6. Download the cleaned dataset.

---

# 💻 Command-Line Usage

The project can also be used directly from the terminal.

### Basic Usage

```bash
python main.py data/sample.csv
```

### Remove Duplicates Based on a Specific Column

```bash
python main.py data/sample.csv -o data/clean.csv --subset email
```

### Use Multiple Columns

```bash
python main.py data/sample.csv --subset name email
```

### Keep the Last Duplicate

```bash
python main.py data/sample.csv --subset name email --keep last
```

### Case-Sensitive Matching

```bash
python main.py data/sample.csv --subset name email --case-sensitive
```

### Generate a Duplicate Report

```bash
python main.py data/sample.csv --report-duplicates data/duplicates.csv
```

---

# 🧠 How Duplicate Detection Works

The application processes the dataset and identifies rows containing duplicate values.

For example:

| Name | Email |
|---|---|
| Alice | alice@gmail.com |
| Bob | bob@gmail.com |
| alice | alice@gmail.com |
| Charlie | charlie@gmail.com |

When matching is case-insensitive, the first and third rows are considered duplicates.

The cleaned dataset becomes:

| Name | Email |
|---|---|
| Alice | alice@gmail.com |
| Bob | bob@gmail.com |
| Charlie | charlie@gmail.com |

The system can also perform duplicate detection using only selected columns such as `email`, rather than comparing the entire row.

---

# 📊 Data Cleaning Workflow

```text
        Upload Dataset
              │
              ▼
      Read CSV / Excel / JSON
              │
              ▼
       Select Columns
              │
              ▼
    Normalize Data Values
   (case + whitespace handling)
              │
              ▼
       Detect Duplicates
              │
              ▼
      Choose Keep Strategy
       ┌──────┼──────┐
       ▼      ▼      ▼
     First   Last   Drop All
       │      │      │
       └──────┼──────┘
              ▼
       Cleaned Dataset
              │
              ▼
       Download / Export
```

---

# 🧩 Use as a Python Library

The duplicate-removal functionality can also be imported into another Python program.

```python
from dedup import load_data, remove_duplicates, remove_duplicates_numpy
import numpy as np

df = load_data("data/sample.csv")

clean = remove_duplicates(
    df,
    subset=["email"],
    keep="first"
)
```

### NumPy Example

```python
remove_duplicates_numpy(
    np.array([3, 1, 3, 2, 1]),
    axis=None
)
```

Output:

```text
[3, 1, 2]
```

---

# 🧪 Running Tests

Run the complete test suite using:

```bash
pytest -v
```

This verifies the core duplicate-removal functionality and helps ensure that changes do not break existing functionality.

---

# 📌 Supported File Types

| File Type | Supported |
|---|---|
| CSV | ✅ |
| Excel (`.xlsx`) | ✅ |
| JSON | ✅ |

---

# 🎯 Use Cases

This project can be useful for:

- 🧹 Cleaning raw datasets
- 📊 Data preprocessing
- 🤖 Machine Learning preprocessing
- 📁 Removing duplicate records
- 👥 Cleaning customer databases
- 📧 Removing duplicate email records
- 🗃️ Preparing datasets for analysis
- 🔬 Exploratory Data Analysis (EDA)

---

# 🔮 Future Improvements

Possible improvements include:

- [ ] Drag-and-drop file upload
- [ ] Support for larger datasets
- [ ] More detailed data-quality reports
- [ ] Duplicate similarity detection
- [ ] Fuzzy matching
- [ ] Advanced filtering options
- [ ] Dataset statistics and visualizations
- [ ] Docker support
- [ ] Cloud deployment
- [ ] Improved Streamlit UI
- [ ] Export reports in multiple formats

---

# 🌐 Live Demo

The project can be deployed using **Streamlit Community Cloud**.

Once deployed, add the live application URL here:

```text
🔗 Live Demo: YOUR_STREAMLIT_URL
```

---

# 👨‍💻 Author

**Rudrapratap Varma**

B.Tech Artificial Intelligence & Machine Learning

GitHub:  
https://github.com/rudrapratapvarma

---

# 📄 License

This project is currently intended for educational and project-development purposes.

If you plan to distribute it publicly, consider adding an appropriate open-source license such as MIT.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Built with Python, Pandas, NumPy & Streamlit.**
