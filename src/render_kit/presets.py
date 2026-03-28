"""Preset definitions for product photography and social media templates."""

PRODUCT_PRESETS = {
    "white_studio": {
        "prompt_suffix": "product photography, pure white background, studio lighting, 8k",
        "bg_color": (255, 255, 255),
        "text_color": (30, 30, 30),
    },
    "lifestyle": {
        "prompt_suffix": "lifestyle product photo, warm wood surface, bokeh, editorial",
        "bg_color": (245, 235, 220),
        "text_color": (60, 40, 20),
    },
    "dark_luxury": {
        "prompt_suffix": "luxury product photo, dark background, dramatic rim lighting",
        "bg_color": (15, 15, 20),
        "text_color": (240, 240, 240),
    },
    "flat_lay": {
        "prompt_suffix": "flat lay product photo, top-down, styled props, instagram",
        "bg_color": (250, 248, 245),
        "text_color": (40, 40, 40),
    },
    "heritage": {
        "prompt_suffix": "artisan handcrafted photo, warm amber, aged wood, shallow DOF",
        "bg_color": (45, 30, 20),
        "text_color": (230, 210, 180),
    },
}

SOCIAL_TEMPLATES = {
    "ig_square": {"width": 1080, "height": 1080, "multi": False},
    "ig_story": {"width": 1080, "height": 1920, "multi": False},
    "ig_carousel": {"width": 1080, "height": 1080, "multi": True},
    "twitter": {"width": 1200, "height": 675, "multi": False},
    "og": {"width": 1200, "height": 630, "multi": False},
    "youtube_thumb": {"width": 1280, "height": 720, "multi": False},
}

ALL_PRESET_NAMES = list(PRODUCT_PRESETS.keys())
ALL_TEMPLATE_NAMES = list(SOCIAL_TEMPLATES.keys())
