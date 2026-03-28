"""Free PIL fallback engine — generates styled placeholder images without any API."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def generate_product_image(
    item_name: str,
    bg_color: tuple[int, int, int],
    text_color: tuple[int, int, int],
    width: int = 1024,
    height: int = 1024,
    output_path: Path | None = None,
) -> Image.Image:
    """Generate a styled product placeholder image using PIL."""
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw decorative elements
    _draw_product_frame(draw, width, height, text_color, bg_color)

    # Draw product name
    _draw_centered_text(draw, item_name, width, height, text_color, size_ratio=0.06)

    # Draw subtle branding
    _draw_branding(draw, width, height, text_color)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path), quality=95)

    return img


def generate_social_image(
    headline: str,
    width: int = 1080,
    height: int = 1080,
    bg_color: tuple[int, int, int] = (6, 6, 8),
    text_color: tuple[int, int, int] = (0, 245, 212),
    output_path: Path | None = None,
) -> Image.Image:
    """Generate a social media image with headline text."""
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Accent bar at top
    accent_height = max(4, height // 200)
    draw.rectangle([(0, 0), (width, accent_height)], fill=text_color)

    # Draw headline
    _draw_centered_text(draw, headline, width, height, text_color, size_ratio=0.05)

    # Bottom branding
    _draw_branding(draw, width, height, text_color)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path), quality=95)

    return img


def _draw_product_frame(
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int,
    text_color: tuple[int, int, int],
    bg_color: tuple[int, int, int],
) -> None:
    """Draw a subtle product photography frame."""
    # Thin border
    border = max(2, width // 200)
    # Blend color between text and bg for subtle frame
    frame_color = tuple(
        (t + b) // 2 for t, b in zip(text_color, bg_color)
    )
    draw.rectangle(
        [(width // 10, height // 10), (width * 9 // 10, height * 9 // 10)],
        outline=frame_color,
        width=border,
    )

    # Center circle placeholder for product
    cx, cy = width // 2, height // 2
    radius = min(width, height) // 5
    draw.ellipse(
        [(cx - radius, cy - radius), (cx + radius, cy + radius)],
        outline=frame_color,
        width=border,
    )


def _draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    width: int,
    height: int,
    color: tuple[int, int, int],
    size_ratio: float = 0.05,
) -> None:
    """Draw text centered on the image."""
    target_size = max(16, int(width * size_ratio))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", target_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", target_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2 + height // 5  # Slightly below center
    draw.text((x, y), text, fill=color, font=font)


def _draw_branding(
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int,
    color: tuple[int, int, int],
) -> None:
    """Draw subtle NOUMENON branding at bottom."""
    brand = "RENDER-KIT"
    target_size = max(10, int(width * 0.02))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", target_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", target_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    # Dim the color
    dim_color = tuple(c // 3 for c in color)
    bbox = draw.textbbox((0, 0), brand, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    y = height - height // 15
    draw.text((x, y), brand, fill=dim_color, font=font)
