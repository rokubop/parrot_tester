from talon import actions
from ..components import (
    legend,
    number,
    status_cell,
    power_ratio_bar,
    table_controls,
    pattern
)
from ...constants import (
    SECONDARY_COLOR,
    BORDER_COLOR,
)

def detected_patterns():
    div, component, state, text = actions.user.ui_elements(["div", "component", "state", "text"])
    state = actions.user.ui_elements("state")
    last_capture = state.get("last_capture", None)
    frames = last_capture.detect_frames if last_capture else []
    patterns = []
    seen = set()

    for frame in frames:
        for p in frame.patterns:
            name = p["name"]
            if name not in seen:
                patterns.append(name)
                seen.add(name)

    return div(height="100%")[
        text("Detected patterns", padding=16, font_size=20, border_bottom=1, border_color=BORDER_COLOR, min_width=320),
        div(flex_direction="column", overflow_y="scroll", height="100%")[
            *[div()[
                component(pattern, props={
                    "name": pattern_name,
                    "highlight_when_active": False,
                })
            ] for pattern_name in patterns]
        ],
    ]

def table_frames():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])
    state = actions.user.ui_elements("state")
    last_capture = state.get("last_capture", None)
    frames = last_capture.frames if last_capture else []

    style({
        "th": {
            "padding": 10,
            "padding_left": 12,
            "padding_right": 12,
            "align_items": "flex_start",
            "border_bottom": 1,
        },
        "td": {
            "padding": 8,
            "padding_left": 12,
            "padding_right": 12,
            "align_items": "flex_end",
            "border_bottom": 1,
        },
    })

    return table(height="100%", overflow_y="scroll", padding=16, padding_top=0)[
        tr()[
            th(align_items="flex_end")[text("Frame", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[div(flex_direction="row", gap=2, align_items="center")[
                icon("delta", size=11, stroke_width=3, color=SECONDARY_COLOR),
                text("ts", color=SECONDARY_COLOR),
            ]],
            th()[text("Pattern", color=SECONDARY_COLOR)],
            # th()[text("Sounds", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[text("Power", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[text("Prob.", color=SECONDARY_COLOR)],
            th(align_items="center")[text("Status", color=SECONDARY_COLOR)],
            th(align_items="flex_start")[div(flex_direction="row", gap=2)[
                text("Power", color=SECONDARY_COLOR),
                icon("multiply", size=11, stroke_width=3, color=SECONDARY_COLOR),
                text("Prob.", color=SECONDARY_COLOR),
            ]],
        ],
        *[
            tr()[
                td()[number(str(frame.id))],
                td()[number(frame.format(frame.ts_delta, 3))],
                td(align_items="flex_start")[div(gap=8, min_width=60)[
                    *[text(p["name"]) for p in frame.patterns]
                ]],
                # td(align_items="flex_start")[div(gap=8)[
                #     *[text(", ".join(p["sounds"])) for p in frame.patterns]
                # ]],
                td()[number(frame.format(frame.power, 2))],
                td(align_items="flex_end")[div(gap=8)[
                    *[number(frame.format(p["probability"], 4)) for p in frame.patterns]
                ]],
                td(align_items="center")[div(gap=8, align_items="center")[
                    *[status_cell(p['status'], p['graceperiod']) for p in frame.patterns]
                ]],
                td(align_items="flex_start", justify_content="center")[
                    power_ratio_bar(
                        frame.power,
                        frame.patterns,
                        frame.winner_grace_power_threshold if frame.grace_detected else \
                            frame.winner_power_threshold if frame.detected else None
                    )
                ],
            ] for frame in frames
        ],
    ]

def page_frames():
    div, component, text = actions.user.ui_elements(["div", "component", "text"])

    state = actions.user.ui_elements("state")
    capture_updating = state.get("capture_updating", False)

    return div(background_color="191B1F", flex_direction="row", height=750)[
        div(flex_direction="column", background_color="#292A2F", gap=16, height=750, border_right=1, border_color=BORDER_COLOR)[
            detected_patterns(),
        ],
        div(flex_direction="column", gap=16, flex=1)[
            div(position="relative", flex=1)[
                div(flex_direction="row", padding=16, justify_content="space_between", align_items="center")[
                    text("Frames", font_size=24),
                    legend(),
                    table_controls(),
                ],
                component(table_frames),
                div(position="absolute", top=0, right=0)[
                    text("Updating...", font_size=14, padding=2)
                ] if capture_updating else None,
            ],
        ],
    ]