from talon import actions
import json
import os
from .colors import (
    SECONDARY_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
)
from .components import last_detection

def page_activity():
    div, text, table, tr, td, style, icon, link = actions.user.ui_elements(
        ["div", "text", "table", "tr", "td", "style", "icon", "link"]
    )

    style({
        "td": {
            "padding": 8,
        },
        "text": {
            "font_size": 18,
        }
    })

    return div(flex_direction="row", padding=16, gap=16, height="100%")[
        div(align_items="center", justify_content="center", background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
            last_detection(size="large"),
        ]
    ]