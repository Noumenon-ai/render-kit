"""Product photography generation."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.progress import Progress

from render_kit.engines import pil as pil_engine
from render_kit.engines import replicate as replicate_engine
from render_kit.presets import ALL_PRESET_NAMES, PRODUCT_PRESETS

console = Console()


def generate_product(
    item_name: str,
    preset: str = "white_studio",
    output_dir: str = "renders",
    all_presets: bool = False,
) -> list[Path]:
    """Generate product photography images."""
    presets_to_run = ALL_PRESET_NAMES if all_presets else [preset]
    output_path = Path(output_dir)
    results: list[Path] = []

    with Progress(console=console) as progress:
        task = progress.add_task("Generating...", total=len(presets_to_run))

        for preset_name in presets_to_run:
            config = PRODUCT_PRESETS.get(preset_name)
            if not config:
                console.print(f"  [red]Unknown preset: {preset_name}[/]")
                progress.advance(task)
                continue

            slug = item_name.lower().replace(" ", "_")
            filename = f"{slug}_{preset_name}.png"
            filepath = output_path / filename

            # Try Replicate first, fall back to PIL
            prompt = f"{item_name}, {config['prompt_suffix']}"
            if replicate_engine.is_available():
                result = replicate_engine.generate_image(prompt, output_path=filepath)
                if result:
                    results.append(result)
                    console.print(f"  [green]Saved:[/] {filepath} (Flux AI)")
                    progress.advance(task)
                    continue

            # PIL fallback
            pil_engine.generate_product_image(
                item_name=item_name,
                bg_color=config["bg_color"],
                text_color=config["text_color"],
                output_path=filepath,
            )
            results.append(filepath)
            console.print(f"  [green]Saved:[/] {filepath} (PIL)")
            progress.advance(task)

    return results
