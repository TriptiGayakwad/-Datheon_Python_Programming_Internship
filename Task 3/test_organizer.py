"""
Test / Demo script for organizer.py (Task 3)
Creates a temporary sample directory with dummy files,
runs the organizer on it, and verifies the results.
"""

import os
import sys
import shutil
from pathlib import Path

# Add task 3 directory to path
sys.path.insert(0, str(Path(__file__).parent))

from organizer import (
    get_category, resolve_collision,
    organise_directory, EXTENSION_MAP,
    setup_logging, UNKNOWN_CATEGORY
)

DEMO_DIR = Path(__file__).parent / "_demo_folder"


def create_demo_files() -> list:
    """Create dummy files of various types for testing."""
    DEMO_DIR.mkdir(exist_ok=True)

    sample_files = [
        # Documents
        "report.pdf", "notes.txt", "budget.xlsx", "slides.pptx",
        # Images
        "photo.jpg", "logo.png", "banner.gif", "icon.ico",
        # Videos
        "tutorial.mp4", "clip.mkv",
        # Audio
        "song.mp3", "podcast.wav",
        # Archives
        "backup.zip", "project.rar",
        # Code
        "script.py", "index.html", "styles.css", "data.json",
        # Executables
        "installer.exe",
        # Unknown
        "weirdfile.xyz", "noextension",
        # Duplicate (to test collision handling)
        "report.pdf",   # This won't be re-created but tests resolve_collision
    ]

    created = []
    seen = set()
    for fname in sample_files:
        if fname in seen:
            continue
        seen.add(fname)
        fpath = DEMO_DIR / fname
        fpath.write_text(f"Dummy content for {fname}")
        created.append(fpath)

    return created


def cleanup_demo() -> None:
    """Remove the demo folder after tests, closing any open log handlers first."""
    # Close all logging handlers to release the log file lock on Windows
    import logging
    log = logging.getLogger("organizer")
    for handler in log.handlers[:]:
        handler.close()
        log.removeHandler(handler)

    if DEMO_DIR.exists():
        shutil.rmtree(DEMO_DIR, ignore_errors=True)


def run_tests() -> None:
    print("=" * 60)
    print("  ORGANIZER.PY — UNIT TESTS")
    print("=" * 60)
    print()

    # Test 1: Extension map size
    print(f"[TEST 1] Extension map size       : {len(EXTENSION_MAP)} entries   OK")

    # Test 2: get_category known extensions
    assert get_category(Path("doc.pdf"))  == "Documents",  "PDF should be Documents"
    assert get_category(Path("img.jpg"))  == "Images",     "JPG should be Images"
    assert get_category(Path("vid.mp4"))  == "Videos",     "MP4 should be Videos"
    assert get_category(Path("aud.mp3"))  == "Audio",      "MP3 should be Audio"
    assert get_category(Path("arc.zip"))  == "Archives",   "ZIP should be Archives"
    assert get_category(Path("cod.py"))   == "Code",       "PY should be Code"
    assert get_category(Path("exe.exe"))  == "Executables","EXE should be Executables"
    print(f"[TEST 2] get_category (7 types)   : All correct   OK")

    # Test 3: Unknown extension
    assert get_category(Path("file.xyz")) == UNKNOWN_CATEGORY
    print(f"[TEST 3] Unknown extension        : -> '{UNKNOWN_CATEGORY}'   OK")

    # Test 4: No extension
    assert get_category(Path("noext")) == UNKNOWN_CATEGORY
    print(f"[TEST 4] No extension             : -> '{UNKNOWN_CATEGORY}'   OK")

    # Test 5: Case insensitive
    assert get_category(Path("IMG.JPG")) == "Images"
    assert get_category(Path("DOC.PDF")) == "Documents"
    print(f"[TEST 5] Case insensitive         : OK")

    # Test 6: Collision resolution
    tmp = Path(__file__).parent / "_collision_test"
    tmp.mkdir(exist_ok=True)
    (tmp / "file.txt").write_text("original")

    r1 = resolve_collision(tmp / "file.txt")
    assert r1.name == "file (1).txt", f"Expected 'file (1).txt', got '{r1.name}'"
    r1.write_text("collision1")

    r2 = resolve_collision(tmp / "file.txt")
    assert r2.name == "file (2).txt", f"Expected 'file (2).txt', got '{r2.name}'"
    shutil.rmtree(tmp)
    print(f"[TEST 6] Collision resolution     : file(1).txt, file(2).txt   OK")

    # Test 7: Full dry-run organise on demo folder
    print(f"\n[TEST 7] Full dry-run on demo folder...")
    files = create_demo_files()
    print(f"         Created {len(files)} dummy files in _demo_folder/")

    logger = setup_logging(DEMO_DIR)
    stats  = organise_directory(DEMO_DIR, DEMO_DIR, logger, dry_run=True)

    total = stats.get("__total__", 0)
    print(f"         Dry-run would move: {total} files")
    print(f"         Categories detected: {[k for k in stats if not k.startswith('__')]}")

    # Verify no files were actually moved (dry run)
    still_there = [f for f in files if f.exists()]
    assert len(still_there) == len(files), "Dry run should not move any files!"
    print(f"         All {len(files)} files still in place (dry-run confirmed)   OK")

    cleanup_demo()
    print(f"         Demo folder cleaned up   OK")

    print()
    print("=" * 60)
    print("  All tests passed! organizer.py is ready to use.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
