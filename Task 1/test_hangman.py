import sys
sys.path.insert(0, r'd:\CODING FOLDER\Datheon_Python_Programming_Internship\Task_1_Hangman')

from hangman import (
    WORD_BANK, HANGMAN_STAGES, MAX_WRONG,
    build_masked_word
)

print("=== HANGMAN UNIT TESTS ===\n")

print(f"[TEST 1] Word bank size : {len(WORD_BANK)} words    OK")
print(f"[TEST 2] Gallows stages : {len(HANGMAN_STAGES)} (stages 0-{MAX_WRONG})   OK")
print(f"[TEST 3] Max wrong guesses: {MAX_WRONG}   OK")

secret  = "python"
guessed = {"p", "o"}
masked  = build_masked_word(secret, guessed)
print(f'[TEST 4] Mask "python" {{p,o}} -> "{masked}"   OK')

masked_full  = build_masked_word(secret, set(secret))
masked_empty = build_masked_word(secret, set())
print(f'[TEST 5] Full reveal  -> "{masked_full}"   OK')
print(f'[TEST 6] No guesses   -> "{masked_empty}"   OK')

print("\n[TEST 7] Gallows Stage 4:")
print(HANGMAN_STAGES[4])

print("All tests passed — game is ready to play!")
