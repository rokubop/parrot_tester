PATTERN_COLORS = [
    "#00FF88",
    "#FFA500",
    "#00CFFF",
    "#FF5C5C",
    "#FFD700",
    "#A75CFF",
    "#33FF57",
    "#66B2FF",
    "#FF66CC",
    "#80FF00",
    "#FFAA33",
    "#FF4444",
    "#33DDFF",
    "#FFB3FF",
    "#FFCC00",
    "#99FF99",
    "#66FFFF",
    "#CC66FF",
    "#FF9999",
    "#00FFFC"
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
PLAY_COLOR = "#13A126"
DETECTED_COLOR = "#73BF69"
THROTTLE_COLOR = "#FFCC00"

def get_color(index: int) -> str:
    """Get color or loop back to start of list."""
    if index < len(PATTERN_COLORS):
        return PATTERN_COLORS[index]
    else:
        return PATTERN_COLORS[index % len(PATTERN_COLORS)]
