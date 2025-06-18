from talon import actions
from .colors import (
    BORDER_COLOR,
    BG_DARKEST,
)
from .components import last_detection

def page_activity():
    div = actions.user.ui_elements(["div"])

    return div(flex_direction="row", padding=16, gap=16, height="100%")[
        div(
            align_items="center",
            justify_content="center",
            background_color=BG_DARKEST,
            flex=1,
            border_radius=4,
            padding=16,
            border_width=1,
            border_color=BORDER_COLOR
        )[
            last_detection(size="large"),
        ]
    ]