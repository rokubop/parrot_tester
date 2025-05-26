from talon import actions
from ...constants import (
    BORDER_COLOR,
    BORDER_COLOR_LIGHT,
)

def page_settings():
    div, text, switch, state = actions.user.ui_elements(["div", "text", "switch", "state"])
    style = actions.user.ui_elements("style")

    # settings_state, set_settings = state.use("settings", {})

    style({
        ".setting_line": {
            "flex_direction": "row",
            "align_items": "center",
            "justify_content": "space_between",
            "border_bottom": 1,
            "border_color": BORDER_COLOR_LIGHT,
        },
        ".setting_text": {
            "padding_top": 16,
            "padding_bottom": 16,
            "flex": 1,
        }
    })

    return div(flex_direction="row", justify_content="center")[
        div(
            flex_direction="column",
            margin=16,
            padding=24,
            gap=16,
            min_width=500,
            background_color="#1D1F24",
            border_radius=8,
            border_color=BORDER_COLOR_LIGHT,
            border_width=1
        )[
            text("Settings", font_size=20, font_family="inter"),
            div(margin_left=16)[
                div(class_name="setting_line")[
                    text("Listen on launch", class_name="setting_text", for_id="listen_on_launch"),
                    switch(id="listen_on_launch", checked=False),
                ],
            ],
            text("While listening", font_size=18, margin_top=16, font_family="inter"),
            div(margin_left=16)[
                div(class_name="setting_line")[
                    text("Disable speech", class_name="setting_text", for_id="disable_speech"),
                    switch(id="disable_speech", checked=True),
                ],
                div(class_name="setting_line")[
                    text("Disable parrot actions", class_name="setting_text", for_id="disable_noise_actions"),
                    switch(id="disable_noise_actions", checked=True),
                ],
                div(class_name="setting_line")[
                    text("Allow pop action", class_name="setting_text", for_id="allow_pop_action", margin_left=16),
                    switch(id="allow_pop_action", checked=True),
                ],
                div(class_name="setting_line")[
                    text("Triple pop to pause listening", class_name="setting_text", for_id="triple_pop_to_pause"),
                    switch(id="triple_pop_to_pause", checked=True),
                ]
            ],
        ]
    ]