# from talon import actions
# from ..constants import (
#     ACCENT_COLOR,
#     BORDER_COLOR,
#     SECONDARY_COLOR
# )
# from .components import (
#     get_pattern_json,
#     removable_pill,
#     pattern_pill,
# )

# def edit_page():
#     div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
#     table, tr, th, td, style, input_text = actions.user.ui_elements(["table", "tr", "th", "td", "style", "input_text"])

#     edit_pattern, set_edit_pattern = state.use("edit_pattern", None)
#     pattern_data = get_pattern_json(edit_pattern) if edit_pattern else {}

#     style({
#         "th": {
#             "padding": 10,
#             "padding_left": 16,
#             "padding_right": 16,
#             "align_items": "flex_start",
#             "border_bottom": 1,
#             "border_color": BORDER_COLOR,
#             "color": SECONDARY_COLOR,
#         },
#         "tr": {
#             "justify_content": "center",
#         },
#         "td": {
#             "padding": 8,
#             "padding_left": 16,
#             "padding_right": 16,
#             "align_items": "flex_start",
#             "border_bottom": 1,
#             "border_color": BORDER_COLOR,
#         },
#         "input_text": {
#             "border_radius": 4,
#             "border_width": 1,
#             "font_size": 14,
#             "border_color": BORDER_COLOR,
#             "background_color": "#151515",
#             "color": "#EEEEFF",
#         },
#     })

#     return div(align_items="center")[
#         div(padding=16, gap=16)[
#             div(flex_direction="row", align_items="center", gap=8)[
#                 button(on_click=lambda e: set_edit_pattern(None), flex_direction="row", align_items="center", gap=4, padding=8)[
#                     icon("arrow_left", size=16),
#                     text("Back"),
#                 ],
#             ],

#             div(flex_direction="column", gap=8)[
#                 text(f"Editing Pattern: {edit_pattern}", font_size=24),
#                 text("Modify pattern parameters. Any overridden values will replace the original pattern settings.", color=SECONDARY_COLOR),
#             ],

#             div(flex_direction="row", gap=16)[
#                 table()[
#                     tr()[
#                         th(width="20%")[text("Field")],
#                         th(width="40%")[text("Original")],
#                         th(width="40%")[text("Override")],
#                     ],
#                     tr()[
#                         td()[text("Pattern name")],
#                         td()[text(edit_pattern)],
#                         td()[input_text(id="pattern_name", value=edit_pattern)],
#                     ],
#                     tr()[
#                         td()[text("Sounds")],
#                         td()[text(", ".join(pattern_data.get("sounds", [])))],
#                         td()[
#                             div(flex_direction="row", gap=8, flex_wrap=True)[
#                                 *[removable_pill(sound) for sound in pattern_data.get("sounds", [])],
#                                 pattern_pill("Add sound"),
#                             ],
#                         ],
#                     ],
#                     tr()[
#                         td()[text("Throttles")],
#                     ],
#                     *[tr()[
#                         td()[text(f"{key}", margin_left=16)],
#                         td()[text(value)],
#                         td()[input_text(id=f"throttle_{key}", value=value, width=100)]
#                     ] for key, value in pattern_data.get("throttle", {}).items()],
#                     tr()[
#                         td()[text("Detect after")],
#                         td()[text(str(pattern_data.get("detect_after", "")))],
#                         td()[input_text(id="detect_after", value=str(pattern_data.get("detect_after", "")), width=100)],
#                     ],
#                 ],
#                 table(width="100%")[
#                     tr()[
#                         th(width="20%")[text("Field")],
#                         th(width="40%")[text("Original")],
#                         th(width="40%")[text("Override")],
#                     ],
#                     tr()[
#                         td()[text("Thresholds")],
#                     ],
#                     tr()[
#                         td()[text(">power", margin_left=16)],
#                         td()[text(pattern_data.get("threshold", {}).get(">power", "0"))],
#                         td()[input_text(id="threshold_power", value=pattern_data.get("threshold", {}).get(">power", "0"), width=100)],
#                     ],
#                     tr()[
#                         td()[text(">probability", margin_left=16)],
#                         td()[text(pattern_data.get("threshold", {}).get(">probability", "0"))],
#                         td()[input_text(id="threshold_probability", value=pattern_data.get("threshold", {}).get(">probability", "0"), width=100)],
#                     ],
#                     tr()[
#                         td()[text("Grace period")],
#                         td()[text(str(pattern_data.get("graceperiod", "")))],
#                         td()[input_text(id="grace_period", value=str(pattern_data.get("graceperiod", "")), width=100)],
#                     ],
#                     tr()[
#                         td()[text("Grace thresholds")],
#                         td()[
#                             div(flex_direction="column", gap=4)[
#                                 *[
#                                     div(flex_direction="row", gap=8)[
#                                         text(f"{key}:"),
#                                         text(value),
#                                     ]
#                                     for key, value in pattern_data.get("grace_threshold", {}).items()
#                                 ],
#                             ],
#                         ],
#                         td()[
#                             div(flex_direction="column", gap=4)[
#                                 *[
#                                     div(flex_direction="row", gap=8)[
#                                         text(f"{key}:"),
#                                         input_text(id=f"grace_threshold_{key}", value=value, width=100),
#                                     ]
#                                     for key, value in pattern_data.get("grace_threshold", {}).items()
#                                 ],
#                             ],
#                         ],
#                     ],
#                 ],
#             ],

#             # Action buttons
#             div(flex_direction="row", gap=16, justify_content="flex_end", margin_top=16)[
#                 button(padding=8, padding_left=16, padding_right=16, border_width=1, border_color=BORDER_COLOR, border_radius=4)[
#                     text("Cancel"),
#                 ],
#                 button(padding=8, padding_left=16, padding_right=16, background_color=ACCENT_COLOR, border_radius=4)[
#                     text("Save changes"),
#                 ],
#             ],
#         ] if edit_pattern else None
#     ]
