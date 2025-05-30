from talon import actions
from ..parrot_integration_wrapper import restore_patterns, parrot_tester_initialize
from .pages.page_about import page_about
from .pages.page_detection_log import page_detection_log
from .pages.page_frames import page_frames
from .pages.page_patterns import page_patterns
from .pages.page_stats import page_stats
from .pages.page_pattern_edit import edit_page
from .pages.page_settings import page_settings
from ..constants import (
    ACTIVE_COLOR,
    BG_DARKEST,
    BORDER_COLOR,
    WINDOW_BORDER_COLOR,
)
import traceback

tab_id_to_page = {
    "frames": page_frames,
    # "detection_log": page_detection_log,
    "patterns": page_patterns,
    # "stats": page_stats,
    # "settings": page_settings,
    "about": page_about,
}

format_label = lambda label: ' '.join(label.split("_")).capitalize()

def tabs():
    div, button, text, state = actions.user.ui_elements(["div", "button", "text", "state"])
    tab_state, set_tab = state.use("tab")

    return div(flex_direction="row", align_items="flex_end")[
        *[button(on_click=lambda e, id=tab: set_tab(id), padding=16, position="relative")[
            text(format_label(tab), font_size=16, color="FFFFFF"),
            div(
                position="absolute",
                bottom=0,
                background_color=ACTIVE_COLOR,
                height=3,
                width="100%",
                border_radius=2
            ) if tab_state == tab else None
        ] for tab in tab_id_to_page.keys()]
    ]

common_play_button_props = {
    "padding": 8,
    "padding_left": 24,
    "padding_right": 28,
    "flex_direction": "row",
    "align_items": "center",
    "gap": 16,
    "border_width": 1,
    "border_radius": 2,
    "border_color": BORDER_COLOR,
}

def play_button():
    text, icon, button, state, effect = actions.user.ui_elements(["text", "icon", "button", "state", "effect"])
    play, set_play = state.use("play", True)
    play_bg_color = "#13A126"

    def toggle_play(e):
        new_play = not play
        show_hints = not new_play
        actions.user.ui_elements_toggle_hints(show_hints)
        set_play(new_play)
        if new_play:
            parrot_tester_initialize()
        else:
            parrot_tester_disable()

    if play:
        return button(
            common_play_button_props,
            on_click=toggle_play,
            background_color=ACTIVE_COLOR,
            autofocus=True,
        )[
            icon("pause", fill=True),
            text("PAUSE"),
        ]
    else:
        return button(
            common_play_button_props,
            on_click=toggle_play,
            autofocus=True,
            background_color=play_bg_color,
        )[
            icon("play"),
            text("Start listening"),
        ]

def parrot_tester_disable():
    print("Disabling parrot tester")
    restore_patterns()

def parrot_tester_disable_and_exit():
    print("Disabling parrot tester")
    restore_patterns()
    actions.user.ui_elements_hide_all()

def parrot_tester_toggle():
    if actions.user.ui_elements_is_active(parrot_tester_ui):
        parrot_tester_disable_and_exit()
    else:
        try:
            parrot_tester_initialize()
            actions.user.ui_elements_show(parrot_tester_ui, show_hints=False)
        except Exception as e:
            # traceback.print_exc()
            print(f"Error initializing parrot tester: {e}")
            parrot_tester_disable_and_exit()
            return

def parrot_tester_ui():
    window, div, screen, style, component = actions.user.ui_elements([
        "window", "div", "screen", "style", "component"
    ])
    state = actions.user.ui_elements(['state'])
    tab_state = state.get("tab", next(iter(tab_id_to_page)))
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
            on_close=parrot_tester_disable_and_exit,
            flex_direction="column",
            min_width=1100,
            background_color=BG_DARKEST,
            border_radius=8,
            border_width=1,
            border_color=WINDOW_BORDER_COLOR
        )[
            edit_page() if edit_pattern else (
                div(flex_direction="row", align_items="stretch", justify_content="space_between", border_bottom=1, border_color=BORDER_COLOR)[
                    tabs(),
                    # global_options(),
                    div(padding=8)[
                        play_button(),
                    ],
                ],
                div(min_height=750, max_height=900)[
                    component(tab_id_to_page[tab_state]),
                ]
            )
        ]
    ]