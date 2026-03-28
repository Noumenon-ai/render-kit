"""Render-Kit CLI — command definitions."""

from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from render_kit import __version__
from render_kit.presets import ALL_PRESET_NAMES, ALL_TEMPLATE_NAMES

app = typer.Typer(
    name="render-kit",
    help="Generate product photos and social media images from the command line.",
    no_args_is_help=True,
)
console = Console()


def _header():
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]RENDER-KIT[/] v{__version__}",
        border_style="cyan",
    ))
    console.print()


@app.command()
def product(
    item: str = typer.Argument(help="Product name or description"),
    preset: str = typer.Option("white_studio", "--preset", "-p", help=f"Preset: {', '.join(ALL_PRESET_NAMES)}"),
    all_presets: bool = typer.Option(False, "--all-presets", help="Generate all 5 presets"),
    output_dir: str = typer.Option("renders", "--output", "-o", help="Output directory"),
) -> None:
    """Generate product photography images."""
    from render_kit.product import generate_product

    _header()
    console.print(f"  Generating: [bold]{item}[/]")
    if all_presets:
        console.print("  Presets: [bold]all ({len(ALL_PRESET_NAMES)})[/]")
    else:
        console.print(f"  Preset: [bold]{preset}[/]")
    console.print()

    results = generate_product(item, preset=preset, output_dir=output_dir, all_presets=all_presets)
    console.print(f"\n  [bold green]{len(results)} images generated.[/]")


@app.command()
def social(
    headline: str = typer.Argument(help="Headline text for the image"),
    template: str = typer.Option("ig_square", "--template", "-t", help=f"Template: {', '.join(ALL_TEMPLATE_NAMES)}"),
    slides: int = typer.Option(1, "--slides", "-s", help="Number of slides (for carousel)"),
    output_dir: str = typer.Option("renders", "--output", "-o", help="Output directory"),
) -> None:
    """Generate social media images."""
    from render_kit.social import generate_social

    _header()
    console.print(f"  Headline: [bold]{headline}[/]")
    console.print(f"  Template: [bold]{template}[/]")
    if slides > 1:
        console.print(f"  Slides: [bold]{slides}[/]")
    console.print()

    results = generate_social(headline, template=template, slides=slides, output_dir=output_dir)
    console.print(f"\n  [bold green]{len(results)} images generated.[/]")


@app.command()
def video(
    scenes: str = typer.Option(..., "--scenes", help="Path to scenes JSON file"),
    fps: int = typer.Option(30, "--fps", help="Frames per second"),
    output: str = typer.Option("renders/output.mp4", "--output", "-o", help="Output file"),
) -> None:
    """Generate video from scenes JSON file."""
    from render_kit.video import generate_video

    _header()
    console.print(f"  Scenes: [bold]{scenes}[/]")
    console.print(f"  FPS: [bold]{fps}[/]")
    console.print()

    generate_video(scenes, fps=fps, output=output)


@app.command()
def voice(
    text: str = typer.Argument(help="Text to convert to speech"),
    output: str = typer.Option("renders/voiceover.wav", "--output", "-o", help="Output file"),
    speaker: str = typer.Option("en-US-AriaNeural", "--voice", "-v", help="Voice name"),
) -> None:
    """Generate voiceover from text."""
    from render_kit.voice import generate_voice

    _header()
    console.print(f"  Text: [bold]{text[:60]}...[/]" if len(text) > 60 else f"  Text: [bold]{text}[/]")
    console.print()

    generate_voice(text, output=output, voice=speaker)


@app.command()
def batch(
    csv_file: str = typer.Argument(help="CSV file with product names"),
    preset: str = typer.Option("white_studio", "--preset", "-p", help="Default preset"),
    output_dir: str = typer.Option("renders", "--output", "-o", help="Output directory"),
) -> None:
    """Batch generate product images from CSV."""
    from render_kit.batch import process_batch

    _header()
    console.print(f"  CSV: [bold]{csv_file}[/]")
    console.print(f"  Preset: [bold]{preset}[/]")
    console.print()

    results = process_batch(csv_file, preset=preset, output_dir=output_dir)
    console.print(f"\n  [bold green]{len(results)} images generated.[/]")


@app.command()
def version() -> None:
    """Show render-kit version."""
    console.print(f"render-kit v{__version__}")


if __name__ == "__main__":
    app()
