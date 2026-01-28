"""
Main entry point for generating FeuerON documentation screenshots.

This script orchestrates:
1. Taking screenshots using Playwright
2. Applying annotations to create highlighted versions
3. Wrapping screenshots in browser frames

Usage:
    uv run python -m scripts.feueron.generate [--screenshots-only] [--annotations-only] [--frames-only]
"""

import argparse
from pathlib import Path

from tools.annotation import annotate_screenshot
from tools.browserframe import wrap_in_browser_frame

from scripts.feueron.annotations import get_annotations
from scripts.feueron.screenshots import take_screenshots

# Output directories
SCREENSHOTS_DIR = Path("docs/assets/feueron/screenshots/raw")
ANNOTATED_DIR = Path("docs/assets/feueron/screenshots/annotated")
FRAMED_DIR = Path("docs/assets/feueron/screenshots/framed")


def generate_screenshots() -> list[Path]:
    """Take all FeuerON screenshots."""
    print("=" * 60)
    print("Taking FeuerON screenshots...")
    print("=" * 60)
    return take_screenshots(SCREENSHOTS_DIR)


def apply_annotations() -> list[Path]:
    """Apply annotations to screenshots."""
    print("\n" + "=" * 60)
    print("Applying annotations...")
    print("=" * 60)

    ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)

    annotations = get_annotations()
    output_paths: list[Path] = []

    for source_filename, annotation_list in annotations.items():
        source_path = SCREENSHOTS_DIR / source_filename

        if not source_path.exists():
            print(f"Warning: Source file not found: {source_path}")
            continue

        if not annotation_list:
            continue

        for output_suffix, markers in annotation_list:
            if not markers:
                continue

            output_filename = source_path.stem + output_suffix + source_path.suffix
            output_path = ANNOTATED_DIR / output_filename

            annotate_screenshot(source_path, output_path, markers)
            output_paths.append(output_path)
            print(f"Created annotated image: {output_path}")

    if output_paths:
        print(f"\nAnnotations completed: {len(output_paths)} files created")
    else:
        print(
            "\nNo annotations defined. Edit scripts/feueron/annotations.py to add markers."
        )

    return output_paths


def apply_frames() -> list[Path]:
    """Wrap screenshots in browser frames.

    Processes annotated screenshots if they exist, otherwise falls back to raw screenshots.
    """
    print("\n" + "=" * 60)
    print("Applying browser frames...")
    print("=" * 60)

    FRAMED_DIR.mkdir(parents=True, exist_ok=True)

    output_paths: list[Path] = []

    # Get all annotated screenshots
    annotated_files = (
        list(ANNOTATED_DIR.glob("*.png")) if ANNOTATED_DIR.exists() else []
    )

    # Get all raw screenshots
    raw_files = list(SCREENSHOTS_DIR.glob("*.png")) if SCREENSHOTS_DIR.exists() else []

    # Process annotated screenshots
    for source_path in annotated_files:
        output_path = FRAMED_DIR / source_path.name

        wrap_in_browser_frame(
            source_path,
            output_path,
            profile="generic_light",
            padding=40,
            shadow_amount=20,
        )
        output_paths.append(output_path)
        print(f"Created framed image: {output_path}")

    # Process raw screenshots that don't have annotated versions
    for source_path in raw_files:
        # Check if this raw file has any annotated versions
        has_annotated = any(
            af.stem.startswith(source_path.stem) for af in annotated_files
        )

        if not has_annotated:
            output_path = FRAMED_DIR / source_path.name

            wrap_in_browser_frame(
                source_path,
                output_path,
                profile="generic_light",
                padding=40,
                shadow_amount=20,
            )
            output_paths.append(output_path)
            print(f"Created framed image: {output_path}")

    if output_paths:
        print(f"\nFrames completed: {len(output_paths)} files created")
    else:
        print("\nNo screenshots found to frame.")

    return output_paths


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate FeuerON documentation screenshots"
    )
    parser.add_argument(
        "--screenshots-only",
        action="store_true",
        help="Only take screenshots, skip annotations and frames",
    )
    parser.add_argument(
        "--annotations-only",
        action="store_true",
        help="Only apply annotations, skip taking screenshots and frames",
    )
    parser.add_argument(
        "--frames-only",
        action="store_true",
        help="Only apply browser frames, skip taking screenshots and annotations",
    )
    args = parser.parse_args()

    try:
        if args.screenshots_only:
            generate_screenshots()
        elif args.annotations_only:
            apply_annotations()
        elif args.frames_only:
            apply_frames()
        else:
            generate_screenshots()
            apply_annotations()
            apply_frames()

        print("\n" + "=" * 60)
        print("Done!")
        print("=" * 60)

    except ValueError as e:
        print(f"Error: {e}")
        print("\nUsage:")
        print("  export FEUERON_USERNAME='your_username'")
        print("  export FEUERON_PASSWORD='your_password'")
        print("  export FEUERON_REGION_ID='156'  # Optional, defaults to 156")
        print("  uv run python -m scripts.feueron.generate")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
