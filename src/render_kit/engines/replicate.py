"""Replicate API engine — uses Flux AI for high-quality image generation."""

from __future__ import annotations

import os
from pathlib import Path

from rich.console import Console

console = Console()


def is_available() -> bool:
    """Check if Replicate API key is configured."""
    return bool(os.environ.get("REPLICATE_API_TOKEN"))


def generate_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    output_path: Path | None = None,
) -> Path | None:
    """Generate an image using Flux AI via Replicate API."""
    if not is_available():
        console.print("  [dim]Replicate API not configured. Set REPLICATE_API_TOKEN.[/]")
        console.print("  [dim]Falling back to PIL engine.[/]")
        return None

    try:
        import replicate
    except ImportError:
        console.print("  [dim]replicate package not installed. pip install render-kit[ai][/]")
        return None

    try:
        output = replicate.run(
            "black-forest-labs/flux-1.1-pro",
            input={
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_outputs": 1,
                "output_format": "png",
            },
        )

        if output and output_path:
            import urllib.request
            url = output[0] if isinstance(output, list) else output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(str(url), str(output_path))
            return output_path

    except Exception as e:
        console.print(f"  [red]Replicate error: {e}[/]")
        return None

    return None
