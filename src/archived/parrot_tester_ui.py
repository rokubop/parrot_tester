from talon import Context, actions, clip, cron
from pathlib import Path
import pprint
import re
import random
import math
import time
from .core import (
    parrot_tester_initialize,
    restore_patterns,
    get_pattern_json,
    get_pattern_color,
)

pp = pprint.PrettyPrinter()

ctx = Context()
data = {}
start_time = 0
cron_job = None
duration = 10.0

def set_data(noise, power, f0, f1, f2):
    global data

    if noise not in data:
        data[noise] = {
            "triggered_count": 0,
            "power": [],
            "f0": [],
            "f1": [],
            "f2": [],
            "average_power": 0,
            "average_f0": 0,
            "average_f1": 0,
            "average_f2": 0,
            "min_power": 0,
            "min_f0": 0,
            "min_f1": 0,
            "min_f2": 0,
            "max_power": 0,
            "max_f0": 0,
            "max_f1": 0,
            "max_f2": 0,
        }

    if power is not None:
        data[noise]["power"].append(power)

    if f0 is not None:
        data[noise]["f0"].append(f0)

    if f1 is not None:
        data[noise]["f1"].append(f1)

    if f2 is not None:
        data[noise]["f2"].append(f2)

    data[noise]["triggered_count"] += 1

    data[noise]["average_power"] = sum(data[noise]["power"]) / len(data[noise]['power'])
    data[noise]["average_f0"] = sum(data[noise]["f0"]) / len(data[noise]['f0'])
    data[noise]["average_f1"] = sum(data[noise]["f1"]) / len(data[noise]['f1'])
    data[noise]["average_f2"] = sum(data[noise]["f2"]) / len(data[noise]['f2'])
    data[noise]["min_power"] = min(data[noise]["power"])
    data[noise]["min_f0"] = min(data[noise]["f0"])
    data[noise]["min_f1"] = min(data[noise]["f1"])
    data[noise]["min_f2"] = min(data[noise]["f2"])
    data[noise]["max_power"] = max(data[noise]["power"])
    data[noise]["max_f0"] = max(data[noise]["f0"])
    data[noise]["max_f1"] = max(data[noise]["f1"])
    data[noise]["max_f2"] = max(data[noise]["f2"])

    actions.user.ui_elements_set_text(f"{noise}_count", f"({data[noise]['triggered_count']})")
    actions.user.ui_elements_set_text(f"{noise}_power_latest", f"{power:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_latest", f"{f0:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_latest", f"{f1:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_latest", f"{f2:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_power_average", f"{data[noise]['average_power']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_average", f"{data[noise]['average_f0']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_average", f"{data[noise]['average_f1']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_average", f"{data[noise]['average_f2']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_power_min", f"{data[noise]['min_power']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_min", f"{data[noise]['min_f0']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_min", f"{data[noise]['min_f1']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_min", f"{data[noise]['min_f2']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_power_max", f"{data[noise]['max_power']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_max", f"{data[noise]['max_f0']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_max", f"{data[noise]['max_f1']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_max", f"{data[noise]['max_f2']:.2f}")

def init_parrot_noises_state():
    noise_definitions_file = Path(__file__).parent.parent / "auto_generated" / "parrot_tester_active.talon"

    with open(noise_definitions_file, "r") as file:
        content = file.readlines()

    noises = [re.search(r'parrot\(([^):]+)', line).group(1) for line in content if line.startswith("parrot(")]

    noises = {
        noise: { "active": True, "color": random_hex_color() } for noise in noises
    }

    return noises

def copy_all_data_to_clipboard():
    clip.set_text(pp.pformat(data))

def copy_data_to_clipboard(noise):
    return lambda e: clip.set_text(pp.pformat(data[noise])) if noise in data else None

def noise_data_ui(noise):
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])

    def cell():
        return div(padding=8, border=1, background_color="212141")

    def cell_alt():
        return div(padding=8, border=1, background_color="313151")

    def stat_category(name):
        return div(width=80, flex_direction="column")[
            div()[
                cell()[text(name)],
                cell_alt()[text(id=f"{noise}_power_{name.lower()}")],
                cell()[text(id=f"{noise}_f0_{name.lower()}")],
                cell_alt()[text(id=f"{noise}_f1_{name.lower()}")],
                cell()[text(id=f"{noise}_f2_{name.lower()}")],
            ],
        ]

    return div(flex_direction="column", padding=16, border_width=1, id=noise)[
        div(flex_direction="row", justify_content="space_between", align_items="center")[
            div(flex_direction="row", align_items="center", gap=8, margin_bottom=16)[
                text(noise, font_size=20, font_weight="bold"),
                text(id=f"{noise}_count"),
            ],
            button(border_radius=4, on_click=copy_data_to_clipboard(noise), align_items="center", flex_direction="row", gap=8)[
                text("Copy", font_size=14),
                icon("copy")
            ]
        ],
        div(flex_direction="row")[
            div(flex_direction="column")[
                cell()[text(" ")],
                cell_alt()[text("Power")],
                cell()[text("F0")],
                cell_alt()[text("F1")],
                cell()[text("F2")],
            ],
            stat_category("Latest"),
            stat_category("Average"),
            stat_category("Min"),
            stat_category("Max"),
        ],
    ]


def rect_color(color, size=20, **props):
    div = actions.user.ui_elements("div")
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return div(**props)[
        svg(size=size)[
            rect(x=0, y=0, width=24, height=24, fill=color)
        ]
    ]

def stop_icon(**props):
    div = actions.user.ui_elements("div")
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return div(justify_content="center", **props)[
        svg()[
            rect(x=4, y=4, width=16, height=16, fill="FFFFFF"),
        ]
    ]

def delta_icon(**props):
    div = actions.user.ui_elements("div")
    svg, path = actions.user.ui_elements_svg(["svg", "path"])

    return div(justify_content="center", **props)[
        svg(size=16)[
            path(d="M5 20h14L12 4z"),
        ]
    ]

def random_hex_color():
    r = random.randint(50, 255)
    g = random.randint(50, 255)
    b = random.randint(50, 255)
    return f"#{r:02X}{g:02X}{b:02X}"

def noise_item(noise):
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return button(flex_direction="row", padding=8, border_width=1, gap=8, border_color=BORDER_COLOR, align_items="center")[
        icon("chevron_right", size=20),
        icon("check", size=20),
        # random color 6 digit hex
        rect_color(random_hex_color()),
        div(min_width=100, flex_direction="row", justify_content="space_between")[
            text(noise),
            text("20"),
        ]
    ]

def cell(children):
    div = actions.user.ui_elements("div")

    return div(padding_left=8, padding_right=8, border_top=1, height=32, justify_content="center", border_color="383838")[
        children
    ]

def log():
    div, text, state = actions.user.ui_elements(["div", "text", "state"])

    log = state.get("log")
    noises = state.get("noises")

    return div(id="log", flex_direction="column", min_height=500, overflow_y="scroll", max_height=800, border_width=1, background_color="191B1F")[
        # text('hello'),
        *[row(item, noises[item["noise"]]["color"]) for item in log],
        # time_col(),
        # # time_delta_col(),
        # color_col(),
        # noise_col(),
        # power_col(),
        # # delta_power_col(),
        # # count_col(),
        # f0_col(),
        # f1_col(),
        # f2_col(),
    ]

# def toggle_play(e):
#     actions.user.ui_elements_set_state("play", lambda p: not p)



# def Timeline():
#     div, state, effect = actions.user.ui_elements(["div", "state", "effect"])

#     effect(init_graph, [])

#     return div(id="timeline", position="relative", width="100%", min_width=900, height=150, background_color="191B1F", border_width=1)[
#      *[div(position="absolute", width=1, height="100%", background_color="333333", left=f"{i * 10}%") for i in range(11)],
#     ]

def cron_timer_enable():
    global cron_job, start_time

    def update():
        elapsed = time.perf_counter() - start_time
        fraction = (elapsed % duration) / duration
        actions.user.ui_elements_set_state("time_fraction", fraction)

    cron_job = cron.interval("32ms", update)

def cron_timer_disable():
    global cron_job
    if cron_job:
        cron.cancel(cron_job)
        cron_job = None

def play_button():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
    play, set_play = state.use("play", False)
    play_bg_color = "191B1F"

    def toggle_play(e):
        global start_time
        is_live = not play
        set_play(is_live)

        if is_live:
            start_time = time.perf_counter()
            ctx.tags = ["user.parrot_tester"]
            cron_timer_enable()
        else:
            ctx.tags = []
            cron_timer_disable()

    if play:
        return button(on_click=toggle_play, align_items="center", gap=16, padding=12, padding_left=24, padding_right=28, flex_direction="row", border_width=1, margin_right=16, border_color="333333", border_radius=16)[
            icon("stop", color="C6053D"),
            text("Stop listening"),
        ]
    else:
        return button(on_click=toggle_play, autofocus=True, align_items="center", gap=16, padding=12, padding_left=24, padding_right=28, flex_direction="row", border_width=1, margin_right=16, border_color="333333", border_radius=16)[
            icon("play", fill=play_bg_color),
            text("Start listening"),
        ]

def clear_all(e):
    global start_time
    start_time = 0
    actions.user.ui_elements_set_state({
        "log": [],
        "play": False,
        "time_fraction": 0,
    })
    ctx.tags = []
    cron_timer_disable()

def controls():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])

    # play_bg_color = "73BF69"
    return div(flex_direction='row', gap=16, align_items="center")[
        play_button(),
        button()[icon("chevron_left")],
        text("Page 1"),
        button()[icon("chevron_right")],
        styled_button("New page"),
        styled_button("Clear page"),
        styled_button("Clear all", on_click=clear_all),
        # button("Prev page"),
        # button("Page 1"),
        # button("Next page"),
        # div(flex_direction="row", gap=8, margin_right=16, align_items="center")[
        #     text("Time", font_size=14),
        #     input_text(value="10", id="graph_time", width=50, border_radius=4),
        # ],
        # div(flex_direction="row", gap=8, align_items="center")[
        #     text("Power", font_size=14),
        #     input_text(value="20", id="graph_power", width=50, border_radius=4),
        # ],
        styled_button("Import"),
        styled_button("Export"),
    ]

def sidebar():
    div, text, state, button = actions.user.ui_elements(["div", "text", "state", "button"])

    noises = state.get("noises")

    return div(flex_direction='column', padding=16, border_right=1, border_color=BORDER_COLOR)[
        text("Parrot Tester", font_size=24, margin_bottom=24),
        *[noise_item(noise) for noise in noises]
    ]

def filter_dropdown_button(title: str):
    text, icon, button = actions.user.ui_elements(["text", "icon", "button"])
    return button(flex_direction="row", align_items="center", gap=8, border_radius=4, border_color=BORDER_COLOR, border_width=1, padding=8, padding_left=16, padding_right=16)[
        text(title),
        icon("chevron_down", size=16),
    ]

def styled_button(title: str, on_click=lambda e: None):
    button = actions.user.ui_elements(["button"])
    return button(text=title, on_click=on_click, border_radius=4, border_color=BORDER_COLOR, border_width=1, padding=12, padding_left=16, padding_right=16)

def filters():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="row", gap=12)[
        filter_dropdown_button("View: Log"),
        filter_dropdown_button("Noises"),
        filter_dropdown_button("Columns"),
        filter_dropdown_button("Scope: Single page"),
        filter_dropdown_button("Mode: One-shot"),
    ]

def noise(name, color, active, toggle_active):
    div, text = actions.user.ui_elements(["div", "text"])
    opacity = 1 if active else 0.5
    color = color if active else "999999"

    return div(
        opacity=opacity,
        # on_click=toggle_active,
        flex_direction="row",
        gap=4,
        align_items="center",
        border_width=1,
        border_radius=4,
        padding=6,
        id=name,
    )[
        rect_color(color, size=15),
        text(name),
    ]

def noises_ui():
    div, state = actions.user.ui_elements(["div", "state"])

    noises, set_noises = state.use("noises")

    def toggle_active(name):
        def toggle(e):
            set_noises({
                **noises,
                name: {
                    **noises[name],
                    "active": not noises[name]["active"]
                }
            })

        return toggle

    return div(flex_direction="row", gap=12)[
        *[noise(
            name=name,
            color=data["color"],
            active=data["active"],
            toggle_active=toggle_active(name)
        ) for name, data in noises.items()]
    ]
        # noise("ah", random_hex_color()),
        # noise("oh", random_hex_color()),
        # noise("ee", random_hex_color()),
        # noise("guh", random_hex_color()),
        # noise("eh", random_hex_color()),
        # noise("er", random_hex_color()),
        # noise("t", random_hex_color()),
        # noise("mm", random_hex_color()),
        # noise("palate", random_hex_color()),
        # noise("pop", random_hex_color()),
        # noise("tut", random_hex_color()),
        # noise("sh", random_hex_color()),
        # noise("ss", random_hex_color()),
        # noise("cluck", random_hex_color()),
    # ]

# def nav():
#     div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
#     return div(flex_direction="row", gap=16, width="100%", justify_content="center", align_items="center")[
#         button()[icon("chevron_left")],
#         text("Page 1"),
#         button()[icon("chevron_right")],
#     ]
def header():
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    return div(flex_direction='row', justify_content="space_between")[
        text("Parrot Tester", font_size=24, margin=18),
        button(on_click=parrot_tester_disable, padding=18)[
            icon("close")
        ]
    ]

def tabs():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])

    tab, set_tab = state.use("tab", "activity")

    def tab_button(name):
        return button(
            on_click=lambda e: set_tab(name),
            padding=8,
            border_radius=4,
            border_color=BORDER_COLOR,
            border_width=1,
            background_color="191B1F" if tab == name else "212141",
            flex_direction="row",
            gap=8,
        )[
            text(name.capitalize()),
        ]

    return div(flex_direction='row', justify_content="space_between")[
        tab_button("activity"),
        tab_button("log"),
        # tab_button("timeline"),
        tab_button("stats"),
        tab_button("patterns"),
    ]

def body():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
    tab = state.get("tab", "activity")
    return div(flex_direction='row', justify_content="space_between")[
        text("Hello"),
        text(f"Current Tab: {tab}"),
    ]

def parrot_tester_ui_2(props):
    div, text, screen, window = actions.user.ui_elements(["div", "text", "screen", "window"])

    return screen(justify_content="center", align_items="center")[
        window(id="parrot_tester", title="Parrot Tester", on_close=parrot_tester_disable, on_minimize=parrot_tester_disable)[
        # div(draggable=True, background_color="222222", border_radius=8, border_width=1)[
            # div(flex_direction='row')[
                # sidebar(),
            # header(),
            div(flex_direction='column', width="100%", gap=16, padding=16)[
                play_button(),
                tabs(),
                body(),
                # controls(),
                # filters(),
                # noises_ui(),
                # # log(),
                # Timeline,
                # # nav(),
                # controls(),
            ]
        ]
    ]

# def parrot_tester_ui_2(props):
#     div, text, screen, window = actions.user.ui_elements(["div", "text", "screen", "window"])

#     return screen(justify_content="center", align_items="center")[
#         window(id="parrot_tester", title="Parrot Tester", on_close=parrot_tester_disable, on_minimize=parrot_tester_disable)[
#         # div(draggable=True, background_color="222222", border_radius=8, border_width=1)[
#             # div(flex_direction='row')[
#                 # sidebar(),
#             # header(),
#             div(flex_direction='column', width="100%", gap=16, padding=16)[
#                 # controls(),
#                 filters(),
#                 noises_ui(),
#                 # log(),
#                 Timeline,
#                 # nav(),
#                 controls(),
#             ]
#         ]
#     ]

def log_to_vertical_lines(log, noises):
    max_power = 40
    duration = 10.0
    lines = []
    for item in log:
        if item["power"]:
            lines.append({
                "time_fraction": (item["time"] % duration) / duration,
                "power_fraction": (min(item["power"] / max_power, max_power) * 0.8) + 0.2,
                "color": noises[item["noise"]]["color"],
            })
    return lines

def filter_last_x_seconds(log, seconds):
    now = time.perf_counter() - start_time
    filtered_log = []
    for item in log:
        if item["time"] >= now - seconds:
            filtered_log.append(item)
    return filtered_log

def graph(props):
    div, screen, state = actions.user.ui_elements(["div", "screen", "state"])
    rect = props["rect"]
    time_fraction = state.get("time_fraction", 0)
    log = state.get("log")
    filtered_log = filter_last_x_seconds(log, 10)
    noises = state.get("noises")
    lines = log_to_vertical_lines(filtered_log, noises)

    return screen()[
        div(position="absolute", left=rect.x, top=rect.y, width=rect.width, height=rect.height)[
            div(position="absolute", z_index=2, bottom=0, height=2, width=f"{time_fraction * 100}%", background_color="73BF69", border_radius=2),
            *[
                div(
                    position="absolute",
                    left=f"{line['time_fraction'] * 100}%",
                    bottom=0,
                    height=f"{line['power_fraction'] * 100}%",
                    width=2,
                    background_color=line["color"],
                    border_radius=2) for line in lines
            ],
        ]
    ]

def init_graph():
    timeline_node = actions.user.ui_elements_get_node("timeline")
    rect = timeline_node.box_model.padding_rect
    actions.user.ui_elements_show(
        graph,
        props={
            "rect": rect,
        }
    )

def listen():
    ctx.tags = ["user.parrot_tester"]

def stop_listen():
    ctx.tags = []

def parrot_tester_disable():
    global start_time
    print("Disabling parrot tester")
    restore_patterns()
    start_time = 0
    ctx.tags = []
    data.clear()
    actions.user.ui_elements_hide_all()
    data.clear()
    cron_timer_disable()

def parrot_tester_toggle():
    """Toggle parrot tester"""
    global start_time

    if actions.user.ui_elements_is_active(parrot_tester_new_ui):
        parrot_tester_disable()
    else:
        parrot_tester_initialize()
        actions.user.ui_elements_show(parrot_tester_new_ui)

HEADER_TEXT = "Parrot Tester"
DOCS_BUTTON_TEXT = "parrot.py documentation"
PATTERNS_BUTTON_TEXT = "patterns.json"
# TABS = ["Frames", "Log", "Silence", "Stats", "Patterns", "Export", "About"]
TABS = ["Frames", "About"]
CHART_DATA = [10, 20, 30, 40, 50, 40, 30, 20]
DETAILS_TEXT = [f"pop {i*10}, gu4 {i*5}" for i in range(1, 9)]
GREEN = "3D7D3D"

def play_button():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
    play, set_play = state.use("play", False)
    play_bg_color = "191B1F"

    def toggle_play(e):
        is_live = not play
        set_play(is_live)

    if play:
        return div(flex_direction="row", align_items="center", gap=8)[
            button(on_click=toggle_play, background_color="991111", align_items="center", gap=16, padding=8, padding_left=14, padding_right=18, flex_direction="row", border_color=BORDER_COLOR, border_radius=8)[
                icon("stop", color="C6053D", size=16, stroke_width=4),
                text("Stop listening", font_size=16, font_weight="bold"),
            ],
            text("Listening..."),
        ]
    else:
        return button(on_click=toggle_play, align_items="center", background_color=GREEN, gap=16, padding=8, padding_left=14, padding_right=18, flex_direction="row", border_color=BORDER_COLOR, border_radius=8)[
            icon("play", fill=play_bg_color, size=16, stroke_width=4),
            text("Start listening", font_size=18),
        ]

def legend():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])

    # style({
    #     "table":{
    #         # "border_width": 1,
    #         # "background_color": "222222",
    #     },
    #     "th": {
    #         "padding": 8,
    #         "padding_left": 10,
    #         "padding_right": 10,
    #         "align_items": "flex_start",
    #     },
    #     "td": {
    #         "padding": 8,
    #         "padding_left": 10,
    #         "padding_right": 10,
    #         "align_items": "flex_start",
    #     },
    # })

    return div(flex_direction="row", gap=32, align_items="flex_end")[
        div(flex_direction="row", gap=8, align_items="center")[
            text("Detected"),
            icon("check", size=14, color="73BF69", stroke_width=3),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Throttle"),
            icon("clock", size=14, color="FFCC00"),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            text("Not detected"),
            text("-", color="999999"),
        ],
    ]

    return table()[
        tr()[
            td()[text("Detected")],
            td()[icon("check", size=16, color="73BF69", stroke_width=3)],
        ],
        tr()[
            td()[text("Throttled")],
            td()[icon("clock", size=16, color="FFCC00")],
        ],
        tr()[
            td()[text("Not detected")],
            td()[text("-", color="999999")],
        ],
    ]




    #         th()[text("Detected")],
    #         th()[text("Throttled")],
    #         th()[text("Not detected")],
    #     ],
    #     tr()[
    #         td()[icon("check", size=16, color="73BF69", stroke_width=3)],
    #         td()[text("!", color="C6053D", font_weight="bold")],
    #         td()[text("-", color="999999")],
    #     ],
    # ]

    # return table()[
    #     tr()[
    #         th()[text("Detected")],
    #         th()[text("Throttled")],
    #         th()[text("Not detected")],
    #     ],
    #     tr()[
    #         td()[icon("check", size=16, color="73BF69", stroke_width=3)],
    #         td()[text("!", color="C6053D", font_weight="bold")],
    #         td()[text("-", color="999999")],
    #     ],
    # ]

    # return div(flex_direction="row", gap=24, padding=16)[
    #     div(flex_direction="row", gap=4, align_items="center")[
    #         text("Detected"),
    #         icon("check", size=16, color="73BF69"),
    #     ],
    #     div(flex_direction="row", gap=4, align_items="center")[
    #         text("Throttled"),
    #         text("!"),
    #     ],
    #     div(flex_direction="row", gap=4, align_items="center")[
    #         text("Not detected"),
    #         text("-"),
    #     ],
    # ]

ACTIVE_COLOR = "3B71D9"
ACCENT_COLOR = "67A4FF"
SECONDARY_COLOR = "CCCCCC"
WINDOW_BORDER_COLOR = "#2F3137"
BORDER_COLOR = "#000000"

def number(value, **kwargs):
    text = actions.user.ui_elements("text", **kwargs)
    return text(value, font_family="consolas")

def graph_test():
    div, text, state = actions.user.ui_elements(["div", "text", "state"])
    last_capture = state.get("last_capture", None)
    frames = last_capture.frames if last_capture else []

    # time_fraction = state.get("time_fraction", 0)
    # log = state.get("log")
    # filtered_log = filter_last_x_seconds(log, 10)
    # noises = state.get("noises")
    # lines = log_to_vertical_lines(filtered_log, noises)

    lines = [
        {"time_fraction": frame.index * 0.04, "power_fraction": min(1.0, frame.power / 30), "color": "73BF69"} \
            for frame in frames
    ]

    # lines = [
    #     {"time_fraction": 0.0, "power_fraction": 0.1, "color": "73BF69"},
    #     {"time_fraction": 0.04, "power_fraction": 0.51, "color": "73BF69"},
    #     {"time_fraction": 0.08, "power_fraction": 0.55, "color": "73BF69"},
    #     {"time_fraction": 0.12, "power_fraction": 0.35, "color": "73BF69"},
    # ]

    return div(position="relative", min_width=500, height=130, margin_bottom=20, margin_left=25, margin_top=16, border_bottom=1, border_color=BORDER_COLOR)[
        # div(position="absolute", z_index=2, bottom=0, height=2, width=f"{time_fraction * 100}%", background_color="73BF69", border_radius=2),
        # 4 horizontal lines
        *[div(position="absolute", width="100%", height=1, background_color=BORDER_COLOR, top=f"{i * 25}%") for i in range(1, 4)],
        # 4 text labels on left
        *[div(position="absolute", left=-35, width=25, align_items="flex_end", top=f"{i * 25}%", margin_top=18)[text(str(val), color=SECONDARY_COLOR, font_size=12)] for i, val in enumerate([30, 20, 10, 0])],
        *[
            div(
                position="absolute",
                left=f"{line['time_fraction'] * 100}%",
                bottom=0,
                height=f"{line['power_fraction'] * 100}%",
                width=9,
                background_color=line["color"],
                border_radius=2) for line in lines
        ],
        # labels under bars
        *[div(position="absolute", left=f"{line['time_fraction'] * 100}%", bottom=-20, align_items="center")[text(str(i), font_size=12, font_weight="bold")] for i, line in enumerate(lines)],
    ]

def status_cell(status: str, graceperiod: bool = False):
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])

    s = None

    if status == "detected":
        s = icon("check", size=16, color="73BF69", stroke_width=3)
    if status == "throttled":
        s = icon("clock", size=16, color="FFCC00")
        # return text("!", color="C6053D", font_weight="bold")
    if s:
        # if graceperiod:
        #     return div(flex_direction="row", gap=4, align_items="center")[
        #         text("~", color="C6053D", font_weight="bold"),
        #         s,
        #     ]
        return s
    return text("-", color="999999")

def power_ratio_bar(power: float, patterns: list, power_threshold: float = None):
    div, icon = actions.user.ui_elements(["div", "icon"])
    power_percent = min(30, power) / 30
    power_threshold_percent = min(30, power_threshold) / 30 if power_threshold else 0
    full_bar_width = 150
    bar_width = int(full_bar_width * power_percent)
    power_threshold_left = int(power_threshold_percent * full_bar_width) if power_threshold else None
    # print("power_threshold_left", power_threshold_left)

    return div(position="relative", flex_direction="row", width=bar_width, background_color="555555", height=9)[
        *[div(width=int(pattern["probability"] * bar_width), background_color=pattern["color"]) for pattern in patterns],
        div(position="absolute", left=power_threshold_left - 1.5, width=1.5, top=0, bottom=0, background_color="191B1FCC") if power_threshold else None,
        # div(position="absolute", left=power_threshold_left - 7, top=0, bottom=0)[
        #     icon("diamond", size=9, color="191B1F", fill="191B1F" stroke_width=3)
        # ] if power_threshold else None,
    ]

def table_test():
    div, text, icon, style = actions.user.ui_elements(["div", "text", "icon", "style"])
    table, th, tr, td = actions.user.ui_elements(["table", "th", "tr", "td"])
    state = actions.user.ui_elements("state")

    # capture_updating = state.get("capture_updating", False)
    last_capture = state.get("last_capture", None)
    frames = last_capture.frames if last_capture else []

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
            th(align_items="flex_end")[text("Frame", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[div(flex_direction="row", gap=2, align_items="center")[
                icon("delta", size=11, stroke_width=3, color=SECONDARY_COLOR),
                text("ts", color=SECONDARY_COLOR),
            ]],
            th()[text("Pattern", color=SECONDARY_COLOR)],
            # th()[text("Sounds", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[text("Power", color=SECONDARY_COLOR)],
            th(align_items="flex_end")[text("Prob.", color=SECONDARY_COLOR)],
            th(align_items="center")[text("Status", color=SECONDARY_COLOR)],
            th(align_items="flex_start")[div(flex_direction="row", gap=2)[
                text("Power", color=SECONDARY_COLOR),
                icon("multiply", size=11, stroke_width=3, color=SECONDARY_COLOR),
                text("Prob.", color=SECONDARY_COLOR),
            ]],
        ],
        *[
            tr()[
                td()[number(str(frame.id))],
                td()[number(frame.format(frame.ts_delta, 3))],
                td(align_items="flex_start")[div(gap=8, min_width=60)[
                    *[text(p["name"]) for p in frame.patterns]
                ]],
                # td(align_items="flex_start")[div(gap=8)[
                #     *[text(", ".join(p["sounds"])) for p in frame.patterns]
                # ]],
                td()[number(frame.format(frame.power, 2))],
                td(align_items="flex_end")[div(gap=8)[
                    *[number(frame.format(p["probability"], 4)) for p in frame.patterns]
                ]],
                td(align_items="center")[div(gap=8, align_items="center")[
                    *[status_cell(p['status'], p['graceperiod']) for p in frame.patterns]
                ]],
                td(align_items="flex_start", justify_content="center")[
                    power_ratio_bar(
                        frame.power,
                        frame.patterns,
                        frame.winner_power_threshold if frame.detected else None
                    )
                ],
            ] for frame in frames
        ],
        # tr()[
        #     td()[number("1")],
        #     td()[number("-call")],
        #     td()[number("4.2")],
        #     td(align_items="flex_start")[text("pop")],
        #     td()[number("0.522")],
        #     td(align_items="center")[text("-", color="999999")],
        # ],
        # tr()[
        # # tr(background_color="272727")[
        #     td(justify_content="center")[number("2")],
        #     td(justify_content="center")[number("+0.000")],
        #     td(justify_content="center")[number("20.2")],
        #     td(align_items="flex_start")[div(gap=8)[
        #         text("pop"),
        #         text("guh"),
        #     ]],
        #     td(align_items="flex_end")[div(gap=8)[
        #         number("0.999"),
        #         number("0.032")
        #     ]],
        #     td(align_items="center")[div(gap=8, align_items="center")[
        #         icon("check", size=16, color="73BF69", stroke_width=3),
        #         text("-", color="999999"),
        #     ]],
        # ],
        # tr()[
        #     td(justify_content="center")[number("3")],
        #     td(justify_content="center")[number("+0.252")],
        #     td(justify_content="center")[number("21.2")],
        #     td(align_items="flex_start")[div(gap=8)[
        #         text("pop"),
        #     ]],
        #     td()[div(gap=8)[
        #         number("0.984"),
        #     ]],
        #     td(align_items="center")[div(gap=8)[
        #         text("!", color="C6053D", font_weight="bold"),
        #     ]],
        # ],
        # tr()[
        #     td(justify_content="center")[number("4")],
        #     td(justify_content="center")[number("+0.312")],
        #     td(justify_content="center")[number("13.2")],
        #     td(align_items="flex_start")[div(gap=8)[
        #         text("pop"),
        #         text("guh"),
        #     ]],
        #     td(align_items="flex_end")[div(gap=8)[
        #         number("0.442"),
        #         number("0.032")
        #     ]],
        #     td(align_items="center")[div(gap=8)[
        #         text("-", color="999999"),
        #         text("-", color="999999"),
        #     ]],
        # ],
        # div(position="absolute", top=0, left=0, width="100%", height="100%", background_color="00000066") if capture_updating else None,
    ]

    #         th(font_size=14, padding=8)[text("Noise")],
    #         th(font_size=14, padding=8)[text("Power")],
    #         th(font_size=14, padding=8)[text("F0")],
    #     ],
    #     tr(background_color="222222")[
    #         td(font_size=14, padding=8)[text("pop")],
    #         td(font_size=14, padding=8)[text("20")],
    #         td(font_size=14, padding=8)[text("20")],
    #     ],
    #     tr(background_color="292929")[
    #         td(font_size=14, padding=8)[text("asafefwefw")],
    #         td(font_size=14, padding=8)[text("30.2333")],
    #         # td(padding=8)[text("20")],
    #     ],
    # ]

def key_val(key, val):
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="row", gap=8, justify_content="space_between")[
        text(key, font_size=15, color=ACCENT_COLOR),
        number(val),
    ]

def pattern(props):
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    table, tr, td, style = actions.user.ui_elements(["table", "tr", "td", "style"])

    pattern_data = get_pattern_json(props["name"])
    pattern_color = get_pattern_color(props["name"])

    style({
        "th": {
            "padding": 5,
            "padding_right": 7,
            "flex_direction": "row",
            "align_items": "center",
            # "padding_left": 0,
            # "padding_right": 12,
        },
        "td": {
            "padding": 5,
            "padding_right": 7,
            "flex_direction": "row",
            "align_items": "center",
            # "padding_left": 0,
            # "padding_right": 12,
        },
    })

    throttles = pattern_data.get("throttle", {})
    throttle_items = list(throttles.items())
    throttle_groups = [throttle_items[i:i + 2] for i in range(0, len(throttle_items), 2)]

    return div(id=f"pattern_{props['name']}", padding=16, flex_direction="column", gap=8, width=300, border_bottom=1, border_color=BORDER_COLOR)[
        div(flex_direction="row", gap=8, align_items="center", padding_bottom=8)[
            rect_color(pattern_color, size=14),
            text(props["name"], font_size=20),
        ],
        div(justify_content="center", align_items="center")[
            div()[
                div(flex_direction="row", gap=8, margin_left=15, align_items="center")[
                    text("sounds", font_size=14, color=ACCENT_COLOR),
                    text(",".join(pattern_data.get("sounds", [])), font_size=14),
                ],
                table(padding=8, padding_bottom=0)[
                    tr()[
                        td(position="relative")[
                            text(">power", font_size=14, color=ACCENT_COLOR),
                            # text("sounds", font_size=14, color=ACCENT_COLOR, position="absolute", right=10, top=-20),
                        ],
                        td(margin_right=16, position="relative")[
                            number(pattern_data.get("threshold", {}).get(">power", "0")),
                            # text(",".join(pattern_data.get("sounds", "")), {"position": "absolute", "left": 2, "top": -25, "width": 200}),
                        ],
                        td()[text(">probability", font_size=14, color=ACCENT_COLOR)],
                        td(margin_right=16)[number(pattern_data.get("threshold", {}).get(">probability", "0"))],
                    ],
                    *[
                        tr()[
                            *[
                                item
                                for k, v in group
                                for item in [
                                    td()[
                                        div(flex_direction="row", gap=4, align_items="center")[
                                            icon("clock", size=14, color="FFCC00"),
                                            text(k, font_size=14, color=ACCENT_COLOR),
                                        ]
                                    ],
                                    td(margin_right=16)[number(v)],
                                ]
                            ]
                        ]
                        for group in throttle_groups
                    ]
                ],
            ]
        ],
        # div(flex_direction="row", margin=12)[
        #     key_val("Sounds", ", ".join(pattern_data.get("sounds", []))),
        # ],
        # # text("Threshold", margin_top=12),
        # table()[
        #     tr()[
        #         td()[key_val(">power", pattern_data.get("threshold", {}).get(">power", "0"))],
        #         td()[key_val(">probability", pattern_data.get("threshold", {}).get(">probability", "0"))],
        #     ],
        # ],
        # # text("Throttle", margin_top=12),
        # table()[
        #     *[tr()[
        #         *[td()[key_val(k, v)] for k, v in throttle],
        #     ] for throttle in throttle_groups],
        # ],
    ]

def detected_patterns():
    div, component, state, text = actions.user.ui_elements(["div", "component", "state", "text"])
    state = actions.user.ui_elements("state")

    # capture_updating = state.get("capture_updating", False)
    last_capture = state.get("last_capture", None)
    frames = last_capture.detect_frames if last_capture else []
    patterns = []
    seen = set()

    for frame in frames:
        for p in frame.patterns:
            name = p["name"]
            if name not in seen:
                patterns.append(name)
                seen.add(name)

    return div(height="100%")[
        text("Detected patterns", padding=16,font_size=20, border_bottom=1, border_color=BORDER_COLOR),
        div(flex_direction="column", overflow_y="scroll", height="100%", width=300)[
            *[div()[
                component(pattern, props={
                    "name": pattern_name
                })
            ] for pattern_name in patterns]
        ],
    ]

def noise_power_probability(props):
    state = actions.user.ui_elements("state")
    table, th, tr, td, style, text = actions.user.ui_elements(["table", "th", "tr", "td", "style", "text"])

    last_capture = state.get("last_capture", None)
    # print("last_capture", last_capture)
    detect_frames = last_capture.detect_frames if last_capture else []
    # print("detect_frames", detect_frames)
    style({
        "th": {
            "padding_bottom": 10,
            "padding_left": 12,
            "padding_right": 12,
        },
        "td": {
            "padding_left": 12,
            "padding_right": 12,
            "padding_bottom": 10,
        },
    })

    return table()[
        tr()[
            # th()[text("ts", font_size=14, color=ACCENT_COLOR)],
            th()[text("power", font_size=14, color=ACCENT_COLOR)],
            th()[text("probability", font_size=14, color=ACCENT_COLOR)],
            th()[text("noise", font_size=14, color=ACCENT_COLOR)],
        ],
        *[
            tr()[
                # td()[text(f"{frame.ts:.3f}", font_size=24)],
                td()[text(frame.format(frame.power), font_size=24)],
                td()[text(frame.format(frame.winner_probability), font_size=24)],
                td()[text(frame.winner_name, font_size=24)],
            ] for frame in detect_frames
        ],
    ]

def table_controls():
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    state = actions.user.ui_elements("state")

    return div(flex_direction="row", gap=16)[
        # button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, border_color=BORDER_COLOR, border_width=2, border_radius=4)[
        #     text("Capture time"),
        #     icon("chevron_down", size=14),
        # ],
        # button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, border_color=BORDER_COLOR, border_width=2, border_radius=4)[
        #     text("Filters"),
        #     icon("chevron_down", size=14),
        # ],
        button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, background_color="#292A2F", border_color=BORDER_COLOR, border_width=1, border_radius=4)[
            text("Columns"),
            icon("chevron_down", size=14),
        ],
    ]

def pattern_pill(name):
    div, text = actions.user.ui_elements(["div", "text"])

    pattern_color = get_pattern_color(name)
    return div(border_width=1, border_color=pattern_color, background_color=f"{pattern_color}33", padding=4, border_radius=4)[
        text(f"+ {name}", font_size=14)
    ]

def thunder_svg():
    svg, path = actions.user.ui_elements_svg(["svg", "path"])

    return svg(size=16, color="FFCC00")[
        path(d="M7 2v11h3v9l7-12h-4l4-8h-10z")
    ]

def textbox(text_str, props={}):
    div, text = actions.user.ui_elements(["div", "text"])

    return div(
        background_color="111111",
        flex_direction="row",
        align_items="center",
        padding=5,
        min_width=60,
        border_radius=2,
        border_width=1,
        border_color="000000",
        **props,
    )[
        text(text_str, font_size=14, color=SECONDARY_COLOR),
    ]

def override_pattern(props):
    div, text, icon, style, switch, state = actions.user.ui_elements(["div", "text", "icon", "style", "switch", "state"])
    table, tr, th, td = actions.user.ui_elements(["table", "tr", "th", "td"])

    is_open, set_is_open = state.use_local("is_open", False)
    pattern = get_pattern_json(props["name"])
    color = get_pattern_color(props["name"])

    style({
        "td": {
            "padding": 3,
            "padding_right": 10,
            "flex_direction": "row",
            "align_items": "center",
        },
    })

    throttles = pattern.get("throttle", {})
    throttle_items = list(throttles.items())
    throttle_groups = [throttle_items[i:i + 2] for i in range(0, len(throttle_items), 2)]

    return div()[
        div(
            flex_direction="row",
            justify_content="space_between",
            border_bottom=0 if is_open else 1,
            border_color=BORDER_COLOR,
            align_items="center",
            gap=16
        )[
            switch(checked=False, size=16, margin_left=12, on_change=lambda e: set_is_open(e.checked)),
            div(position="relative", flex_direction="row", justify_content="space_between", flex=1)[
                div(flex_direction="row", gap=8, align_items="center")[
                    rect_color(color, size=16),
                    text(props["name"], for_id="pattern_" + props["name"], padding=8, flex=1),
                ],
                div(flex_direction="row", align_items="center")[
                    icon("copy", size=20, color="999999", padding=8),
                    icon("rotate_left", size=16, color="999999", padding=8),
                ],
                # slightly muted if disabled
                div(position="absolute", width="100%", height="100%", background_color="292A2F88") if not is_open else None,
            ],
        ],
        div(justify_content="center", align_items="center")[
            table(padding=8, margin_top=24)[
                tr()[
                    td(justify_content="flex_end", position="relative")[
                        text(">power", font_size=14),
                        text("sounds", font_size=14, position="absolute", right=10, top=-20),
                    ],
                    td(margin_right=16, position="relative")[
                        textbox(pattern.get("threshold", {}).get(">power", "0")),
                        textbox(",".join(pattern.get("sounds", "")), {"position": "absolute", "left": 2, "top": -25, "width": 200}),
                    ],
                    td(justify_content="flex_end")[text(">probability", font_size=14)],
                    td(margin_right=16)[textbox(pattern.get("threshold", {}).get(">probability", "0"))],
                ],
                *[
                    tr()[
                        *[
                            item
                            for k, v in group
                            for item in [
                                td(justify_content="flex_end")[
                                    div(flex_direction="row", gap=4, align_items="center")[
                                        icon("clock", size=14, color="FFCC00"),
                                        text(k, font_size=14),
                                    ]
                                ],
                                td(margin_right=16)[textbox(v)],
                            ]
                        ]
                    ]
                    for group in throttle_groups
                ]
            ] if is_open else None,
        ],
    ]

    # table()[
    #         *[tr()[
    #             *[td()[key_val(k, v)] for k, v in throttle],
    #         ] for throttle in throttle_groups],
    #     ],

def pattern_pills(patterns_names):
    div, text = actions.user.ui_elements(["div", "text"])

    # iterate through patterns, count the characters for each name, and add to current line until we hit a limit
    # then start a new line
    # max_line_length = 20

    lines = []
    current_line = []
    current_line_length = 0
    max_line_length = 45
    for name in patterns_names:
        name_length = len(name)
        if current_line_length + name_length > max_line_length:
            lines.append(current_line)
            current_line = [name]
            current_line_length = name_length + 4
        else:
            current_line.append(name)
            current_line_length += name_length + 4

    lines.append(current_line)

    return div(flex_direction="column", gap=8, padding=16)[
        *[div(flex_direction="row", gap=8)[
            *[pattern_pill(name) for name in line]
        ] for line in lines]
    ]

def overrides_panel():
    div, text, icon, component, switch = actions.user.ui_elements(["div", "text", "icon", "component", "switch"])
    patterns = get_pattern_json()


    return div(overflow_y="scroll", width=400, background_color="#292A2F", border_left=1, border_color=BORDER_COLOR, height=750)[
        div(flex_direction="row", justify_content="space_between", align_items="center", border_bottom=1, border_color=BORDER_COLOR)[
            div(flex_direction="row", gap=8, align_items="center")[
                # switch(id="use_overrides", size=16, margin_left=12, on_change=lambda e: print("use_overrides", e.checked)),
                text("Draft pattern overrides", font_size=20, padding=16),
            ],
            # icon("rotate_left", size=16, color="999999", padding=16),
        ],
        # pattern_pills(patterns.keys()),
        *[component(override_pattern, props={
            "name": pattern_name,
        }) for pattern_name in patterns.keys()],
        # div(flex_direction="row", align_items="center", gap=16, padding=12, border_radius=4, border_width=1, border_color=BORDER_COLOR)[
        #     icon("chevron_right", size=16, color="999999"),
        #     text("Column visibility"),
        # ],
        # div(flex_direction="row", align_items="center", gap=16, padding=12, border_radius=4, border_width=1, border_color=BORDER_COLOR)[
        #     icon("chevron_right", size=16, color="999999"),
        #     text("Filters"),
        # ],
    ]

def page_detect_frames():
    div, component, text = actions.user.ui_elements(["div", "component", "text"])

    # patterns = get_pattern_json()

    # return div(flex_direction="column")[
    #     div(id="test_parent", flex_direction="column", gap=16, padding=16, width="100%")[
    #         div(id="test", flex_direction="row", gap=8, flex_wrap=True)[
    #             *[pattern_pill(p) for p in patterns.keys()],
    #         ],
    #         text("hello"),
    #     ],
    #     text("bottom"),
    # ]
    state = actions.user.ui_elements("state")
    capture_updating = state.get("capture_updating", False)

    return div(background_color="191B1F", flex_direction="row", height=750)[
        div(flex_direction="column", background_color="#292A2F", gap=16, height=750, border_right=1, border_color=BORDER_COLOR)[
            detected_patterns(),
        ],
        div(flex_direction="column", gap=16, flex=1)[
            div(position="relative", flex=1)[
                div(flex_direction="row", padding=16, justify_content="space_between", align_items="center")[
                    text("Frames", font_size=24),
                    legend(),
                    table_controls(),
                ],
                component(table_test),
                div(position="absolute", top=0, right=0)[
                    text("Updating...", font_size=14, padding=2)
                ] if capture_updating else None,
            ],
            # legend,
        ],
        # overrides_panel(),
    ]

def page_log():
    div = actions.user.ui_elements("div")

    return div(flex_direction="row", padding=16, gap=16, height="100%")[
        div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
            table_test,
        ]
    ]

def page_patterns():
    div, component, table, tr, td, style = actions.user.ui_elements(["div", "component", "table", "tr", "td", "style"])

    style({
        "td": {
            "padding": 8,
        }
    })

    return div(flex_direction="column", padding=8, height="100%")[
        table()[
            tr()[
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "pop",
                            "color": "73BF69",
                        }),
                    ]
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "guh",
                            "color": "FF7808",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "ah",
                            "color": "AA00FF",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "eh",
                            "color": "FF00FF",
                        }),
                    ],
                ],
            ],
            tr()[
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "oh",
                            "color": "C0C0C0",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "er",
                            "color": "00FFFF",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "t",
                            "color": "FFFF00",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "ss",
                            "color": "FF00FF",
                        }),
                    ],
                ],
            ],
            tr()[
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "mm",
                            "color": "FF0000",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "palate",
                            "color": "00FF00",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "sh",
                            "color": "0000FF",
                        }),
                    ],
                ],
                td()[
                    div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
                        component(pattern, props={
                            "name": "cluck",
                            "color": "94C8FF",
                        }),
                    ],
                ],
            ],
        ],
        # div(flex_direction="row", gap=16)[
        #     div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
        #         component(pattern, props={
        #             "name": "oh",
        #             "color": "C0C0C0",
        #         }),
        #     ],
        # ],
    ]

def page_timeline():
    div, component = actions.user.ui_elements(["div", "component"])

    return div(flex_direction="row", padding=16, gap=16, height="100%")[
        div(background_color="191B1F", flex=1, border_radius=4, padding=16, border_width=1, border_color=BORDER_COLOR)[
            component(graph_test),
        ]
    ]

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

tab_to_page = {
    "Frames": page_detect_frames,
    # "Log": page_log,
    # "Timeline": page_patterns,
    # "Stats": page_patterns,
    # "Patterns": page_patterns,
    "About": page_about,
}

def global_options():
    # a horizontal row of checkbox items for "Disable noise actions", "Allow pop action", and a switch for "Use overrides"
    div, checkbox, text, switch, button, icon = actions.user.ui_elements(["div", "checkbox", "text", "switch", "button", "icon"])

    return div(flex_direction="row", gap=24, align_items="center")[
        div(flex_direction="row", gap=8, align_items="center")[
            checkbox(id="disable_noise_actions"),
            text("Disable actions when listening", for_id="disable_noise_actions"),
        ],
        div(flex_direction="row", gap=8, align_items="center")[
            checkbox(id="allow_pop_action"),
            text("Allow pop action when listening", for_id="allow_pop_action"),
        ],
        button(padding=8, padding_left=12, padding_right=12, flex_direction="row", align_items="center", gap=4, border_color=BORDER_COLOR, border_width=2, border_radius=4)[
            text("Select play/stop noise"),
            icon("chevron_down", size=14),
        ],
    ]

def parrot_tester_new_ui():
    window, div, text, screen, button, icon, state, style, component = actions.user.ui_elements([
        "window", "div", "text", "screen", "button", "icon", "state", "style", "component"
    ])

    tab, set_tab = state.use("tab", "Frames")

    style({
        "*": {
            "highlight_color": "BBBBCC33",
            "focus_outline_color": "BBBBCC",
        },
        "text": {
            "color": "EEEEFF",
        }
    })

    return screen(justify_content="center", align_items="center")[
        window(title=HEADER_TEXT, on_close=parrot_tester_disable, flex_direction="column", width=1100, background_color="#191B1F", border_radius=8, border_width=1, border_color=WINDOW_BORDER_COLOR)[
            # Header Section
            div(flex_direction="row", align_items="flex_end", border_bottom=1, border_color=BORDER_COLOR, position="relative")[
                div(padding=16)[
                    play_button(),
                ],
                div(flex_direction="row", position="absolute", left=300, bottom=0)[
                    *[button(on_click=lambda e, l=label: set_tab(l), padding=16, position="relative")[
                        div(position="absolute", bottom=0, background_color=ACTIVE_COLOR, height=3, width="100%", border_radius=2) if tab == label else None,
                        text(label, font_size=16, color="FFFFFF")
                    ] for label in TABS]
                ],
                # div(flex_direction="row", gap=8, align_items="center")
                # [
                    # global_options,
                    # button(on_click=lambda e: print("Docs clicked"), border_radius=4, gap=8, padding=8, flex_direction="row", align_items="center")[
                    #     text(DOCS_BUTTON_TEXT, font_size=16, color="FFFFFF"),
                    #     icon("external_link", size=16)
                    # ],
                    # button(on_click=lambda e: print("Patterns clicked"), border_radius=4, gap=8, padding=8, flex_direction="row", align_items="center")[
                    #     text(PATTERNS_BUTTON_TEXT, font_size=16, color="FFFFFF"),
                    #     icon("file_text", size=16)
                    # ]
                # ]
            ],
            # Tabs Section

            div(height=750)[
                tab_to_page[tab](),
            ]
        ]
    ]