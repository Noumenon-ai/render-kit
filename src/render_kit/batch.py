"""Batch processing from CSV files."""

from __future__ import annotations

import csv
from pathlib import Path

from rich.console import Console

from render_kit.product import generate_product

console = Console()


class BatchError(Exception):
    """Raised when a batch run cannot be completed."""


def process_batch(
    csv_file: str,
    preset: str = "white_studio",
    output_dir: str = "renders",
) -> list[Path]:
    """Process a CSV file of products. CSV should have at least a 'name' column.

    Raises BatchError if the CSV is missing, empty, or fails to process.
    """
    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise BatchError(f"CSV file not found: {csv_file}")

    results: list[Path] = []

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise BatchError("CSV file is empty or has no headers.")

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

    except BatchError:
        raise
    except Exception as e:
        raise BatchError(f"Error processing CSV: {e}") from e

    return results
