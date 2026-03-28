# Render-Kit

**Product photos + social media from the command line.**

Free (PIL) or $0.01/image (Flux AI). No design skills needed.

```bash
$ render-kit product "leather journal" --preset dark_luxury
```

> Built by NOUMENON — AI agents that debate, evolve, and build.

![PyPI](https://img.shields.io/pypi/v/render-kit)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## Why This Exists

Professional product photography costs $500+.
Every Shopify and Etsy seller needs product photos.
This tool generates them for free (PIL) or $0.01 each (Flux AI via Replicate).

## Install

```bash
pip install render-kit

# Optional: AI-powered generation
pip install render-kit[ai]

# Optional: Text-to-speech
pip install render-kit[voice]
```

## Usage

### Product Photography

```bash
# Single preset
render-kit product "leather journal" --preset dark_luxury

# All 5 presets at once
render-kit product "leather journal" --all-presets

# Available presets: white_studio, lifestyle, dark_luxury, flat_lay, heritage
```

### Social Media

```bash
# Instagram square
render-kit social "NOUMENON — AI that debates before it builds" --template ig_square

# Instagram carousel (4 slides)
render-kit social "Launch Day" --template ig_carousel --slides 4

# Twitter/X header
render-kit social "New Release" --template twitter

# YouTube thumbnail
render-kit social "How I Built This" --template youtube_thumb
```

### Video

```bash
render-kit video --scenes scenes.json --fps 30
```

### Voiceover

```bash
render-kit voice "Welcome to our product" --output voiceover.wav
```

### Batch Processing

```bash
render-kit batch products.csv --preset lifestyle
```

CSV format:
```csv
name,preset
Leather Journal,dark_luxury
Canvas Bag,heritage
Coffee Mug,white_studio
```

## Presets

| Preset | Background | Style |
|--------|-----------|-------|
| white_studio | Pure white | Studio lighting, clean |
| lifestyle | Warm wood | Editorial, bokeh |
| dark_luxury | Dark | Dramatic rim lighting |
| flat_lay | Off-white | Top-down, styled |
| heritage | Dark amber | Artisan, aged wood |

## Social Templates

| Template | Size | Use Case |
|----------|------|----------|
| ig_square | 1080x1080 | Instagram feed |
| ig_story | 1080x1920 | Instagram/TikTok story |
| ig_carousel | 1080x1080 | Multi-slide carousel |
| twitter | 1200x675 | Twitter/X post |
| og | 1200x630 | Open Graph / link preview |
| youtube_thumb | 1280x720 | YouTube thumbnail |

## Engines

- **PIL (default)** — Free, offline, generates styled placeholders
- **Replicate (optional)** — $0.01/image, photorealistic via Flux AI

Set `REPLICATE_API_TOKEN` to enable AI generation:
```bash
export REPLICATE_API_TOKEN=r8_your_token_here
```

## License

MIT

---

Part of the NOUMENON ecosystem.
