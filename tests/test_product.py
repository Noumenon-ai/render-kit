"""Tests for product image generation."""

from pathlib import Path

from render_kit.engines.pil import generate_product_image, generate_social_image
from render_kit.presets import PRODUCT_PRESETS, SOCIAL_TEMPLATES


def test_pil_product_image(tmp_path):
    out = tmp_path / "test.png"
    img = generate_product_image(
        "Test Product",
        bg_color=(255, 255, 255),
        text_color=(30, 30, 30),
        output_path=out,
    )
    assert img.size == (1024, 1024)
    assert out.exists()


def test_pil_social_image(tmp_path):
    out = tmp_path / "social.png"
    img = generate_social_image(
        "Hello World",
        width=1080,
        height=1080,
        output_path=out,
    )
    assert img.size == (1080, 1080)
    assert out.exists()


def test_all_presets_have_required_keys():
    for name, preset in PRODUCT_PRESETS.items():
        assert "prompt_suffix" in preset, f"{name} missing prompt_suffix"
        assert "bg_color" in preset, f"{name} missing bg_color"
        assert "text_color" in preset, f"{name} missing text_color"


def test_all_templates_have_required_keys():
    for name, tmpl in SOCIAL_TEMPLATES.items():
        assert "width" in tmpl, f"{name} missing width"
        assert "height" in tmpl, f"{name} missing height"
