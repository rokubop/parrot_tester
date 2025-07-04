from talon import actions
from .components import (
    legend,
    number,
    status_cell,
    power_ratio_bar,
    table_controls,
    pattern,
    subtitle,
)
from .colors import (
    SECONDARY_COLOR,
    BORDER_COLOR,
    BORDER_COLOR_LIGHTER,
    GRAY_SOFT,
    BG_GRAY,
    BG_DARKEST,
    BG_DARK,
)

def detected_patterns():
    div, component, state, text = actions.user.ui_elements(["div", "component", "state", "text"])
    state = actions.user.ui_elements("state")
    last_capture = state.get("last_capture", None)
    patterns = last_capture.detected_pattern_names if last_capture else []
    other_patterns = last_capture.other_pattern_names if last_capture else []

    return div(height="100%")[
        subtitle("Detected patterns"),
        div(flex_direction="column", overflow_y="scroll", height="100%")[
            *[div()[
                component(pattern, props={
                    "name": pattern_name,
                    "highlight_when_active": False,
                })
            ] for pattern_name in patterns],
            subtitle("Other patterns") if other_patterns else None,
            *[div()[
                component(pattern, props={
                    "name": pattern_name,
                    "highlight_when_active": False,
                    "show_throttles": False,
                    "show_grace": False,
                    "small": True,
                    "edit": False,
                }),
            ] for pattern_name in other_patterns]
        ],
    ]

def table_frames():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])
    state = actions.user.ui_elements("state")
    last_capture = state.get("last_capture", None)
    frames = last_capture.frames if last_capture else []
    show_formants = state.get("show_formants", False)

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
            "justify_content": "center",
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
            *[
                th(align_items="flex_end", justify_content="center")[
                    text("F0", color=SECONDARY_COLOR),
                ],
                th(align_items="flex_end", justify_content="center")[
                    text("F1", color=SECONDARY_COLOR),
                ],
                th(align_items="flex_end", justify_content="center")[
                    text("F2", color=SECONDARY_COLOR),
                ],
            ] if show_formants else [],
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
                td(align_items="flex_start")[div(gap=10, min_width=60)[
                    *[text(p["name"]) for p in frame.patterns]
                ]],
                # td(align_items="flex_start")[div(gap=8)[
                #     *[text(", ".join(p["sounds"])) for p in frame.patterns]
                # ]],
                td()[number(frame.format(frame.power, 2))],
                td(align_items="flex_end")[div(gap=10)[
                    *[number(frame.format(p["probability"], 4)) for p in frame.patterns]
                ]],
                *[
                    td(align_items="flex_end", justify_content="center")[
                        number(str(round(frame.f0))),
                    ],
                    td(align_items="flex_end", justify_content="center")[
                        number(str(round(frame.f1))),
                    ],
                    td(align_items="flex_end", justify_content="center")[
                        number(str(round(frame.f2))),
                    ],
                ] if show_formants else [],
                td(align_items="center")[div(gap=10, align_items="center")[
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

    return div()[
        div(background_color=BG_DARKEST, flex_direction="row", height=750)[
            div(flex_direction="column", background_color=BG_GRAY, gap=16, height=750, border_right=1, border_color=BORDER_COLOR)[
                detected_patterns(),
            ],
            div(flex_direction="column", gap=16, flex=1)[
                div(flex=1, position="relative")[
                    div(background_color=BG_DARK, border_color=BORDER_COLOR, border_bottom=1)[
                        div(flex_direction="row", padding=8, justify_content="space_between", align_items="center")[
                            text("Frames", font_size=16),
                            component(table_controls),
                        ],
                    ],
                    div(position="relative", flex=1)[
                        component(table_frames),
                        div(position="absolute", top=0, right=0)[
                            text("Updating...", font_size=14, padding=2)
                        ] if capture_updating else None,
                    ],
                    div(
                        position="absolute",
                        bottom=0,
                        right=0,
                        flex_direction="row",
                        justify_content="flex_end",
                        background_color=BG_DARK,
                    )[
                        legend(),
                    ],
                ],
            ],
        ]
    ]