from talon import actions
from ...constants import (
    BORDER_COLOR,
)
from ..components import (
    pattern
)
from ...core import (
    get_pattern_json,
)

def page_patterns():
    div, component, table, tr, td, style = actions.user.ui_elements(["div", "component", "table", "tr", "td", "style"])
    patterns = get_pattern_json()

    pattern_items = list(patterns.items())  # (name, pattern)
    pattern_groups = [pattern_items[i:i + 4] for i in range(0, len(pattern_items), 4)]

    style({
        "td": {
            "padding": 8,
        }
    })

    return div(flex_direction="column", padding=8, height="100%")[
        table()[
            *[tr()[
                *[td()[
                    div(background_color="#36393E", border_radius=4, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": name,
                            "highlight_when_active": True,
                        }),
                    ]
                ] for name, pattern_data in group]
            ] for group in pattern_groups]
        ]
    ]