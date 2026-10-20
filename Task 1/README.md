# 🪤 Task 1 — Hangman Word Guessing Game (Console)

> **Datheon Python Programming Internship** | Task 1 of 4

---

## 📋 Overview

A fully interactive, terminal-based **Hangman** game written in pure Python 3.  
The player attempts to guess a hidden English word **letter by letter** within **6 incorrect attempts**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎨 ASCII Gallows Art | 7 progressive stages (0 – 6 wrong guesses) drawn in ASCII |
| 🔤 Word Masking | Hidden word displayed as `_ A _ H E O N` style |
| 📚 60+ Word Bank | Diverse words across animals, tech, nature, science, food |
| 🚫 Duplicate Guard | Re-guessing a letter gives a warning but **no extra penalty** |
| 🎯 Guess Tracker | Shows all guessed letters and wrong-only letters separately |
| 🏆 Victory Screen | Celebratory ASCII banner on winning |
| 💀 Game Over Screen | Dramatic loss banner revealing the secret word |
| 📊 Session Stats | Running Wins / Losses counter across multiple rounds |
| 🔄 Play Again | Re-play without restarting the program |
| 📖 Help/Instructions | Built-in rules accessible from the main menu |

---

## 🚀 How to Run

```bash
# Navigate to the project folder
cd Task_1_Hangman

# Run the game
python hangman.py
```

> **Requirements**: Python 3.6+ (uses only the Standard Library — `random`, `os`, `sys`)

---

## 🎮 How to Play

1. The game randomly picks a secret word.
2. Type **one letter** per turn and press **Enter**.
3. ✅ Correct guess → the letter is revealed in the word.
4. ❌ Wrong guess → a body part is added to the gallows.
5. You are **hanged after 6 wrong guesses** (head → body → left arm → right arm → left leg → right leg).
6. **Win** by revealing the full word before running out of chances!

---

## 📁 Project Structure

```
Task_1_Hangman/
│
├── hangman.py      ← Main game file (single-file, self-contained)
└── README.md       ← This file
```

---

## 🔧 Technical Implementation

| Aspect | Implementation |
|---|---|
| Word Selection | `random.choice()` from a built-in `WORD_BANK` list |
| Guess Tracking | Python `set` — O(1) lookup for duplicates |
| Word Masking | List comprehension over `secret` string |
| Screen Refresh | `os.system("cls"/"clear")` for clean per-turn display |
| Input Validation | Loop with `isalpha()` and length check |
| Modular Design | Separate functions for display, input, logic, and screens |

---

## 🖼️ Sample ASCII Gallows Stages

```
Stage 0        Stage 3        Stage 6
  +---+          +---+          +---+
  |   |          |   |          |   |
      |          O   |          O   |
      |         /|   |         /|\  |
      |              |         / \  |
      |              |              |
=========      =========      =========
```

---

## 📌 Notes

- All game logic uses only the **Python Standard Library** (`random`, `os`, `sys`).
- No external packages or downloads required.
- Fully cross-platform: works on Windows, macOS, and Linux.

---

*Submitted as part of the Datheon Python Programming Internship.*
