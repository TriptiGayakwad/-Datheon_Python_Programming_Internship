"""
╔══════════════════════════════════════════════════════════════╗
║          HANGMAN WORD GUESSING GAME — Task 1                 ║
║          Datheon Python Programming Internship               ║
╚══════════════════════════════════════════════════════════════╝

Description:
    A terminal-based Hangman game where the player tries to guess
    a hidden word letter by letter within 6 incorrect attempts.
    Features ASCII gallows art, guess tracking, and duplicate
    penalty prevention.

Author  : Datheon Internship Submission
Language: Python 3
"""

import random
import os
import sys


# ─────────────────────────────────────────────────────────────
#  WORD BANK — loaded from words.txt
#  Falls back to a small built-in list if the file is missing.
# ─────────────────────────────────────────────────────────────

# Built-in fallback list (used only if words.txt is not found)
_FALLBACK_WORDS = [
    "elephant", "dolphin", "penguin", "python", "algorithm",
    "database", "hurricane", "volcano", "waterfall", "spaghetti",
    "avocado", "chemistry", "telescope", "adventure", "mystery",
    "symphony", "knowledge", "treasure", "skeleton", "paradise",
]


def load_word_bank(filename: str = "words.txt") -> list:
    """
    Load words from a plain-text word list file.

    The file must have ONE word per line.
    Words shorter than 4 characters are skipped to keep the game fun.
    If the file cannot be found or read, the built-in fallback list is used.

    Args:
        filename: Name of the word list file (in the same directory as this script).

    Returns:
        A list of lowercase words ready for random selection.
    """
    # Resolve the file path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath   = os.path.join(script_dir, filename)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            words = [
                line.strip().lower()
                for line in f
                if line.strip().isalpha() and len(line.strip()) >= 4
            ]
        if words:
            print(f"  [OK]  Loaded {len(words)} words from '{filename}'.")
            return words
        else:
            print(f"  [!]   '{filename}' is empty or has no valid words. Using built-in list.")
    except FileNotFoundError:
        print(f"  [!]   '{filename}' not found. Using built-in word list.")
    except OSError as e:
        print(f"  [!]   Could not read '{filename}': {e}. Using built-in word list.")

    return _FALLBACK_WORDS


# Load words once at startup
WORD_BANK = load_word_bank("words.txt")


# ─────────────────────────────────────────────────────────────
#  ASCII GALLOWS ART  (stages 0 → 6)
#  Stage 0 = empty gallows, Stage 6 = fully hanged figure
# ─────────────────────────────────────────────────────────────
HANGMAN_STAGES = [
    # Stage 0 — No wrong guesses yet
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========
    """,
    # Stage 1 — Head
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========
    """,
    # Stage 2 — Head + Body
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
    """,
    # Stage 3 — Head + Body + Left Arm
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
    """,
    # Stage 4 — Head + Body + Both Arms
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
    """,
    # Stage 5 — Head + Body + Both Arms + Left Leg
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
    """,
    # Stage 6 — FULL FIGURE (game over)
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
    """,
]

MAX_WRONG = len(HANGMAN_STAGES) - 1   # = 6


# ─────────────────────────────────────────────────────────────
#  UTILITY — CLEAR SCREEN
# ─────────────────────────────────────────────────────────────
def clear_screen() -> None:
    """Clear the terminal for a clean display."""
    os.system("cls" if os.name == "nt" else "clear")


# ─────────────────────────────────────────────────────────────
#  UTILITY — DISPLAY HEADER
# ─────────────────────────────────────────────────────────────
def display_header() -> None:
    """Print the game title banner."""
    print("=" * 60)
    print("       ██╗  ██╗ █████╗ ███╗  ██╗ ██████╗ ███╗  ███╗ █████╗ ███╗  ██╗")
    print("       ██║  ██║██╔══██╗████╗ ██║██╔════╝ ████╗████║██╔══██╗████╗ ██║")
    print("       ███████║███████║██╔██╗██║██║  ███╗██╔████╔██║███████║██╔██╗██║")
    print("       ██╔══██║██╔══██║██║╚████║██║   ██║██║╚██╔╝██║██╔══██║██║╚████║")
    print("       ██║  ██║██║  ██║██║ ╚███║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚███║")
    print("       ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚══╝")
    print("=" * 60)
    print("        Word Guessing Game  |  6 Wrong Guesses Allowed")
    print("=" * 60)


# ─────────────────────────────────────────────────────────────
#  UTILITY — BUILD MASKED WORD
# ─────────────────────────────────────────────────────────────
def build_masked_word(secret: str, guessed: set) -> str:
    """
    Return the word with unguessed letters replaced by underscores.

    Example:
        secret  = "python"
        guessed = {'p', 'o'}
        returns → "p _ t h o n"  → displayed as "P _ T H O N"
    """
    return " ".join(
        letter.upper() if letter in guessed else "_"
        for letter in secret
    )


# ─────────────────────────────────────────────────────────────
#  UTILITY — DISPLAY GAME STATE
# ─────────────────────────────────────────────────────────────
def display_game_state(
    secret: str,
    guessed_letters: set,
    wrong_guesses: set,
    wrong_count: int,
) -> None:
    """Render the current game board to the terminal."""
    clear_screen()
    display_header()

    # ASCII gallows
    print(HANGMAN_STAGES[wrong_count])

    # Masked word
    masked = build_masked_word(secret, guessed_letters)
    print(f"  Word  : {masked}")
    print(f"  Length: {len(secret)} letters\n")

    # Wrong guesses
    wrong_sorted = sorted(wrong_guesses)
    wrong_display = "  ".join(w.upper() for w in wrong_sorted) if wrong_sorted else "None"
    print(f"  Wrong guesses ({wrong_count}/{MAX_WRONG}): {wrong_display}")
    print(f"  All guessed   : {', '.join(sorted(l.upper() for l in guessed_letters)) or 'None'}")
    print()


# ─────────────────────────────────────────────────────────────
#  UTILITY — VICTORY SCREEN
# ─────────────────────────────────────────────────────────────
def display_victory(secret: str, wrong_count: int) -> None:
    """Show a celebratory win screen."""
    clear_screen()
    print("\n" + "🎉" * 30)
    print("""
  ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗  ██╗██╗
  ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗ ██║██║
   ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗██║██║
    ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚████║╚═╝
     ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚███║██╗
     ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚══╝╚═╝
    """)
    print(f"  ✅  The word was: {secret.upper()}")
    print(f"  🎯  Wrong guesses used: {wrong_count} / {MAX_WRONG}")
    print("🎉" * 30 + "\n")


# ─────────────────────────────────────────────────────────────
#  UTILITY — GAME OVER SCREEN
# ─────────────────────────────────────────────────────────────
def display_game_over(secret: str) -> None:
    """Show a dramatic loss screen."""
    clear_screen()
    print("\n" + "💀" * 30)
    print("""
   ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
  ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
    """)
    print(HANGMAN_STAGES[MAX_WRONG])
    print(f"  ☠️   The word was: {secret.upper()}")
    print(f"  Better luck next time!\n")
    print("💀" * 30 + "\n")


# ─────────────────────────────────────────────────────────────
#  CORE — GET PLAYER GUESS
# ─────────────────────────────────────────────────────────────
def get_player_guess(guessed_letters: set) -> str:
    """
    Prompt the player for a single alphabetic letter.
    Re-prompts on:
        - Non-alphabetic input
        - Input longer than one character
        - Previously guessed letters (no penalty deducted)
    Returns the validated, lowercase letter.
    """
    while True:
        try:
            guess = input("  👉  Enter a letter: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Game interrupted. Goodbye!\n")
            sys.exit(0)

        if len(guess) != 1:
            print("  ⚠️   Please enter exactly ONE letter.\n")
            continue

        if not guess.isalpha():
            print("  ⚠️   Only alphabetic characters are accepted.\n")
            continue

        if guess in guessed_letters:
            print(f"  🔁  You already guessed '{guess.upper()}'. No penalty. Try another!\n")
            continue

        return guess


# ─────────────────────────────────────────────────────────────
#  CORE — PLAY ONE ROUND
# ─────────────────────────────────────────────────────────────
def play_game() -> bool:
    """
    Run one complete round of Hangman.

    Returns:
        True  → player won
        False → player lost
    """
    secret          = random.choice(WORD_BANK)
    guessed_letters: set = set()
    wrong_guesses:   set = set()
    wrong_count:     int = 0

    while wrong_count < MAX_WRONG:
        display_game_state(secret, guessed_letters, wrong_guesses, wrong_count)

        # Check if all letters have been revealed
        if all(letter in guessed_letters for letter in secret):
            display_victory(secret, wrong_count)
            return True

        guess = get_player_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret:
            print(f"\n  ✅  Great! '{guess.upper()}' is in the word!\n")
        else:
            wrong_count += 1
            wrong_guesses.add(guess)
            remaining = MAX_WRONG - wrong_count
            if remaining > 0:
                print(f"\n  ❌  '{guess.upper()}' is NOT in the word. "
                      f"{remaining} chance(s) remaining.\n")
            else:
                print(f"\n  ❌  '{guess.upper()}' is NOT in the word. No more chances!\n")

        # Small pause to let player read feedback
        input("  Press ENTER to continue...")

    # Check one last time after the final guess loop exits
    if all(letter in guessed_letters for letter in secret):
        display_victory(secret, wrong_count)
        return True

    display_game_over(secret)
    return False


# ─────────────────────────────────────────────────────────────
#  CORE — ASK TO PLAY AGAIN
# ─────────────────────────────────────────────────────────────
def ask_play_again() -> bool:
    """Return True if the player wants another round."""
    while True:
        try:
            choice = input("  🔄  Play again? (y / n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False

        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("  ⚠️   Please type 'y' for yes or 'n' for no.\n")


# ─────────────────────────────────────────────────────────────
#  CORE — SHOW INSTRUCTIONS
# ─────────────────────────────────────────────────────────────
def show_instructions() -> None:
    """Print the rules of the game."""
    clear_screen()
    display_header()
    print("""
  HOW TO PLAY
  ───────────
  1. A secret English word is chosen at random.
  2. You guess ONE letter at a time.
  3. Correct guess  → the letter is revealed in the word.
  4. Wrong guess    → a body part is added to the gallows.
  5. You lose after 6 wrong guesses (head, body, 2 arms, 2 legs).
  6. You win by revealing the complete word before being hanged!

  RULES
  ─────
  • Guessing a letter you already tried costs NO extra penalty.
  • Only single alphabetic characters are accepted.
  • The game is case-insensitive (a = A).
    """)
    input("  Press ENTER to start playing...\n")


# ─────────────────────────────────────────────────────────────
#  CORE — MAIN MENU
# ─────────────────────────────────────────────────────────────
def main_menu() -> str:
    """
    Display the main menu and return the player's choice.

    Returns:
        'play'  → start game
        'help'  → show instructions
        'quit'  → exit
    """
    clear_screen()
    display_header()
    print("""
  MAIN MENU
  ─────────
  [1]  Play Game
  [2]  How to Play
  [3]  Quit
    """)
    while True:
        try:
            choice = input("  Select an option (1 / 2 / 3): ").strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"

        if choice == "1":
            return "play"
        if choice == "2":
            return "help"
        if choice == "3":
            return "quit"
        print("  ⚠️   Invalid option. Please enter 1, 2, or 3.\n")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
def main() -> None:
    """Program entry point — orchestrates menu → game → replay loop."""
    wins   = 0
    losses = 0

    while True:
        action = main_menu()

        if action == "quit":
            clear_screen()
            print("\n  Thanks for playing Hangman! 👋\n")
            print(f"  📊  Session Stats:  Wins={wins}  |  Losses={losses}\n")
            sys.exit(0)

        if action == "help":
            show_instructions()
            continue

        # action == "play"
        won = play_game()
        if won:
            wins   += 1
        else:
            losses += 1

        print(f"  📊  Session Stats:  Wins={wins}  |  Losses={losses}\n")

        if not ask_play_again():
            clear_screen()
            print("\n  Thanks for playing Hangman! 👋\n")
            print(f"  📊  Final Stats:  Wins={wins}  |  Losses={losses}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
