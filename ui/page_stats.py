from talon import actions, clip, cron
from .components import (
    legend,
    number,
    status_cell,
    power_ratio_bar,
    table_controls,
    subtitle,
    rect_color,
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
    update_stats_state,
    get_stats_pretty_print,
    format,
    get_pattern_color,
    format_stats_multiline,
)
#60A5FA
#A1A1AA
#F87171
def icon_triangle_up():
    svg, path = actions.user.ui_elements_svg(["svg", "path"])

    return svg(size=10)[
        path(
            d="M3 20h18L12 4z",
            fill="#60A5FA",
        )
    ]

def icon_diamond():
    svg, path = actions.user.ui_elements_svg(["svg", "path"])

    return svg(size=10)[
        path(
            d="M12 2l10 10-10 10-10-10z",
            fill="#A1A1AA",
        )
    ]

def icon_triangle_down():
    svg, path = actions.user.ui_elements_svg(["svg", "path"])

    return svg(size=10)[
        path(
            d="M3 4h18L12 20z",
            fill="#F87171",
        )
    ]

def legend():
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])

    return div(flex_direction="row", gap=32, padding=8, align_items="flex_end")[
        div(flex_direction="row", gap=8, align_items="center")[
            text("Minimum"),
            icon_triangle_down(),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Average"),
            icon_diamond(),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Maximum"),
            icon_triangle_up(),
        ],
    ]

def stats_triplet(stat, decimal_places=2):
    div = actions.user.ui_elements(["div"])

    return div(gap=10)[
        div(flex_direction="row", align_items="center", gap=4)[
            icon_triangle_down(),
            number(format(stat["min"], decimal_places)),
        ],
        div(flex_direction="row", align_items="center", gap=4)[
            icon_diamond(),
            number(format(stat["average"], decimal_places)),
        ],
        div(flex_direction="row", align_items="center", gap=4)[
            icon_triangle_up(),
            number(format(stat["max"], decimal_places)),
        ],
    ]

def copy_button(name):
    button, icon, state = actions.user.ui_elements(["button", "icon", "state"])

    copied, set_copied = state.use_local("copied", False)

    def copy_to_clipboard(name):
        clip.set_text(get_stats_pretty_print(name))
        set_copied(True)
        try:
            cron.after("2s", lambda: set_copied(False))
        except Exception as e:
            pass

    return button(on_click=lambda: copy_to_clipboard(name), disabled=copied, padding=8, border_radius=8)[
        icon(
            "check" if copied else "copy",
            size=20,
            color="#28EB66" if copied else SECONDARY_COLOR
        ),
    ]

def table_stats():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])
    state, button, effect, component = actions.user.ui_elements(["state", "button", "effect", "component"])
    stats = state.get("patterns_stats", {})
    copied, set_copied = state.use("copied", {})
    stats_list = list(stats.values()) if isinstance(stats, dict) else stats or []
    stats_list_groups = [stats_list]

    # Break stats into two groups if there are more than 10 items
    if len(stats_list) > 10:
        mid = (len(stats_list) + 1) // 2
        stats_list_groups = [stats_list[:mid], stats_list[mid:]]

    def on_mount(e):
        update_stats_state()

    effect(on_mount, [])

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

    return div(height="100%")[
        div(background_color=BG_DARK, border_color=BORDER_COLOR, border_bottom=1)[
            div(flex_direction="row", padding=8, justify_content="space_between", align_items="center")[
                text("Statistics", font_size=16, margin_left=8),
                component(table_controls),
            ],
        ],
        div(flex_direction="row", height="100%", overflow_y="scroll", position="relative")[
            *[table(padding=16, padding_top=0)[
                tr()[
                    th(align_items="flex_end")[text("Pattern - Count", color=SECONDARY_COLOR)],
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
                    th(align_items="center")[text("Copy", color=SECONDARY_COLOR)],
                ],
                *[
                    tr()[
                        td(align_items="flex_start", justify_content="center")[
                            div(gap=8, flex_direction="row")[
                                rect_color(get_pattern_color(pattern_stats["name"]), size=10),
                                text(pattern_stats["name"]),
                                text("-"),
                                number(str(pattern_stats["count"]))
                            ]
                        ],
                        td(align_items="flex_end")[stats_triplet(pattern_stats["power"], 2)],
                        td(align_items="flex_end")[div(gap=10)[
                            number(format(pattern_stats["probability"]["min"], 4)),
                            number(format(pattern_stats["probability"]["average"], 4)),
                            number(format(pattern_stats["probability"]["max"], 4)),
                        ]],
                        td(align_items="flex_end", justify_content="center")[div(gap=10)[
                            number(str(round(pattern_stats["f0"]["min"]))),
                            number(str(round(pattern_stats["f0"]["average"]))),
                            number(str(round(pattern_stats["f0"]["max"]))),
                        ]],
                        td(align_items="flex_end", justify_content="center")[div(gap=10)[
                            number(str(round(pattern_stats["f1"]["min"]))),
                            number(str(round(pattern_stats["f1"]["average"]))),
                            number(str(round(pattern_stats["f1"]["max"]))),
                        ]],
                        td(align_items="flex_end", justify_content="center")[div(gap=10)[
                            number(str(round(pattern_stats["f2"]["min"]))),
                            number(str(round(pattern_stats["f2"]["average"]))),
                            number(str(round(pattern_stats["f2"]["max"]))),
                        ]],
                        td(align_items="center", justify_content="center")[
                            component(copy_button, pattern_stats["name"]),
                        ]
                    ] for pattern_stats in stats_list
                ]
            ] for stats_list in stats_list_groups],
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
        ]
    ]

def page_stats():
    div, component, text, state, button = actions.user.ui_elements(
        ["div", "component", "text", "state", "button"]
    )
    effect = actions.user.ui_elements("effect")

    def on_mount(e):
        init_stats()

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