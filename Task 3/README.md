# 🗂️ Task 3 — Automated File Organizer & Cleanup Utility

> **Datheon Python Programming Internship** | Task 3 of 4

---

## 📋 Overview

An autonomous desktop automation utility that organizes cluttered directories
(e.g., Downloads folder). The script inspects every file's extension, dynamically
creates category subfolders, and safely moves files while handling permission
exceptions and naming collisions.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📁 Auto Category Folders | Creates `/Documents`, `/Images`, `/Videos`, `/Audio`, `/Archives`, `/Code`, `/Executables`, `/Fonts`, `/Ebooks`, `/Others` dynamically |
| 🔍 Extension Mapping | 80+ file extensions mapped to categories |
| 💥 Collision Handling | Duplicate filenames auto-renamed: `file.pdf` → `file (1).pdf` |
| 🔒 Permission Safety | `PermissionError` caught and skipped gracefully |
| 🧪 Dry Run Mode | Simulate organisation without moving any files |
| 🔁 Recursive Scan | Optionally scan subdirectories too |
| 📝 Log File | All actions logged to `organizer_log.txt` with timestamps |
| 📊 Summary Table | Formatted execution report: files per category, errors, time |
| 🖥️ CLI Support | Run directly with arguments: `python organizer.py <dir>` |
| 🎮 Interactive Menu | Guided prompts when run with no arguments |

---

## 🚀 How to Run

### Interactive Mode (recommended)
```bash
cd "task 3"
python organizer.py
```

### Command-Line Mode
```bash
# Organise a directory in-place (LIVE)
python organizer.py "C:\Users\YourName\Downloads"

# Organise into a separate target folder
python organizer.py "C:\Users\YourName\Downloads" "D:\Organised"

# Dry run — simulate without moving files
python organizer.py "C:\Users\YourName\Downloads" --dry-run
```

> **Requirements**: Python 3.10+, Standard Library only (`os`, `shutil`, `pathlib`, `logging`, `datetime`)

---

## 📂 Category Structure Created

```
Source Directory/
│
├── Documents/        ← .pdf .doc .docx .txt .xls .xlsx .ppt .csv .md ...
├── Images/           ← .jpg .jpeg .png .gif .bmp .svg .webp .ico .tiff ...
├── Videos/           ← .mp4 .mkv .avi .mov .wmv .flv .webm ...
├── Audio/            ← .mp3 .wav .flac .aac .ogg .wma .m4a ...
├── Archives/         ← .zip .rar .7z .tar .gz .iso .dmg ...
├── Code/             ← .py .js .html .css .java .cpp .json .sql .ipynb ...
├── Executables/      ← .exe .msi .apk .deb .rpm ...
├── Fonts/            ← .ttf .otf .woff .woff2 ...
├── Ebooks/           ← .epub .mobi .azw ...
├── Torrents/         ← .torrent ...
├── Incomplete_Downloads/ ← .crdownload .part ...
├── Others/           ← Any unrecognised extension
└── organizer_log.txt ← Full activity log with timestamps
```

---

## 🖥️ Sample Output

```
=================================================================
  AUTOMATED FILE ORGANIZER & CLEANUP UTILITY
  Datheon Python Programming Internship — Task 3
=================================================================
  Scanning : C:\Users\Name\Downloads
  Files found: 47

  [MOVED]   budget_2026.xlsx          =>  Documents/
  [MOVED]   photo_001.jpg             =>  Images/
  [MOVED]   setup.exe                 =>  Executables/
  [MOVED]   report.pdf (1)            =>  Documents/   (renamed: collision)
  [SKIPPED] locked_file.mp4           (PermissionError)

=================================================================
  EXECUTION SUMMARY
=================================================================
  CATEGORY                     FILES MOVED
  -----------------------------------------------------------------
  Documents                         18   ##################
  Images                            12   ############
  Videos                             7   #######
  Archives                           5   #####
  Code                               3   ###
  Others                             2   ##
  -----------------------------------------------------------------
  TOTAL FILES MOVED                 47
  ERRORS / SKIPPED                   1
  TIME ELAPSED                    0.43s
=================================================================
  [OK] Organisation complete! 47 file(s) relocated.
```

---

## 🔧 Technical Implementation

| Aspect | Implementation |
|---|---|
| Extension Lookup | Python `dict` — O(1) `.suffix.lower()` lookup |
| File Moving | `shutil.move()` for cross-drive safety |
| Collision Resolution | Counter loop: `file (1).pdf`, `file (2).pdf` … |
| Directory Walking | `os.walk()` for recursive, `Path.iterdir()` for flat |
| Folder Creation | `Path.mkdir(parents=True, exist_ok=True)` |
| Error Handling | `try/except` for `PermissionError`, `FileNotFoundError`, `shutil.Error` |
| Logging | `logging` module → both console + `organizer_log.txt` |

---

## 📁 Project Structure

```
task 3/
│
├── organizer.py        ← Main automation script
├── test_organizer.py   ← Unit test / demo script
├── organizer_log.txt   ← Auto-generated on first run
└── README.md           ← This file
```

---

*Submitted as part of the Datheon Python Programming Internship.*
