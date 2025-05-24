from talon import actions
from .components import play_button, tabs, removable_pill
from ..core import restore_patterns, parrot_tester_initialize
from .page_about import page_about
from .page_frames import page_frames
from .page_pattern_edit import edit_page
from ..constants import (
    WINDOW_BORDER_COLOR,
    BORDER_COLOR,
)

tab_id_to_page = {
    "frames": page_frames,
    "about": page_about,
}

def parrot_tester_disable():
    print("Disabling parrot tester")
    restore_patterns()
    actions.user.ui_elements_hide_all()

def parrot_tester_toggle():
    if actions.user.ui_elements_is_active(parrot_tester_ui):
        parrot_tester_disable()
    else:
        print("Enabling parrot tester")
        try:
            parrot_tester_initialize()
            actions.user.ui_elements_show(parrot_tester_ui)
        except Exception as e:
            print(f"Error initializing parrot tester: {e}")
            parrot_tester_disable()
            return

def current_page():
    div, state = actions.user.ui_elements(["div", "state"])
    tab_state = state.get("tab")

    return div(height=750)[
        tab_id_to_page[tab_state](),
    ]

def edit_modal():
    div, state, text, modal, input_text = actions.user.ui_elements(["div", "state", "text", "modal", "input_text"])
    edit_pattern, set_edit_pattern = state.use("edit_pattern", None)

    return modal(
        title="My Modal",
        open=edit_pattern is not None,
        on_close=lambda: set_edit_pattern(None),
        padding=16,
        # width=800,
        # height=1000,
    )[
        div(gap=16)[
            div(flex_direction="row")[
                text("Pattern", width=100),
                input_text(id="pattern_edit_name", autofocus=True, value="edit_pattern"),
            ],
            div(flex_direction="row")[
                text("Sounds", width=100),
                div(flex_direction="row", gap=8)[
                    removable_pill("ah"),
                    removable_pill("oh")
                ]
            ]
        ],
    ]

def parrot_tester_ui():
    window, div, screen, style = actions.user.ui_elements([
        "window", "div", "screen", "style"
    ])
    state = actions.user.ui_elements('state')
    edit_pattern, set_edit_pattern = state.use("edit_pattern", None)

    style({
        "*": {
            "highlight_color": "BBBBCC33",
            "focus_outline_color": "BBBBCC",
        },
        "text": {
            "color": "EEEEFF",
        },
    })

    return screen(justify_content="center", align_items="center")[
        window(
            title="Parrot Tester",
            on_close=parrot_tester_disable,
            flex_direction="column",
            width=1100,
            background_color="#191B1F",
            border_radius=8,
            border_width=1,
            border_color=WINDOW_BORDER_COLOR
        )[
            edit_page() if edit_pattern else (
                div(flex_direction="row", align_items="flex_end", border_bottom=1, border_color=BORDER_COLOR, position="relative")[
                    div(padding=16)[
                        play_button(),
                    ],
                    div(position="absolute", left=300, bottom=0)[
                        tabs({"start_tab": "frames"}),
                    ],
                ],
                current_page(),
                # edit_modal(),(her
            )
        ]
    ]