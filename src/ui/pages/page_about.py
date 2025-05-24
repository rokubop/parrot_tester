from talon import actions
from ...constants import (
    SECONDARY_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
)

def page_about():
    div, text, table, tr, td, style, icon = actions.user.ui_elements(["div", "text", "table", "tr", "td", "style", "icon"])

    style({
        "td": {
            "padding": 8,
        },
    })

    return div(flex_direction="row", padding=16, gap=16, height="100%")[
        div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
            table()[
                tr()[
                    td()[text("Parrot Tester version", font_size=18, color=SECONDARY_COLOR, font_weight="bold")],
                    td()[text("v0.1", font_size=18, font_weight="bold")],
                ],
                tr()[
                    td()[text("GitHub", font_size=18, color=SECONDARY_COLOR, font_weight="bold")],
                    td()[
                        div(flex_direction="row", gap=8, align_items="center")[
                            text("https://github.com/your-repo", font_size=18, color=ACCENT_COLOR),
                            icon("external_link", size=16, color=ACCENT_COLOR),
                        ],
                    ],
                ],
                tr()[
                    td()[text("parrot.py documentation", font_size=18, color=SECONDARY_COLOR, font_weight="bold")],
                    td()[
                        div(flex_direction="row", gap=8, align_items="center")[
                            text("https://github.com/your-repo/parrot.py", font_size=18, color=ACCENT_COLOR),
                            icon("external_link", size=16, color=ACCENT_COLOR),
                        ],
                    ],
                ],
            ],
            div(flex_direction="row", align_items="center", margin_top=24, margin_left=8)[
                text("Check for updates", font_size=18, color=ACCENT_COLOR),
                icon("external_link", size=16, color=ACCENT_COLOR),
            ],
        ]
    ]