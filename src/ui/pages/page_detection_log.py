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

def table_log():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])
    state, effect = actions.user.ui_elements(["state", "effect"])
    detection_frames = state.get("detection_frames", [])

    def on_mount(e):
        print("Mounting detection log table")

    def on_unmount(e):
        print("Unmounting detection log table")

    effect(on_mount, on_unmount, [])

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
            ] for frame in detection_frames
        ],
    ]

def page_detection_log():
    div, component, text = actions.user.ui_elements(["div", "component", "text"])
    effect = actions.user.ui_elements("effect")

    def on_mount(e):
        print("Mounting detection log page")

    def on_unmount(e):
        print("Unmounting detection log page")

    effect(on_mount, on_unmount, [])

    return div(background_color="191B1F", flex_direction="row", height=750)[
        div(flex_direction="column", gap=16, flex=1)[
            div(position="relative", flex=1)[
                div(flex_direction="row", padding=16, justify_content="space_between", align_items="center")[
                    text("Detection Log", font_size=24),
                    legend(),
                    table_controls(),
                ],
                component(table_log),
            ],
        ],
    ]