"""Screenshot annotation utilities."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont


@dataclass
class Marker:
    """
    An annotation marker for screenshots.

    Supports both rectangles and circles with customizable styling.

    For rectangles: x, y define top-left corner; width, height define size
    For circles: x, y define center; width is used as diameter (height is ignored)
    """

    # Required: Position and size
    x: int
    y: int
    width: int
    height: int = 0  # Not used for circles

    # Shape type
    shape: Literal["rectangle", "circle"] = "rectangle"

    # Colors
    fill_color: str = "#ff0000"
    border_color: str = "#ff0000"

    # Opacity (0-255)
    fill_opacity: int = 51  # 20% opacity
    border_opacity: int = 255  # 100% opacity

    # Border
    border_width: int = 2

    # Corner radius (only for rectangles)
    radius: int = 0

    # Label
    label: str | None = None
    label_size: int = 24
    label_color: str = "#ffffff"

    @classmethod
    def rectangle(
        cls,
        x: int,
        y: int,
        width: int,
        height: int,
        **kwargs,
    ) -> "Marker":
        """Create a rectangle marker."""
        return cls(x=x, y=y, width=width, height=height, shape="rectangle", **kwargs)

    @classmethod
    def circle(
        cls,
        x: int,
        y: int,
        diameter: int,
        **kwargs,
    ) -> "Marker":
        """Create a circle marker. x, y is the center point."""
        return cls(x=x, y=y, width=diameter, height=diameter, shape="circle", **kwargs)


def hex_to_rgba(hex_color: str, opacity: int = 255) -> tuple[int, int, int, int]:
    """Convert hex color to RGBA tuple."""
    hex_color = hex_color.lstrip("#")

    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b, opacity)


def annotate_screenshot(
    screenshot_path: Path,
    output_path: Path,
    markers: list[Marker],
) -> None:
    """
    Annotate a screenshot with markers (rectangles or circles).

    Args:
        screenshot_path: Path to the source screenshot
        output_path: Path where annotated image will be saved
        markers: List of Marker objects defining shapes to draw

    Example:
        markers = [
            Marker.rectangle(x=100, y=200, width=300, height=150, label="1"),
            Marker.circle(x=500, y=300, diameter=100, border_color="#00ff00", label="2"),
        ]
        annotate_screenshot(Path("input.png"), Path("output.png"), markers)
    """
    img = Image.open(screenshot_path).convert("RGBA")

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for marker in markers:
        fill_rgba = hex_to_rgba(marker.fill_color, marker.fill_opacity)
        border_rgba = hex_to_rgba(marker.border_color, marker.border_opacity)

        if marker.shape == "circle":
            radius = marker.width // 2
            x1 = marker.x - radius
            y1 = marker.y - radius
            x2 = marker.x + radius
            y2 = marker.y + radius

            draw.ellipse(
                [(x1, y1), (x2, y2)],
                fill=fill_rgba,
                outline=border_rgba,
                width=marker.border_width,
            )

            label_center_x = marker.x
            label_center_y = marker.y

        else:  # rectangle
            x2 = marker.x + marker.width
            y2 = marker.y + marker.height

            if marker.radius > 0:
                draw.rounded_rectangle(
                    [(marker.x, marker.y), (x2, y2)],
                    radius=marker.radius,
                    fill=fill_rgba,
                    outline=border_rgba,
                    width=marker.border_width,
                )
            else:
                draw.rectangle(
                    [(marker.x, marker.y), (x2, y2)],
                    fill=fill_rgba,
                    outline=border_rgba,
                    width=marker.border_width,
                )

            label_center_x = marker.x + marker.width // 2
            label_center_y = marker.y + marker.height // 2

        if marker.label:
            try:
                font = ImageFont.truetype(
                    "/System/Library/Fonts/Helvetica.ttc", marker.label_size
                )
            except Exception:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), marker.label, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            text_x = label_center_x - text_width // 2
            text_y = label_center_y - text_height // 2

            label_rgba = hex_to_rgba(marker.label_color, 255)
            draw.text((text_x, text_y), marker.label, fill=label_rgba, font=font)

    result = Image.alpha_composite(img, overlay)

    result = result.convert("RGB")
    result.save(output_path, "PNG", optimize=True)
