"""Batch processing from CSV files."""

from __future__ import annotations

import csv
from pathlib import Path

from rich.console import Console

from render_kit.product import generate_product

console = Console()


def process_batch(
    csv_file: str,
    preset: str = "white_studio",
    output_dir: str = "renders",
) -> list[Path]:
    """Process a CSV file of products. CSV should have at least a 'name' column."""
    csv_path = Path(csv_file)
    if not csv_path.exists():
        console.print(f"  [red]CSV file not found: {csv_file}[/]")
        return []

    results: list[Path] = []

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                console.print("  [red]CSV file is empty or has no headers.[/]")
                return []

            # Find the name column (flexible matching)
            name_col = None
            for col in reader.fieldnames:
                if col.lower().strip() in ("name", "product", "item", "title"):
                    name_col = col
                    break

            if not name_col:
                name_col = reader.fieldnames[0]
                console.print(f"  [dim]Using first column '{name_col}' as product name.[/]")

            items = list(reader)

        console.print(f"  Found [bold]{len(items)}[/] products in {csv_file}")

        for item in items:
            name = item.get(name_col, "").strip()
            if not name:
                continue
            # Use per-item preset if CSV has a 'preset' column
            item_preset = item.get("preset", preset).strip() or preset
            generated = generate_product(name, preset=item_preset, output_dir=output_dir)
            results.extend(generated)

    except Exception as e:
        console.print(f"  [red]Error processing CSV: {e}[/]")

    return results
