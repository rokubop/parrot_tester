from talon import actions
from ..core import (
    get_pattern_json,
    get_pattern_color,
)
from ..constants import (
    ACTIVE_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
)

def play_button():
    text, icon, button, state = actions.user.ui_elements(["text", "icon", "button", "state"])
    play, set_play = state.use("play", False)
    play_bg_color = "#191B1F"

    def toggle_play(e):
        set_play(not play)

    if play:
        return button(on_click=toggle_play, align_items="center", gap=16, padding=12, padding_left=24, padding_right=28, flex_direction="row", border_width=1, margin_right=16, border_color="333333", border_radius=16)[
            icon("stop", color="#C6053D"),
            text("Stop listening"),
        ]
    else:
        return button(on_click=toggle_play, autofocus=True, align_items="center", gap=16, padding=12, padding_left=24, padding_right=28, flex_direction="row", border_width=1, margin_right=16, border_color="333333", border_radius=16)[
            icon("play", fill=play_bg_color),
            text("Start listening"),
        ]

tab_id_to_label = {
    "frames": "Frames",
    "about": "About",
}

def tabs(props):
    div, button, text, state = actions.user.ui_elements(["div", "button", "text", "state"])
    tab_state, set_tab = state.use("tab", props["start_tab"])

    return div(flex_direction="row")[
        *[button(on_click=lambda e, id=tab_id: set_tab(id), padding=16, position="relative")[
            text(label, font_size=16, color="FFFFFF"),
            div(
                position="absolute",
                bottom=0,
                background_color=ACTIVE_COLOR,
                height=3,
                width="100%",
                border_radius=2
            ) if tab_state == tab_id else None
        ] for tab_id, label in tab_id_to_label.items()]
    ]

def legend():
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])

    return div(flex_direction="row", gap=32, align_items="flex_end")[
        div(flex_direction="row", gap=8, align_items="center")[
            text("Detected"),
            icon("check", size=14, color="73BF69", stroke_width=3),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Throttle"),
            icon("clock", size=14, color="FFCC00"),
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

    s = None

    if status == "detected":
        s = icon("check", size=16, color="73BF69", stroke_width=3)
    if status == "throttled":
        s = icon("clock", size=16, color="FFCC00")
    if s:
        # if graceperiod:
        #     return div(flex_direction="row", gap=4, align_items="center")[
        #         text("~", color="C6053D", font_weight="bold"),
        #         s,
        #     ]
        return s
    return text("-", color="999999")

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

def pattern(props):
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])
    table, tr, td, style = actions.user.ui_elements(["table", "tr", "td", "style"])

    pattern_data = get_pattern_json(props["name"])
    pattern_color = get_pattern_color(props["name"])

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

    throttles = pattern_data.get("throttle", {})
    throttle_items = list(throttles.items())
    throttle_groups = [throttle_items[i:i + 2] for i in range(0, len(throttle_items), 2)]

    return div(id=f"pattern_{props['name']}", padding=16, flex_direction="column", gap=8, width=300, border_bottom=1, border_color=BORDER_COLOR)[
        div(flex_direction="row", gap=8, align_items="center", padding_bottom=8)[
            rect_color(pattern_color, size=14),
            text(props["name"], font_size=20),
        ],
        div(justify_content="center", align_items="center")[
            div()[
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
            ]
        ],
    ]