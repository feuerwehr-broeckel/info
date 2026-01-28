"""Browser frame compositing tool.

Wraps screenshots in browser window frames using 9-slice scaling.
Based on https://browserframe.com/
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image, ImageChops, ImageDraw, ImageFilter


@dataclass
class Slice:
    """A slice region within the frame image."""

    x: int
    y: int
    w: int
    h: int


@dataclass
class FrameProfile:
    """Browser frame profile with 9-slice coordinates."""

    name: str
    frame_path: str
    outline_path: str | None
    slices: dict[str, Slice]


# Frame profiles from browserframe.com
PROFILES: dict[str, FrameProfile] = {
    "generic_light": FrameProfile(
        name="Generic · Light",
        frame_path="generic-light.png",
        outline_path="generic-outline.png",
        slices={
            "tl": Slice(x=0, y=0, w=159, h=77),
            "tc": Slice(x=465, y=0, w=20, h=77),
            "tr": Slice(x=1250, y=0, w=24, h=77),
            "l": Slice(x=0, y=412, w=1, h=10),
            "r": Slice(x=1273, y=412, w=1, h=10),
            "bl": Slice(x=0, y=423, w=11, h=11),
            "bc": Slice(x=33, y=433, w=10, h=1),
            "br": Slice(x=1263, y=423, w=11, h=11),
        },
    ),
    "generic_dark": FrameProfile(
        name="Generic · Dark",
        frame_path="generic-dark.png",
        outline_path="generic-outline.png",
        slices={
            "tl": Slice(x=0, y=0, w=159, h=77),
            "tc": Slice(x=465, y=0, w=20, h=77),
            "tr": Slice(x=1250, y=0, w=24, h=77),
            "l": Slice(x=0, y=412, w=1, h=10),
            "r": Slice(x=1273, y=412, w=1, h=10),
            "bl": Slice(x=0, y=423, w=11, h=11),
            "bc": Slice(x=33, y=433, w=10, h=1),
            "br": Slice(x=1263, y=423, w=11, h=11),
        },
    ),
}

# Type alias for profile names
ProfileName = Literal[
    "generic_light",
    "generic_dark",
]


def _get_assets_dir() -> Path:
    """Get the assets directory path."""
    return Path(__file__).parent / "assets"


def _compute_layout(
    slices: dict[str, Slice],
    screen_width: int,
    screen_height: int,
    padding: int,
) -> dict:
    """
    Compute the layout positions for all 9-slice regions.

    Based on computeLayout() from browserframe.com/js/core.js
    """
    x = padding
    y = padding
    w = screen_width
    h = screen_height

    canvas_size = {
        "w": slices["l"].w + w + slices["r"].w + (2 * padding),
        "h": slices["tl"].h + h + slices["bc"].h + (2 * padding),
    }

    return {
        "canvas_size": canvas_size,
        "blur": {
            "x": x + slices["bl"].w,
            "y": y + slices["bl"].w,
            "w": w - slices["bl"].w - slices["br"].w + slices["l"].w + slices["r"].w,
            "h": h + slices["tl"].h - slices["bl"].w,
        },
        "tl": {"x": x, "y": y, "w": slices["tl"].w, "h": slices["tl"].h},
        "tc": {
            "x": x + slices["tl"].w,
            "y": y,
            "w": w - slices["tl"].w - slices["tr"].w + slices["l"].w + slices["r"].w,
            "h": slices["tc"].h,
        },
        "tr": {
            "x": slices["l"].w + x + w - slices["tr"].w + slices["r"].w,
            "y": y,
            "w": slices["tr"].w,
            "h": slices["tr"].h,
        },
        "l": {
            "x": x,
            "y": y + slices["tl"].h,
            "w": slices["l"].w,
            "h": h - slices["bl"].h + slices["bc"].h,
        },
        "r": {
            "x": x + slices["l"].w + w,
            "y": y + slices["tr"].h,
            "w": slices["r"].w,
            "h": h - slices["br"].h + slices["bc"].h,
        },
        "bl": {
            "x": x,
            "y": y + slices["tl"].h + h - slices["bl"].h + slices["bc"].h,
            "w": slices["bl"].w,
            "h": slices["bl"].h,
        },
        "bc": {
            "x": x + slices["bl"].w,
            "y": y + slices["tc"].h + h,
            "w": w - slices["bl"].w - slices["br"].w + slices["l"].w + slices["r"].w,
            "h": slices["bc"].h,
        },
        "br": {
            "x": x + w - slices["br"].w + slices["l"].w + slices["r"].w,
            "y": y + slices["tl"].h + h - slices["bl"].h + slices["bc"].h,
            "w": slices["br"].w,
            "h": slices["br"].h,
        },
        "s": {
            "x": x + slices["l"].w,
            "y": y + slices["tl"].h,
            "w": w,
            "h": h,
        },
        "ft": {
            "x": x + slices["l"].w,
            "y": y + slices["tl"].h,
            "w": w,
            "h": h - slices["bl"].h + slices["bc"].h,
        },
        "fb": {
            "x": x + slices["bl"].w,
            "y": y + slices["tl"].h + h - slices["bl"].h + slices["bc"].h,
            "w": w - slices["bl"].w - slices["br"].w + slices["l"].w + slices["r"].w,
            "h": slices["bl"].h - 1,
        },
    }


def _draw_slice(
    canvas: Image.Image,
    frame: Image.Image,
    slice_coords: Slice,
    layout_coords: dict,
) -> None:
    """Draw a single slice from the frame image onto the canvas."""
    # Crop the slice from the frame
    region = frame.crop(
        (
            slice_coords.x,
            slice_coords.y,
            slice_coords.x + slice_coords.w,
            slice_coords.y + slice_coords.h,
        )
    )

    # Resize to target dimensions
    target_w = layout_coords["w"]
    target_h = layout_coords["h"]

    if target_w > 0 and target_h > 0:
        resized = region.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas.paste(resized, (layout_coords["x"], layout_coords["y"]), resized)


def _apply_shadow(
    canvas: Image.Image,
    layout: dict,
    shadow_color: str,
    shadow_amount: int,
) -> Image.Image:
    """Apply a drop shadow effect behind the frame."""
    # Create shadow layer
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)

    # Parse shadow color
    color = shadow_color.lstrip("#")
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    # Draw shadow rectangle in blur zone
    blur = layout["blur"]
    draw.rectangle(
        [blur["x"], blur["y"], blur["x"] + blur["w"], blur["y"] + blur["h"]],
        fill=(r, g, b, 180),
    )

    # Apply gaussian blur
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_amount))

    # Composite shadow behind canvas
    result = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    result = Image.alpha_composite(result, shadow)
    result = Image.alpha_composite(result, canvas)

    return result


def wrap_in_browser_frame(
    screenshot_path: Path,
    output_path: Path,
    profile: ProfileName = "generic_light",
    *,
    padding: int = 0,
    background_color: str | None = None,
    shadow_amount: int = 0,
    shadow_color: str = "#666666",
    screen_color: str | None = None,
    screen_scale: float = 1.0,
) -> None:
    """
    Wrap a screenshot in a browser frame.

    Args:
        screenshot_path: Path to the source screenshot
        output_path: Path where the framed image will be saved
        profile: Browser frame profile to use
        padding: Padding around the frame in pixels
        background_color: Background color (hex), None for transparent
        shadow_amount: Shadow blur radius (0 for no shadow)
        shadow_color: Shadow color (hex)
        screen_color: Fill color for screen area (hex), None uses screenshot
        screen_scale: Scale factor for the screenshot

    Example:
        wrap_in_browser_frame(
            Path("screenshot.png"),
            Path("framed.png"),
            profile="safari_light",
            padding=40,
            background_color="#f5f5f5",
            shadow_amount=20,
        )
    """
    # Get profile
    frame_profile = PROFILES.get(profile)
    if not frame_profile:
        raise ValueError(
            f"Unknown profile: {profile}. Available: {list(PROFILES.keys())}"
        )

    # Load images
    assets_dir = _get_assets_dir()
    frame_img = Image.open(assets_dir / frame_profile.frame_path).convert("RGBA")

    outline_img = None
    if frame_profile.outline_path:
        outline_path = assets_dir / frame_profile.outline_path
        if outline_path.exists():
            outline_img = Image.open(outline_path).convert("RGBA")

    screenshot = Image.open(screenshot_path).convert("RGBA")

    # Apply screen scale
    if screen_scale != 1.0:
        new_w = int(screenshot.width * screen_scale)
        new_h = int(screenshot.height * screen_scale)
        screenshot = screenshot.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Convert slices dict
    slices = frame_profile.slices

    # Ensure minimum screen size
    min_w = slices["tl"].w + slices["tr"].w
    min_h = slices["tl"].h + slices["bl"].h
    screen_w = max(screenshot.width, min_w)
    screen_h = max(screenshot.height, min_h)

    # Compute layout
    total_padding = padding + shadow_amount
    layout = _compute_layout(slices, screen_w, screen_h, total_padding)

    # Create canvas
    canvas_w = layout["canvas_size"]["w"]
    canvas_h = layout["canvas_size"]["h"]

    # Start with background
    if background_color:
        color = background_color.lstrip("#")
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (r, g, b, 255))
    else:
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Create foreground layer for frame (matches JS drawForeground)
    foreground = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Draw frame slices
    slice_keys = ["tl", "tc", "tr", "l", "r", "bl", "bc", "br"]
    for key in slice_keys:
        _draw_slice(foreground, frame_img, slices[key], layout[key])

    # Fill missing transparent screen areas with magenta (same as JS)
    # This allows source-atop compositing to clip corners properly
    # Note: PIL rectangle is inclusive on both ends, so subtract 1 from end coords
    fg_draw = ImageDraw.Draw(foreground)
    ft = layout["ft"]
    fb = layout["fb"]
    fg_draw.rectangle(
        [ft["x"], ft["y"], ft["x"] + ft["w"] - 1, ft["y"] + ft["h"] - 1],
        fill=(255, 0, 255, 255),
    )
    fg_draw.rectangle(
        [fb["x"], fb["y"], fb["x"] + fb["w"] - 1, fb["y"] + fb["h"] - 1],
        fill=(255, 0, 255, 255),
    )

    # Get foreground alpha for source-atop masking
    fg_alpha = foreground.split()[3]

    # Create screen content layer
    s = layout["s"]
    screen_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    if screen_color:
        # Fill with solid color
        color = screen_color.lstrip("#")
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        screen_draw = ImageDraw.Draw(screen_layer)
        screen_draw.rectangle(
            [s["x"], s["y"], s["x"] + s["w"], s["y"] + s["h"]],
            fill=(r, g, b, 255),
        )
    else:
        # Paste screenshot
        # Resize screenshot to fit screen area if needed
        if screenshot.width != s["w"] or screenshot.height != s["h"]:
            screenshot = screenshot.resize((s["w"], s["h"]), Image.Resampling.LANCZOS)
        screen_layer.paste(screenshot, (s["x"], s["y"]))

    # Apply source-atop compositing: screenshot only appears where foreground is opaque
    # This clips the screenshot corners to match the frame shape
    screen_alpha = screen_layer.split()[3]
    combined_alpha = ImageChops.multiply(screen_alpha, fg_alpha)
    screen_layer.putalpha(combined_alpha)

    # Composite screen over foreground (replaces magenta with screenshot)
    foreground = Image.alpha_composite(foreground, screen_layer)

    # Create outline layer (provides rounded corner background)
    outline_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    if outline_img:
        for key in slice_keys:
            _draw_slice(outline_layer, outline_img, slices[key], layout[key])

    # Composite: canvas <- shadow <- outline <- foreground (with screen)
    if shadow_amount > 0:
        canvas = _apply_shadow(canvas, layout, shadow_color, shadow_amount)

    # Draw outline behind foreground (destination-over equivalent)
    canvas = Image.alpha_composite(canvas, outline_layer)

    # Draw foreground (frame + screen) on top
    canvas = Image.alpha_composite(canvas, foreground)

    # Save result (preserve RGBA for transparency if no background color)
    if background_color:
        canvas = canvas.convert("RGB")
    canvas.save(output_path, "PNG", optimize=True)
