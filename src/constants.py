#00FF88 – Neon Green

#FFA500 – Vivid Orange

#00CFFF – Electric Cyan

# Tier 2 (distinct hues, still vibrant):
#FF5C5C – Bright Red

#FFD700 – Yellow-Gold

#A75CFF – Purple

#33FF57 – Lime Green

#66B2FF – Sky Blue

# Tier 3 (still decent contrast, watch for neighbors):
#FF66CC – Hot Pink

#80FF00 – Chartreuse

#FFAA33 – Apricot

#FF4444 – Strawberry Red

#33DDFF – Cyan-Teal

#FFB3FF – Light Magenta

#FFCC00 – Warm Yellow

#99FF99 – Soft Lime

#66FFFF – Ice Blue

#CC66FF – Orchid Purple

#FF9999 – Light Red

#00FFFC – Neon Aqua

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

# PATTERN_COLORS = [
#     "00FF88",  # Bright Mint
#     "FFA500",  # Vivid Orange
#     "00CFFF",  # Electric Cyan
#     "FF5C5C",  # Bright Red
#     "FFD700",  # Bright Gold
#     "A75CFF",  # Vibrant Purple
#     "00FFFC",  # Aqua Neon
#     "FF66CC",  # Hot Pink
#     "33FF57",  # Lime
#     "66B2FF",  # Sky Blue
#     "FFAA33",  # Apricot
#     "FF4444",  # Strawberry
#     "FFB3FF",  # Light Magenta
#     "80FF00",  # Chartreuse
#     "33DDFF",  # Soft Electric Blue
#     "FF99CC",  # Cotton Candy
#     "99FF99",  # Light Lime
#     "FFCC00",  # Amber
#     "CC66FF",  # Orchid
#     "66FFFF",  # Ice Blue
# ]

# PATTERN_COLORS = [
#     "7EB26D",  # Lush Green
#     "EAB839",  # Bright Orange
#     "6ED0E0",  # Vivid Cyan
#     "EF843C",  # Strong Orange-Red
#     "E24D42",  # Fire Red
#     "1F78C1",  # Bold Blue
#     "BA43A9",  # Deep Purple
#     "705DA0",  # Grape
#     "CCA300",  # Warm Gold
#     "447EBC",  # Sky Blue
#     "C15C17",  # Rust Orange
#     "890F02",  # Blood Red
#     "0A437C",  # Navy
#     "6D1F62",  # Dark Plum
#     "584477",  # Dusty Purple
#     "86B4D3",  # Steel Blue
#     "FF9248",  # Pop Orange
#     "93C47D",  # Mellow Green
#     "9B59B6",  # Soft Violet
#     "2980B9",  # Deep Sea Blue
# ]

# PATTERN_COLORS = [
#     "7EB26D",
#     "EAB839",
#     "6ED0E0",
#     "EF843C",
#     "E24D42",
#     "1F78C1",
#     "BA43A9",
#     "705DA0",
#     "CCA300",
#     "447EBC",
#     "C15C17",
#     "890F02",
#     "0A437C",
#     "6D1F62",
#     "584477",
#     "B7DBAB",
#     "F4D598",
#     "70DBED",
#     "F9BA8F",
#     "73A8D3",
# ]

def get_color(index: int) -> str:
    """Get color or loop back to start of list."""
    if index < len(PATTERN_COLORS):
        return PATTERN_COLORS[index]
    else:
        return PATTERN_COLORS[index % len(PATTERN_COLORS)]
