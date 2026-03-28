"""Video generation from PIL frames + FFmpeg."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

from render_kit.engines.pil import _draw_centered_text

console = Console()


def generate_video(
    scenes_file: str,
    fps: int = 30,
    duration_per_scene: float = 3.0,
    width: int = 1920,
    height: int = 1080,
    output: str = "renders/output.mp4",
) -> Path | None:
    """Generate a video from a scenes JSON file."""
    if not shutil.which("ffmpeg"):
        console.print("  [red]FFmpeg not found. Install it: sudo apt install ffmpeg[/]")
        return None

    try:
        scenes = json.loads(Path(scenes_file).read_text())
    except (json.JSONDecodeError, OSError) as e:
        console.print(f"  [red]Error reading scenes file: {e}[/]")
        return None

    if not isinstance(scenes, list) or not scenes:
        console.print("  [red]Scenes file must be a JSON array of scene objects.[/]")
        return None

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        frame_count = 0
        frames_per_scene = int(fps * duration_per_scene)

        for scene in scenes:
            text = scene.get("text", "")
            bg = tuple(scene.get("bg_color", [6, 6, 8]))
            fg = tuple(scene.get("text_color", [0, 245, 212]))

            for f in range(frames_per_scene):
                img = Image.new("RGB", (width, height), bg)
                draw = ImageDraw.Draw(img)
                _draw_centered_text(draw, text, width, height, fg, size_ratio=0.04)
                frame_path = Path(tmpdir) / f"frame_{frame_count:06d}.png"
                img.save(str(frame_path))
                frame_count += 1

        # Encode with FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", str(Path(tmpdir) / "frame_%06d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "23",
            str(output_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"  [red]FFmpeg error: {result.stderr[:200]}[/]")
            return None

    console.print(f"  [green]Saved:[/] {output_path} ({frame_count} frames, {fps}fps)")
    return output_path
