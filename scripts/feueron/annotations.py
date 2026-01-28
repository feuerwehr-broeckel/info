"""
Annotation definitions for FeuerON screenshots.

This file defines which markers (rectangles, circles) should be drawn
on each screenshot. Each key in ANNOTATIONS corresponds to a source
screenshot filename, and maps to a list of (output_suffix, markers) tuples.

This allows creating multiple annotated versions from a single screenshot.
"""

from tools.annotation import Marker

# Annotation definitions: source_filename -> list of (output_suffix, markers)
# Example: "01_feueron_homepage.png" -> [("_login_form", [Marker(...), ...]), ...]
ANNOTATIONS: dict[str, list[tuple[str, list[Marker]]]] = {
    # Homepage annotations
    "01_feueron_homepage.png": [
        # Example: Highlight the login form area
        # (
        #     "_login_highlighted",
        #     [
        #         Marker.rectangle(
        #             x=100, y=200, width=400, height=300,
        #             label="1",
        #             border_color="#ff0000",
        #             radius=8,
        #         ),
        #     ],
        # ),
    ],
    # Form filled annotations
    "02_feueron_form_filled.png": [
        # Example: Highlight username and password fields
        # (
        #     "_fields_highlighted",
        #     [
        #         Marker.rectangle(x=100, y=200, width=300, height=40, label="1"),
        #         Marker.rectangle(x=100, y=260, width=300, height=40, label="2"),
        #     ],
        # ),
    ],
    # Logged in annotations
    "03_feueron_logged_in.png": [],
    # Berichte annotations
    "04_feueron_berichte.png": [],
    # Dienstbuch annotations
    "05_feueron_dienstbuch.png": [],
}


def get_annotations() -> dict[str, list[tuple[str, list[Marker]]]]:
    """
    Get all annotation definitions.

    Returns:
        Dictionary mapping source filenames to lists of (output_suffix, markers) tuples
    """
    return ANNOTATIONS
