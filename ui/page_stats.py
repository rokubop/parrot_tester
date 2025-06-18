from talon import actions
from .components import (
    legend,
    number,
    status_cell,
    power_ratio_bar,
    table_controls,
    subtitle,
)
from .colors import (
    SECONDARY_COLOR,
    BORDER_COLOR,
    BG_DARKEST,
    BG_DARK,
    ACTIVE_COLOR,
    BG_GRAY,
)
from ..parrot_integration_wrapper import (
    get_pattern_threshold_value,
    init_stats,
    reset_stats,
    add_frame_to_stats,
    get_stats,
    set_detection_log_state_by_id,
)

def table_stats():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])
    state = actions.user.ui_elements(["state"])
    stats = state.get("patterns_stats", {})

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
            th(align_items="flex_end")[text("Pattern", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[text("Power", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[text("Prob.", color=SECONDARY_COLOR)],
            th(align_items="flex_end", justify_content="center")[
                text("F0", color=SECONDARY_COLOR),
            ],
            th(align_items="flex_end", justify_content="center")[
                text("F1", color=SECONDARY_COLOR),
            ],
            th(align_items="flex_end", justify_content="center")[
                text("F2", color=SECONDARY_COLOR),
            ],
        ],
        *[
            tr(id=f"pattern_{pattern_stats['name']}")[
                td(align_items="flex_start")[div(gap=8, min_width=60)[
                    text(pattern_stats["name"])
                ]],
                td(align_items="flex_end")[number(pattern_stats["power"]["average"])],
                td(align_items="flex_end")[number(pattern_stats["probability"]["average"])],
                td(align_items="flex_end", justify_content="center")[
                    number(str(round(pattern_stats["f0"]["average"]))),
                ],
                td(align_items="flex_end", justify_content="center")[
                    number(str(round(pattern_stats["f1"]["average"]))),
                ],
                td(align_items="flex_end", justify_content="center")[
                    number(str(round(pattern_stats["f2"]["average"]))),
                ],
            ] for pattern_stats in stats
        ],
    ]

def page_stats():
    div, component, text, state, button = actions.user.ui_elements(
        ["div", "component", "text", "state", "button"]
    )
    effect = actions.user.ui_elements("effect")

    def on_mount(e):
        init_stats()
        # print(f"Stats on mount: {s}")
        # state.set("patterns_stats", s)

    effect(on_mount, [])

    return div(background_color=BG_DARKEST, flex_direction="row", height=750)[
        div(flex_direction="column", gap=16, flex=1)[
            div(position="relative", flex=1)[
                div(position="relative", flex=1)[
                    component(table_stats),
                ],
            ],
        ],
    ]