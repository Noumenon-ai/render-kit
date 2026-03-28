"""Voiceover generation using edge-tts (free, no GPU required)."""

from __future__ import annotations

import asyncio
from pathlib import Path

from rich.console import Console

console = Console()


def generate_voice(
    text: str,
    output: str = "renders/voiceover.wav",
    voice: str = "en-US-AriaNeural",
) -> Path | None:
    """Generate a voiceover from text using edge-tts."""
    try:
        import edge_tts
    except ImportError:
        console.print("  [red]edge-tts not installed. pip install render-kit[voice][/]")
        return None

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))

    try:
        asyncio.run(_generate())
        console.print(f"  [green]Saved:[/] {output_path}")
        return output_path
    except Exception as e:
        console.print(f"  [red]Voice generation error: {e}[/]")
        return None
