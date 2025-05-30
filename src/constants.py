PATTERN_COLORS = [
    "00FF88",  # Neon Green
    "FFA500",  # Vivid Orange
    "00CFFF",  # Electric Cyan
    "FF5C5C",  # Bright Red
    "FFD700",  # Yellow-Gold
    "A75CFF",  # Purple
    "33FF57",  # Lime Green
    "66B2FF",  # Sky Blue
    "FF66CC",  # Hot Pink
    "80FF00",  # Chartreuse
    "FFAA33",  # Apricot
    "FF4444",  # Strawberry Red
    "33DDFF",  # Cyan-Teal
    "FFB3FF",  # Light Magenta
    "FFCC00",  # Warm Yellow
    "99FF99",  # Soft Lime
    "66FFFF",  # Ice Blue
    "CC66FF",  # Orchid Purple
    "FF9999",  # Light Red
    "00FFFC"   # Neon Aqua
]

ACTIVE_COLOR = "#3B71D9"
ACCENT_COLOR = "#67A4FF"
GRACE_COLOR = "#C483E5"
SECONDARY_COLOR = "#CCCCCC"
WINDOW_BORDER_COLOR = "#2F3137"
BG_DARKEST = "#191B1F"
BG_DARK = "#232629"
BG_INPUT = "#1F2225"
BG_GRAY = "#292A2F"
GRAY_SOFT = "#ADAFB7"
BORDER_COLOR = "#000000"
BORDER_COLOR_LIGHT = "#2E2D2D"
BORDER_COLOR_LIGHTER = "#5E6165"

def get_color(index: int) -> str:
    """Get color or loop back to start of list."""
    if index < len(PATTERN_COLORS):
        return PATTERN_COLORS[index]
    else:
        return PATTERN_COLORS[index % len(PATTERN_COLORS)]
