"""Social media image generation."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.progress import Progress

from render_kit.engines import pil as pil_engine
from render_kit.engines import replicate as replicate_engine
from render_kit.presets import SOCIAL_TEMPLATES

console = Console()


def generate_social(
    headline: str,
    template: str = "ig_square",
    slides: int = 1,
    output_dir: str = "renders",
) -> list[Path]:
    """Generate social media images."""
    config = SOCIAL_TEMPLATES.get(template)
    if not config:
        console.print(f"  [red]Unknown template: {template}[/]")
        console.print(f"  Available: {', '.join(SOCIAL_TEMPLATES.keys())}")
        return []

    output_path = Path(output_dir)
    width, height = config["width"], config["height"]
    is_multi = config.get("multi", False)
    num_slides = slides if is_multi else 1

    results: list[Path] = []

    with Progress(console=console) as progress:
        task = progress.add_task("Generating...", total=num_slides)

        for i in range(num_slides):
            if num_slides > 1:
                filename = f"slide_{i + 1}.png"
            else:
                slug = template.replace(" ", "_")
                filename = f"{slug}.png"

            filepath = output_path / filename

            # Try Replicate first
            if replicate_engine.is_available():
                prompt = f"Social media graphic, {headline}, modern design, clean typography, {width}x{height}"
                result = replicate_engine.generate_image(prompt, width=width, height=height, output_path=filepath)
                if result:
                    results.append(result)
                    console.print(f"  [green]Saved:[/] {filepath} ({width}x{height})")
                    progress.advance(task)
                    continue

            # PIL fallback
            pil_engine.generate_social_image(
                headline=headline if i == 0 else f"{headline} ({i + 1}/{num_slides})",
                width=width,
                height=height,
                output_path=filepath,
            )
            results.append(filepath)
            console.print(f"  [green]Saved:[/] {filepath} ({width}x{height})")
            progress.advance(task)

    return results
