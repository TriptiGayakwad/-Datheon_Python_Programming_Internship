# 🐍 Datheon Python Programming Internship

> Internship project submissions for the **Datheon Python Programming Internship**.

---

## 📁 Project Structure

```
Datheon_Python_Programming_Internship/
│
├── task 1/              ← Task 1: Hangman Word Guessing Game
│   ├── hangman.py
│   ├── words.txt
│   └── README.md
│
├── task 2/              ← Task 2: Stock Portfolio Performance Tracker
│   ├── portfolio.py
│   ├── constituents.csv
│   ├── sp500_tickers.csv
│   └── README.md
│
├── task 3/              ← Task 3: Automated File Organizer & Cleanup Utility
│   ├── organizer.py
│   ├── test_organizer.py
│   └── README.md
│
└── README.md            ← This file
```

---

## ✅ Tasks Completed

### Task 1 — Hangman Word Guessing Game (Console)
- Terminal-based Hangman game with ASCII gallows art (7 stages)
- 210+ word bank loaded from `words.txt`
- Tracks guessed letters, prevents duplicate penalty, shows win/loss screens
- **Run:** `python "task 1/hangman.py"`

### Task 2 — Stock Portfolio Performance Tracker
- Enter stock tickers, buy prices, and share quantities
- Computes total value, gain/loss per holding, and overall portfolio %
- Loads full **503 S&P 500 tickers** from `constituents.csv`
- Exports performance snapshot to `portfolio_summary.csv`
- **Run:** `python "task 2/portfolio.py"`

### Task 3 — Automated File Organizer & Cleanup Utility
- Organises cluttered directories (e.g. Downloads) by file extension
- **84 extensions** mapped across 12 categories (Documents, Images, Videos, Audio, Archives, Code, Executables, Fonts, Ebooks, Others …)
- Dry Run mode, collision handling, permission-error safety, full logging
- **Run:** `python "task 3/organizer.py"`

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/TriptiGayakwad/Datheon_Python_Programming_Internship.git
cd Datheon_Python_Programming_Internship

# Task 1
python "task 1/hangman.py"

# Task 2
python "task 2/portfolio.py"

# Task 3 — interactive
python "task 3/organizer.py"

# Task 3 — CLI with dry run
python "task 3/organizer.py" "C:\Users\YourName\Downloads" --dry-run
```

---

## 🛠️ Requirements

- **Python 3.10+**
- **Standard Library only** for Tasks 1 & 3
- Task 2 optionally uses `yfinance` for live prices:
  ```bash
  pip install yfinance
  ```

---

## 👤 Author

**Tripti Gayakwad**
- Email: gayakwadtripti@outlook.com

---

*Submitted as part of the Datheon Python Programming Internship.*
