from talon import actions
from ..core import (
    get_pattern_json,
    get_pattern_color,
)
from ..constants import (
    ACTIVE_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
    GRACE_COLOR,
)

def legend():
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])

    return div(flex_direction="row", gap=32, align_items="flex_end", padding=16, border_width=1, background_color="#292A2F", border_color=BORDER_COLOR)[
        div(flex_direction="row", gap=8, align_items="center")[
            text("Detected"),
            icon("check", size=14, color="73BF69", stroke_width=3),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Throttled"),
            icon("clock", size=14, color="FFCC00"),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Grace detected"),
            tilda_icon(),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Not detected"),
            text("-", color="999999"),
        ],
    ]

def rect_color(color, size=20, **props):
    div = actions.user.ui_elements("div")
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return div(**props)[
        svg(size=size)[
            rect(x=0, y=0, width=24, height=24, fill=color)
        ]
    ]

def number(value, **kwargs):
    text = actions.user.ui_elements("text", **kwargs)
    return text(value, font_family="consolas")

def status_cell(status: str, graceperiod: bool = False):
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])
    svg, circle = actions.user.ui_elements_svg(["svg", "circle"])

    s = None

    if status =="grace_detected":
        s = tilda_icon()
        # s = div(position="relative")[
        #     icon("check", size=16, color="#73BF69", stroke_width=3),
        #     div(position="absolute", right="100%", height="100%")[
        #         tilda_icon(),
        #         # svg(size=16)[
        #         #     circle(cx=12, cy=12, r=4, fill="#48CEFF"),
        #         # ]
        #     ]
        # ]
    elif status == "detected":
        s = icon("check", size=16, color="#73BF69", stroke_width=3)
    elif status == "throttled":
        s = icon("clock", size=16, color="#FFCC00")
    return s if s else text("-", color="#999999")

def power_ratio_bar(power: float, patterns: list, power_threshold: float = None):
    div = actions.user.ui_elements("div")
    power_percent = min(30, power) / 30
    power_threshold_percent = min(30, power_threshold) / 30 if power_threshold else 0
    full_bar_width = 150
    bar_width = int(full_bar_width * power_percent)
    power_threshold_left = int(power_threshold_percent * full_bar_width) if power_threshold else None

    return div(position="relative", flex_direction="row", width=bar_width, background_color="555555", height=9)[
        *[div(width=int(pattern["probability"] * bar_width), background_color=pattern["color"]) for pattern in patterns],
        div(position="absolute", left=power_threshold_left - 1.5, width=1.5, top=0, bottom=0, background_color="191B1FCC") if power_threshold else None,
    ]

def table_controls():
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    state = actions.user.ui_elements("state")

    return div(flex_direction="row", gap=16)[
        # button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, border_color=BORDER_COLOR, border_width=2, border_radius=4)[
        #     text("Capture time"),
        #     icon("chevron_down", size=14),
        # ],
        # button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, border_color=BORDER_COLOR, border_width=2, border_radius=4)[
        #     text("Filters"),
        #     icon("chevron_down", size=14),
        # ],
        button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, background_color="#292A2F", border_color=BORDER_COLOR, border_width=1, border_radius=4)[
            text("Columns"),
            icon("chevron_down", size=14),
        ],
    ]

def tilda_icon():
    svg, path = actions.user.ui_elements_svg(["svg", "path"])
    return svg(size=14, stroke=GRACE_COLOR, stroke_width=4)[
        path(d="M4 14 Q8 10, 12 14 T20 14")
    ]

def pattern(props):
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
    table, tr, td, style = actions.user.ui_elements(["table", "tr", "td", "style"])

    pattern_name = props["name"]
    highlight_when_active = props.get("highlight_when_active", False)

    pattern_data = get_pattern_json(pattern_name)
    pattern_color = get_pattern_color(pattern_name)

    style({
        "th": {
            "padding": 5,
            "padding_right": 7,
            "flex_direction": "row",
            "align_items": "center",
        },
        "td": {
            "padding": 5,
            "padding_right": 7,
            "flex_direction": "row",
            "align_items": "center",
        },
    })

    throttle_items = list(pattern_data.get("throttle", {}).items())
    throttle_groups = [throttle_items[i:i + 2] for i in range(0, len(throttle_items), 2)]
    grace_threshold_items = list(pattern_data.get("grace_threshold", {}).items())
    grace_threshold_groups = [grace_threshold_items[i:i + 2] for i in range(0, len(grace_threshold_items), 2)]

    pattern_props = {
        "padding": 16,
        "flex_direction": "column",
        "gap": 8,
        "border_bottom": 1,
        "border_color": BORDER_COLOR,
    }

    if highlight_when_active:
        pattern_props["id"] = f"pattern_{pattern_name}"

    return div(pattern_props)[
        div(flex_direction="row", gap=8, align_items="center", padding_bottom=8, justify_content="space_between")[
            div(flex_direction="row", gap=8, align_items="center")[
                rect_color(pattern_color, size=14),
                text(pattern_name, font_size=20),
            ],
            button(on_click=lambda e: state.set("edit_pattern", pattern_name))[
                icon("edit", size=16, color=ACCENT_COLOR, stroke_width=3),
            ]
        ],
        div(justify_content="center", align_items="flex_start")[
            div(flex_direction="row", gap=8, margin_left=15, align_items="center")[
                text("sounds", font_size=14, color=ACCENT_COLOR),
                text(",".join(pattern_data.get("sounds", [])), font_size=14),
            ],
            table(padding=8, padding_bottom=0)[
                tr()[
                    td(position="relative")[
                        text(">power", font_size=14, color=ACCENT_COLOR),
                    ],
                    td(margin_right=16, position="relative")[
                        number(pattern_data.get("threshold", {}).get(">power", "0")),
                    ],
                    td()[text(">probability", font_size=14, color=ACCENT_COLOR)],
                    td(margin_right=16)[number(pattern_data.get("threshold", {}).get(">probability", "0"))],
                ],
                *[
                    tr()[
                        *[
                            item
                            for k, v in group
                            for item in [
                                td()[
                                    div(flex_direction="row", gap=4, align_items="center")[
                                        icon("clock", size=14, color="FFCC00"),
                                        text(k, font_size=14, color=ACCENT_COLOR),
                                    ]
                                ],
                                td(margin_right=16)[number(v)],
                            ]
                        ]
                    ]
                    for group in throttle_groups
                ]
            ],
            div(flex_direction="row", gap=8, margin_left=15, align_items="center", margin_top=8)[
                text("graceperiod", font_size=14, color=GRACE_COLOR),
                number(pattern_data.get("graceperiod", "")),
            ] if pattern_data.get("graceperiod", None) else None,
            table(padding=8, padding_bottom=0)[
                *[
                    tr()[
                        *[
                            item
                            for k, v in group
                            for item in [
                                td()[
                                    div(flex_direction="row", gap=4, align_items="center")[
                                        text(k, font_size=14, color=GRACE_COLOR),
                                    ]
                                ],
                                td(margin_right=16)[number(v)],
                            ]
                        ]
                    ]
                    for group in grace_threshold_groups
                ]
            ] if grace_threshold_groups else None,
        ]
    ]

def removable_pill(name):
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])

    return div(flex_direction="row", border_width=1, border_color="555555", background_color=f"55555533", padding=4, border_radius=4)[
        text(name, font_size=14),
        icon("close", size=14, color="555555", stroke_width=3, margin_left=8),
    ]

def pattern_pill(name):
    div, text = actions.user.ui_elements(["div", "text"])

    if name in get_pattern_json():
        pattern_color = get_pattern_color(name)
    else:
        pattern_color = "555555"
    return div(border_width=1, border_color=pattern_color, background_color=f"{pattern_color}33", padding=4, border_radius=4)[
        text(f"+ {name}", font_size=14)
    ]