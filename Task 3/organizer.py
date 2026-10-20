"""
╔══════════════════════════════════════════════════════════════╗
║     AUTOMATED FILE ORGANIZER & CLEANUP UTILITY — Task 3     ║
║     Datheon Python Programming Internship                    ║
╚══════════════════════════════════════════════════════════════╝

Description:
    An autonomous desktop automation utility that organizes cluttered
    directories (e.g., Downloads folder). The script inspects every
    file's extension, dynamically creates category subfolders
    (/Documents, /Images, /Videos, /Archives, /Code, etc.), and safely
    moves files while handling permission exceptions and naming
    collisions. Prints a formatted execution summary at the end.

Author   : Datheon Internship Submission
Language : Python 3
Modules  : os, shutil, pathlib, logging, datetime (Standard Library)
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────────────────────────
#  EXTENSION → CATEGORY MAPPING
#  Add or modify entries here to customise organisation rules.
# ─────────────────────────────────────────────────────────────
EXTENSION_MAP: dict[str, str] = {
    # Documents
    ".pdf":   "Documents",
    ".doc":   "Documents",
    ".docx":  "Documents",
    ".txt":   "Documents",
    ".rtf":   "Documents",
    ".odt":   "Documents",
    ".xls":   "Documents",
    ".xlsx":  "Documents",
    ".ppt":   "Documents",
    ".pptx":  "Documents",
    ".csv":   "Documents",
    ".md":    "Documents",

    # Images
    ".jpg":   "Images",
    ".jpeg":  "Images",
    ".png":   "Images",
    ".gif":   "Images",
    ".bmp":   "Images",
    ".svg":   "Images",
    ".webp":  "Images",
    ".ico":   "Images",
    ".tiff":  "Images",
    ".heic":  "Images",
    ".raw":   "Images",

    # Videos
    ".mp4":   "Videos",
    ".mkv":   "Videos",
    ".avi":   "Videos",
    ".mov":   "Videos",
    ".wmv":   "Videos",
    ".flv":   "Videos",
    ".webm":  "Videos",
    ".m4v":   "Videos",
    ".3gp":   "Videos",

    # Audio
    ".mp3":   "Audio",
    ".wav":   "Audio",
    ".flac":  "Audio",
    ".aac":   "Audio",
    ".ogg":   "Audio",
    ".wma":   "Audio",
    ".m4a":   "Audio",

    # Archives
    ".zip":   "Archives",
    ".rar":   "Archives",
    ".7z":    "Archives",
    ".tar":   "Archives",
    ".gz":    "Archives",
    ".bz2":   "Archives",
    ".xz":    "Archives",
    ".iso":   "Archives",
    ".dmg":   "Archives",

    # Code
    ".py":    "Code",
    ".js":    "Code",
    ".ts":    "Code",
    ".html":  "Code",
    ".css":   "Code",
    ".java":  "Code",
    ".c":     "Code",
    ".cpp":   "Code",
    ".cs":    "Code",
    ".go":    "Code",
    ".rs":    "Code",
    ".php":   "Code",
    ".rb":    "Code",
    ".sh":    "Code",
    ".bat":   "Code",
    ".sql":   "Code",
    ".json":  "Code",
    ".xml":   "Code",
    ".yaml":  "Code",
    ".yml":   "Code",
    ".ipynb": "Code",

    # Executables & Installers
    ".exe":   "Executables",
    ".msi":   "Executables",
    ".apk":   "Executables",
    ".deb":   "Executables",
    ".rpm":   "Executables",

    # Fonts
    ".ttf":   "Fonts",
    ".otf":   "Fonts",
    ".woff":  "Fonts",
    ".woff2": "Fonts",

    # Ebooks
    ".epub":  "Ebooks",
    ".mobi":  "Ebooks",
    ".azw":   "Ebooks",

    # Torrents & Downloads
    ".torrent": "Torrents",
    ".crdownload": "Incomplete_Downloads",
    ".part":  "Incomplete_Downloads",
}

UNKNOWN_CATEGORY = "Others"   # Category for unrecognised extensions
SEPARATOR        = "=" * 65
THIN_SEP         = "-" * 65


# ─────────────────────────────────────────────────────────────
#  LOGGING SETUP
#  Writes to both the terminal and organizer_log.txt
# ─────────────────────────────────────────────────────────────
def setup_logging(log_dir: Path) -> logging.Logger:
    """Configure logging to console + file."""
    log_file = log_dir / "organizer_log.txt"

    logger = logging.getLogger("organizer")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # File handler — verbose
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # Console handler — info only
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("  %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ─────────────────────────────────────────────────────────────
#  UTILITY — RESOLVE NAMING COLLISION
#  If destination file already exists, append (1), (2), … suffix.
# ─────────────────────────────────────────────────────────────
def resolve_collision(destination: Path) -> Path:
    """
    Return a unique file path by appending a counter suffix
    when a file with the same name already exists.

    Example:
        report.pdf  →  report (1).pdf  →  report (2).pdf
    """
    if not destination.exists():
        return destination

    stem      = destination.stem
    suffix    = destination.suffix
    parent    = destination.parent
    counter   = 1

    while True:
        new_name = parent / f"{stem} ({counter}){suffix}"
        if not new_name.exists():
            return new_name
        counter += 1


# ─────────────────────────────────────────────────────────────
#  UTILITY — GET CATEGORY FOR A FILE
# ─────────────────────────────────────────────────────────────
def get_category(file: Path) -> str:
    """Return the category folder name for a given file extension."""
    ext = file.suffix.lower()
    return EXTENSION_MAP.get(ext, UNKNOWN_CATEGORY)


# ─────────────────────────────────────────────────────────────
#  CORE — ORGANISE ONE FILE
# ─────────────────────────────────────────────────────────────
def organise_file(
    file: Path,
    target_root: Path,
    logger: logging.Logger,
    stats: dict,
    dry_run: bool = False,
) -> None:
    """
    Move a single file into the correct category subfolder.

    Args:
        file        : Path to the source file.
        target_root : Root directory where category folders are created.
        logger      : Logger instance.
        stats       : Mutable dict for tracking counts per category.
        dry_run     : If True, simulate actions without moving files.
    """
    category   = get_category(file)
    dest_dir   = target_root / category

    # Create category folder if it doesn't exist
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    dest_file  = resolve_collision(dest_dir / file.name)
    collided   = dest_file.name != file.name

    try:
        if not dry_run:
            shutil.move(str(file), str(dest_file))

        action = "[DRY-RUN]" if dry_run else "[MOVED]  "
        collision_note = f" -> renamed to '{dest_file.name}'" if collided else ""
        logger.info(f"{action} {file.name}{collision_note}  =>  {category}/")
        logger.debug(f"  Full path: {file} -> {dest_file}")

        stats[category] = stats.get(category, 0) + 1
        stats["__total__"] = stats.get("__total__", 0) + 1

    except PermissionError:
        logger.warning(f"[SKIPPED] Permission denied: {file.name}")
        stats["__errors__"] = stats.get("__errors__", 0) + 1

    except FileNotFoundError:
        logger.warning(f"[SKIPPED] File not found (already moved?): {file.name}")
        stats["__errors__"] = stats.get("__errors__", 0) + 1

    except shutil.Error as e:
        logger.warning(f"[SKIPPED] Move error for '{file.name}': {e}")
        stats["__errors__"] = stats.get("__errors__", 0) + 1

    except OSError as e:
        logger.error(f"[ERROR]   OS error for '{file.name}': {e}")
        stats["__errors__"] = stats.get("__errors__", 0) + 1


# ─────────────────────────────────────────────────────────────
#  CORE — SCAN AND ORGANISE DIRECTORY
# ─────────────────────────────────────────────────────────────
def organise_directory(
    source_dir: Path,
    target_dir: Path,
    logger: logging.Logger,
    dry_run: bool = False,
    skip_subdirs: bool = False,
) -> dict:
    """
    Scan source_dir and move all files into organised subfolders
    inside target_dir.

    Args:
        source_dir   : Directory to organise.
        target_dir   : Root destination for category folders.
        logger       : Logger instance.
        dry_run      : Simulate only — do not actually move files.
        skip_subdirs : If False (default), also scan subdirectories.

    Returns:
        stats dict with counts per category and error count.
    """
    stats: dict = {}
    files_found = 0

    logger.info(THIN_SEP)
    logger.info(f"Scanning : {source_dir}")
    logger.info(f"Target   : {target_dir}")
    logger.info(f"Mode     : {'DRY RUN (no files moved)' if dry_run else 'LIVE (files will be moved)'}")
    logger.info(THIN_SEP)

    # Collect all files to process
    if skip_subdirs:
        entries = [p for p in source_dir.iterdir() if p.is_file()]
    else:
        # Category folder names to skip when walking recursively
        category_folders = set(EXTENSION_MAP.values()) | {UNKNOWN_CATEGORY}

        entries = []
        for root, dirs, files in os.walk(source_dir):
            root_path = Path(root)
            # Skip walking into already-organised category subdirectories
            dirs[:] = [
                d for d in dirs
                if d not in category_folders
                and not (root_path == source_dir and d in category_folders)
            ]
            for fname in files:
                entries.append(root_path / fname)

    # Filter out the organizer script itself and the log file
    script_name = Path(__file__).name
    entries = [
        f for f in entries
        if f.name != script_name and not f.name.endswith("organizer_log.txt")
    ]

    files_found = len(entries)
    logger.info(f"Files found: {files_found}\n")

    if files_found == 0:
        logger.info("Nothing to organise — directory is already clean!")
        return stats

    for file in entries:
        organise_file(file, target_dir, logger, stats, dry_run=dry_run)

    return stats


# ─────────────────────────────────────────────────────────────
#  CORE — PRINT SUMMARY
# ─────────────────────────────────────────────────────────────
def print_summary(stats: dict, elapsed: float, dry_run: bool) -> None:
    """Print a formatted execution summary table."""
    total  = stats.pop("__total__", 0)
    errors = stats.pop("__errors__", 0)

    print(f"\n{SEPARATOR}")
    print(f"  EXECUTION SUMMARY  {'[DRY RUN]' if dry_run else ''}")
    print(SEPARATOR)
    print(f"  {'CATEGORY':<28}  {'FILES MOVED':>12}")
    print(f"  {THIN_SEP}")

    for category, count in sorted(stats.items(), key=lambda x: -x[1]):
        bar = "#" * min(count, 20)
        print(f"  {category:<28}  {count:>6}   {bar}")

    print(f"  {THIN_SEP}")
    print(f"  {'TOTAL FILES MOVED':<28}  {total:>12}")
    print(f"  {'ERRORS / SKIPPED':<28}  {errors:>12}")
    print(f"  {'TIME ELAPSED':<28}  {elapsed:>10.2f}s")
    print(SEPARATOR)

    if dry_run:
        print("\n  [i] DRY RUN complete. No files were actually moved.")
        print("      Re-run without --dry-run to apply changes.\n")
    else:
        print(f"\n  [OK] Organisation complete! {total} file(s) relocated.\n")


# ─────────────────────────────────────────────────────────────
#  UTILITY — INTERACTIVE DIRECTORY PICKER
# ─────────────────────────────────────────────────────────────
def pick_directory(prompt: str, default: str = "") -> Path:
    """Prompt the user to enter a directory path, with a default option."""
    while True:
        display = f" [{default}]" if default else ""
        raw = input(f"  {prompt}{display}: ").strip()

        if not raw and default:
            path = Path(default)
        else:
            path = Path(raw)

        if path.is_dir():
            return path.resolve()
        else:
            print(f"  [!] '{path}' is not a valid directory. Try again.\n")


# ─────────────────────────────────────────────────────────────
#  UTILITY — SHOW CATEGORY MAP
# ─────────────────────────────────────────────────────────────
def show_category_map() -> None:
    """Print all extension → category mappings."""
    print(f"\n{SEPARATOR}")
    print("  EXTENSION → CATEGORY MAPPING")
    print(SEPARATOR)

    # Group by category
    grouped: dict = {}
    for ext, cat in EXTENSION_MAP.items():
        grouped.setdefault(cat, []).append(ext)

    for cat in sorted(grouped):
        exts = "  ".join(sorted(grouped[cat]))
        print(f"  {cat:<25} {exts}")

    print(f"\n  Unknown extensions  =>  {UNKNOWN_CATEGORY}")
    print(f"  Total mapped extensions: {len(EXTENSION_MAP)}")
    print(SEPARATOR + "\n")


# ─────────────────────────────────────────────────────────────
#  UTILITY — SHOW MAIN HEADER
# ─────────────────────────────────────────────────────────────
def show_header() -> None:
    print(SEPARATOR)
    print("  AUTOMATED FILE ORGANIZER & CLEANUP UTILITY")
    print("  Datheon Python Programming Internship — Task 3")
    print(f"  {datetime.now().strftime('%A, %d %B %Y  |  %I:%M %p')}")
    print(SEPARATOR)


# ─────────────────────────────────────────────────────────────
#  MAIN — INTERACTIVE MODE
# ─────────────────────────────────────────────────────────────
def interactive_mode() -> None:
    """Run the organiser in interactive menu mode."""
    show_header()

    print("""
  MENU
  ─────────────────────────────────────────────────
  [1]  Organise a directory  (LIVE — files moved)
  [2]  Dry Run               (simulate, no changes)
  [3]  Show extension map
  [4]  Exit
    """)

    while True:
        try:
            choice = input("  Select option (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!\n")
            sys.exit(0)

        if choice in ("1", "2"):
            dry_run = (choice == "2")
            print()

            # Get source directory
            default_src = str(Path.home() / "Downloads")
            source_dir  = pick_directory("Source directory to organise", default_src)

            # Ask if target = source or separate folder
            separate = input(
                "\n  Organise IN PLACE (files stay in same folder) or "
                "into a SEPARATE folder?\n  Enter 'S' for separate, ENTER for in-place: "
            ).strip().lower()

            if separate == "s":
                target_dir = pick_directory("Destination root directory")
            else:
                target_dir = source_dir

            # Subdirectory option
            subdirs = input("\n  Also scan subdirectories? (y/n) [n]: ").strip().lower()
            skip_subdirs = (subdirs != "y")

            # Set up logging
            logger = setup_logging(target_dir)

            print(f"\n{SEPARATOR}")
            if dry_run:
                print("  DRY RUN MODE — no files will actually be moved")
            else:
                confirm = input(
                    f"  About to organise: {source_dir}\n"
                    f"  Are you sure? (y/n): "
                ).strip().lower()
                if confirm != "y":
                    print("  Cancelled.\n")
                    continue

            start = datetime.now()
            stats = organise_directory(source_dir, target_dir, logger,
                                       dry_run=dry_run, skip_subdirs=skip_subdirs)
            elapsed = (datetime.now() - start).total_seconds()

            print_summary(stats, elapsed, dry_run)
            input("  Press ENTER to return to menu...")
            show_header()
            print("\n  MENU\n  " + THIN_SEP)
            print("  [1]  Organise a directory  (LIVE)")
            print("  [2]  Dry Run")
            print("  [3]  Show extension map")
            print("  [4]  Exit\n")

        elif choice == "3":
            show_category_map()

        elif choice == "4":
            print("\n  Goodbye!\n")
            sys.exit(0)

        else:
            print("  [!] Invalid option. Enter 1, 2, 3, or 4.\n")


# ─────────────────────────────────────────────────────────────
#  MAIN — COMMAND-LINE MODE
#  Usage: python organizer.py <source_dir> [target_dir] [--dry-run]
# ─────────────────────────────────────────────────────────────
def cli_mode(args: list[str]) -> None:
    """Run the organiser from command-line arguments."""
    dry_run    = "--dry-run" in args
    clean_args = [a for a in args if not a.startswith("--")]

    if not clean_args:
        print("Usage: python organizer.py <source_dir> [target_dir] [--dry-run]")
        sys.exit(1)

    source_dir = Path(clean_args[0]).resolve()
    target_dir = Path(clean_args[1]).resolve() if len(clean_args) > 1 else source_dir

    if not source_dir.is_dir():
        print(f"[ERROR] '{source_dir}' is not a valid directory.")
        sys.exit(1)

    show_header()
    logger  = setup_logging(target_dir)
    start   = datetime.now()
    stats   = organise_directory(source_dir, target_dir, logger, dry_run=dry_run)
    elapsed = (datetime.now() - start).total_seconds()
    print_summary(stats, elapsed, dry_run)


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if args:
        cli_mode(args)
    else:
        interactive_mode()
