from pathlib import Path
import os
import sys
import json
from talon import actions, cron
from talon.experimental.parrot import ParrotFrame
from talon_init import TALON_USER
from math import floor
from .constants import get_color

patterns_json = {}
is_listening = False

def get_talon_user_path():
    """Get the talon user path based on the platform."""
    if sys.platform == "win32":
        return os.path.join(os.getenv("APPDATA"), "talon", "user")
    else:
        return os.path.join(os.getenv("HOME"), ".talon", "user")

def get_parrot_integration_path():
    """Get the path to the parrot_integration.py file."""
    talon_user_path = get_talon_user_path()
    matches = list(Path(talon_user_path).rglob("parrot_integration.py"))

    for path in matches:
        print("Found parrot_integration.py:", path)

    return matches[0] if matches else None

def get_patterns_py_path():
    """Get the path to the patterns.py file."""
    talon_user_path = get_talon_user_path()
    matches = list(Path(talon_user_path).rglob("patterns.json"))

    for path in matches:
        print("Found patterns.json:", path)

    return matches[0] if matches else None

def load_patterns(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Failed to load patterns from {path}: {e}")
        return {}

def build_relative_import_path(current_file: Path, target_file: Path) -> str:
    # Root of all Talon scripts
    # user_root = Path.home() / ".talon" / "user"
    if not all(part.isidentifier() for part in target_file.parts):
        raise ValueError(f"Invalid import path - folder/file names must be valid Python identifiers: {target_file}")

    # Determine how many levels up we need to go from current file
    up_levels = len(current_file.parts) - 1
    dot_prefix = "." * up_levels if up_levels > 0 else "."

    # Module path: foo/bar/baz.py → foo.bar.baz
    target_module = ".".join(target_file.parts)

    return f"{dot_prefix}.{target_module}"

def truncate_stringify(x: float, decimals: int = 3) -> str:
    factor = 10 ** decimals
    truncated = floor(x * factor) / factor
    return f"{truncated:.{decimals}f}"

class ParrotTesterFrame:
    THRESHOLD_PROBABILITY = 0.1

    def __init__(self, frame: ParrotFrame):
        self.id = None
        self.index = None
        self.ts = frame.ts
        self.ts_delta = None
        self.ts_zero_based = None
        self.power = frame.power
        self.f0 = frame.f0
        self.f1 = frame.f1
        self.f2 = frame.f2
        self.patterns = []
        self.pattern_names = set()
        self.detected = False
        self.grace_detected = False

    def add_pattern(self, name: str, sounds: set[str], probability: float, detected: bool, throttled: bool, graceperiod: bool, color: str, grace_detected=bool):
        if probability > self.THRESHOLD_PROBABILITY:
            if detected:
                self.detected = True
            if grace_detected:
                self.grace_detected = True
            self.pattern_names.add(name)
            self.patterns.append({
                "name": name,
                "sounds": sounds,
                "probability": probability,
                "status": "grace_detected" if grace_detected else "detected" if detected else "throttled" if throttled else "",
                "graceperiod": graceperiod,
                "color": color,
            })

    def freeze(self):
        self.patterns = sorted(self.patterns, key=lambda x: x["probability"], reverse=True)

    def format(self, value: float, decimals: int = 3) -> str:
        if value is None:
            return ""
        return truncate_stringify(value, decimals)

    @property
    def winner(self):
        return self.patterns[0] if self.patterns else {}

    @property
    def winner_name(self):
        return self.winner.get("name", "")

    @property
    def winner_power_threshold(self):
        name = self.winner_name
        return patterns_json.get(name, {}).get("threshold", {}).get(">power", None)

    @property
    def winner_grace_power_threshold(self):
        name = self.winner_name
        return patterns_json.get(name, {}).get("grace_threshold", {}).get(">power", None)

    @property
    def winner_probability(self):
        return self.winner.get("probability", 0.0)

    @property
    def winner_status(self):
        return self.winner.get("status", "")

class Buffer:
    def __init__(self, size: int = 5):
        self.size = size
        self.buffer: list[ParrotTesterFrame] = []
        self.buffer_last: list[ParrotTesterFrame] = []
        self.get_time_window = 0.3

    def add(self, item):
        if len(self.buffer) > self.size:
            self.buffer_last = self.buffer.copy()
            self.buffer = []
        self.buffer.append(item)

    def get(self, current_ts: float) -> list[ParrotTesterFrame]:
        all = self.buffer_last + self.buffer
        # but dont include the last one
        all = all[:-1]
        # look at each frame.ts and get the last 0.3 seconds
        return [frame for frame in all if current_ts - frame.ts < self.get_time_window]

    def clear(self):
        """Clear the buffer."""
        self.buffer = []
        self.buffer_last = []

buffer = Buffer()

class Capture:
    def __init__(self, detect_frame: ParrotTesterFrame):
        self.frames = buffer.get(detect_frame.ts)
        self.frames.append(detect_frame)
        detect_frame_index = len(self.frames) - 1
        self._detect_frames = [(detect_frame, detect_frame_index)]
        self.pattern_names = set(detect_frame.pattern_names)

    @property
    def detect_frames(self):
        return [frame[0] for frame in self._detect_frames]

    @property
    def detected_pattern_names(self):
        patterns = []
        seen = set()

        for frame in self.detect_frames:
            for p in frame.patterns:
                name = p["name"]
                if name not in seen:
                    patterns.append(name)
                    seen.add(name)

        return patterns

    @property
    def other_pattern_names(self):
        return self.pattern_names - set(self.detected_pattern_names)

    def add_frame(self, frame: ParrotTesterFrame):
        self.frames.append(frame)
        self.pattern_names.update(frame.pattern_names)

    def add_detect_frame(self, frame: ParrotTesterFrame):
        self.frames.append(frame)
        detect_frame_index = len(self.frames) - 1
        self._detect_frames.append((frame, detect_frame_index))
        self.pattern_names.update(frame.pattern_names)

    def complete(self):
        for i, frame in enumerate(self.frames):
            frame.ts_delta = frame.ts - self.detect_frames[0].ts
            frame.ts_zero_based = frame.ts - self.frames[0].ts
            frame.id = i + 1
            frame.index = i

class CaptureCollection:
    capture_timeout = "350ms"
    max_frames_per_capture = 50

    def __init__(self):
        self.current_capture: Capture | None = None
        self.captures: list[Capture] = []
        self.end_current_capture_job = None

    def add(self, frame: ParrotTesterFrame, active: set[str]):
        new_capture = False
        if self.current_capture and len(self.current_capture.frames) >= self.max_frames_per_capture:
            self.end_current_capture()

        if active:
            if self.current_capture is None:
                new_capture = True
                self.current_capture = Capture(frame)
                self.captures.append(self.current_capture)
            else:
                self.current_capture.add_detect_frame(frame)
            if self.end_current_capture_job is not None:
                cron.cancel(self.end_current_capture_job)
            self.end_current_capture_job = cron.after(self.capture_timeout, self.end_current_capture)
        elif self.current_capture is not None:
            self.current_capture.add_frame(frame)

        if new_capture:
            actions.user.ui_elements_set_state("capture_updating", True)

    def end_current_capture(self):
        if self.current_capture is not None:
            self.current_capture.complete()
            self.current_capture = None
            if self.end_current_capture_job is not None:
                cron.cancel(self.end_current_capture_job)
            self.end_current_capture_job = None
            actions.user.ui_elements_set_state("last_capture", self.captures[-1])
            actions.user.ui_elements_set_state("capture_updating", False)

    def clear(self):
        self.captures = []
        self.current_capture = None
        if self.end_current_capture_job is not None:
            cron.cancel(self.end_current_capture_job)
            self.end_current_capture_job = None

capture_collection = CaptureCollection()
detected_log = []
log_events = False

def reset_capture_collection():
    global log_events
    buffer.clear()
    capture_collection.clear()
    detected_log.clear()
    log_events = False

def listen_log_events(enable: bool):
    global log_events
    log_events = enable

def determine_grace_detected(detect: bool, uses_grace_thresholds: bool, power: float, probability: float, pattern: dict) -> bool:
    if not detect:
        return False

    power_threshold = pattern.lowest_power_thresholds[0]
    grace_power_threshold = pattern.lowest_power_thresholds[1]
    if 0 < grace_power_threshold < power < power_threshold:
        return True

    return False

def is_grace_detected(pattern, frame) -> bool:
    grace_detected = False
    if pattern.timestamps.graceperiod_until and frame.ts < pattern.timestamps.graceperiod_until:
        if pattern.is_active(frame.ts) and pattern.match_pattern(pattern, frame, pattern.timestamps.graceperiod_until):
            grace_detected = True
    return grace_detected

def is_using_grace_thresholds_for_detection(pattern, frame):
    return frame.ts < pattern.timestamps.graceperiod_until

def force_normal_threshold_detection(pattern, frame):
    return pattern.match_pattern(pattern, frame, graceperiod_until=0)

def detect(pattern, frame):
    detected = pattern.detect(frame)
    grace_detected = False
    if detected and pattern.timestamps.graceperiod_until and \
            is_using_grace_thresholds_for_detection(pattern, frame):
        detection_normal = force_normal_threshold_detection(pattern, frame)
        if not detection_normal:
            grace_detected = True

    return detected, grace_detected

def wrap_pattern_match(parrot_delegate):
    pattern_index = {
        name: index for index, name in enumerate(parrot_delegate.patterns.keys())
    }

    def wrapper(frame: ParrotFrame):
        active: set[str] = set()
        parrot_tester_frame = ParrotTesterFrame(frame)
        buffer.add(parrot_tester_frame)

        for pattern in parrot_delegate.patterns.values():
            detected, grace_detected = detect(pattern, frame)
            graceperiod = pattern.timestamps.graceperiod_until > frame.ts
            probability = sum(frame.classes.get(label, 0) for label in pattern.labels)
            parrot_tester_frame.add_pattern(
                name=pattern.name,
                sounds=pattern.labels,
                probability=probability,
                detected=detected,
                grace_detected=grace_detected,
                throttled=pattern.timestamps.throttled_at > 0 and \
                    pattern.timestamps.throttled_until > frame.ts,
                graceperiod=graceperiod,
                color=get_color(pattern_index[pattern.name]),
            )

            if detected:
                active.add(pattern.name)
                throttles = pattern.get_throttles()
                parrot_delegate.throttle_patterns(throttles, frame.ts)
                detected_log.append(parrot_tester_frame)

        parrot_tester_frame.freeze()
        capture_collection.add(parrot_tester_frame, active)

        if active:
            for name in active:
                actions.user.ui_elements_highlight_briefly(f"pattern_{name}")
            if log_events:
                actions.user.ui_elements_set_state("detection_log", detected_log)

        return active
    return wrapper

original_pattern_match = None

def parrot_tester_wrap_parrot_integration(parrot_delegate):
    global original_pattern_match
    if original_pattern_match is None:
        original_pattern_match = parrot_delegate.pattern_match
        parrot_delegate.pattern_match = wrap_pattern_match(parrot_delegate)

# def parrot_tester_wrap_parrot_integration(parrot_delegate, file: str):
#     global original_pattern_match
#     if original_pattern_match is None:
#         with open(file, "r", encoding="utf-8") as f:
#             print("Wrapping pattern_integration.py")
#             original_pattern_match = parrot_delegate.pattern_match
#             parrot_delegate.pattern_match = wrap_pattern_match(parrot_delegate)
#             parrot_delegate.set_patterns(json.load(f))

def parrot_tester_restore_parrot_integration(parrot_delegate):
    global original_pattern_match
    if original_pattern_match is not None:
        parrot_delegate.pattern_match = original_pattern_match
        original_pattern_match = None

    reset_capture_collection()

# def parrot_tester_restore_parrot_integration(parrot_delegate, original_file: str):
#     """Restore pattern patterns."""
#     global original_pattern_match
#     if original_pattern_match is not None:
#         parrot_delegate.pattern_match = original_pattern_match
#         original_pattern_match = None

#     with open(original_file, "r", encoding="utf-8") as f:
#         parrot_delegate.set_patterns(json.load(f))
#         print("Restored pattern_integration.py")

#     reset_capture_collection()

def generate_parrot_integration_hook(import_path: str, current_file: Path):
    target_dir = current_file.parent.parent
    test_file = target_dir / "parrot_integration_hook.py"

    code = f"""\
# AUTO-GENERATED: Do not edit manually.
# This provides Talon access to parrot_delegate via actions,
# while preserving the integrity of the original source.
try:
    from talon import Context
    from {import_path} import parrot_delegate
    from .src.parrot_integration_wrapper import (
        parrot_tester_wrap_parrot_integration,
        parrot_tester_restore_parrot_integration
    )

    ctx = Context()

    @ctx.action_class("user")
    class Actions:
        def parrot_tester_wrap_parrot_integration():
            parrot_tester_wrap_parrot_integration(parrot_delegate)

        def parrot_tester_restore_parrot_integration():
            parrot_tester_restore_parrot_integration(parrot_delegate)
except ImportError:
    pass
"""

    test_file.write_text(code)
    print(f"✅ Wrote test file to {test_file}")

# def copy_patterns_to_generated(original_path: Path, generated_path: Path):
#     generated_path = generated_path / "patterns_draft.json"
#     try:
#         with original_path.open("r", encoding="utf-8") as f:
#             patterns = json.load(f)

#         # set power to 1
#         # for pattern in patterns.values():
#         #     for section in ("threshold", "grace_threshold"):
#         #         if section in pattern:
#         #             if ">power" in pattern[section]:
#         #                 pattern[section][">power"] = 1

#         with generated_path.open("w", encoding="utf-8") as f:
#             json.dump(patterns, f, indent=2)

#         print(f"✅ Copied patterns.json to: {generated_path}")
#         return patterns
#     except Exception as e:
#         print(f"❌ Failed to copy patterns.json: {e}")
#         return {}

def create_auto_generated_folder(generated_folder: Path):
    """Create the auto_generated folder if it doesn't exist."""
    try:
        generated_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created auto_generated folder: {generated_folder}")
    except Exception as e:
        print(f"❌ Failed to create auto_generated folder: {e}")

def get_pattern_json(name: str = None):
    """Get the pattern JSON for a specific name."""
    global patterns_json
    if patterns_json and name is not None:
        return patterns_json.get(name, {})
    return patterns_json

def get_pattern_color(name: str):
    try:
        index = list(patterns_json.keys()).index(name)
        return get_color(index)
    except:
        return "#FFFFFF"

def parrot_tester_initialize():
    """Test function to check if the paths are correct."""
    global patterns_json
    parrot_integration_path = get_parrot_integration_path().resolve()
    patterns_py_path = get_patterns_py_path().resolve()
    current_path = Path(__file__).resolve()

    current = Path(__file__).parent.resolve()
    target = Path(parrot_integration_path).resolve()
    user_root = Path(TALON_USER).resolve()

    current_rel = current.relative_to(user_root)
    target_rel = target.relative_to(user_root).with_suffix("")  # drop .py

    # print(f"current: {current}, target: {target}, user_root: {user_root}")
    # print(f"patterns_py_path: {patterns_py_path}")
    patterns_json = load_patterns(patterns_py_path)

    # print("TALON_USER:", TALON_USER)
    # print("current_path:", current_path)
    # print("parrot_integration_path:", parrot_integration_path)
    import_path = build_relative_import_path(current_rel, target_rel)
    # print(import_path)
    generate_parrot_integration_hook(import_path, current_path)
    actions.user.parrot_tester_wrap_parrot_integration()

    # print(f"Parrot Integration Path: {parrot_integration_path}")
    # print(f"Patterns.py Path: {patterns_py_path}")

def restore_patterns():
    """Restore the original patterns.json file."""
    actions.user.parrot_tester_restore_parrot_integration()
    patterns_json.clear()