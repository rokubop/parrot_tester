from pathlib import Path
from talon import actions
from talon_init import TALON_USER
from .ui.colors import get_color
from .parrot_integration_paths import (
    get_parrot_integration_path,
    get_patterns_py_path,
    load_patterns,
    build_relative_import_path,
    generate_parrot_integration_hook,
)

patterns_json = {}

def parrot_tester_initialize():
    """Test function to check if the paths are correct."""
    print("**** Starting Parrot Tester ****")

    try:
        parrot_integration_path = get_parrot_integration_path().resolve()
        patterns_py_path = get_patterns_py_path().resolve()
        current_path = Path(__file__).resolve()

        current = Path(__file__).parent.resolve()
        target = Path(parrot_integration_path).resolve()
        user_root = Path(TALON_USER).resolve()

        current_rel = current.relative_to(user_root)
        target_rel = target.relative_to(user_root).with_suffix("")

        patterns_data = load_patterns(patterns_py_path)
        set_patterns_json(patterns_data)

        import_path = build_relative_import_path(current_rel, target_rel)
        generate_parrot_integration_hook(import_path, current_path)
        actions.user.parrot_tester_wrap_parrot_integration()

    except ValueError as e:
        # This catches our detailed error message about invalid paths
        print(str(e))
        return
    except Exception as e:
        print(f"❌ PARROT TESTER ERROR: Failed to initialize: {e}")
        return

def restore_patterns_paused():
    actions.user.parrot_tester_restore_parrot_integration()

def restore_patterns():
    actions.user.parrot_tester_restore_parrot_integration()
    clear_patterns_json()

def get_pattern_color(name: str):
    global_patterns = get_patterns_json()
    try:
        index = list(global_patterns.keys()).index(name)
        return get_color(index)
    except:
        return "#FFFFFF"

def get_pattern_threshold_value(name: str, key: str):
    """Get a specific value from the pattern JSON."""
    global_patterns = get_patterns_json()
    if global_patterns and name in global_patterns:
        return global_patterns[name].get("threshold", {}).get(key, None)
    return None


def get_pattern_json(name: str = None):
    """Get the pattern JSON for a specific name."""
    global_patterns = get_patterns_json()
    # print(f"Pattern JSON: {json.dumps(global_patterns)}")
    # print(f"Getting pattern JSON for name: {name}")
    # print(f"Pattern JSON:", global_patterns)
    if global_patterns:
        return global_patterns.get(name, {})
    return {}

def get_patterns_json():
    """Get the patterns JSON."""
    global patterns_json
    if not patterns_json:
        patterns_py_path = get_patterns_py_path()
        if patterns_py_path:
            patterns_py_path = patterns_py_path.resolve()
            patterns_json = load_patterns(patterns_py_path)
        else:
            patterns_json = {}
    return patterns_json

def clear_patterns_json():
    """Clear the patterns JSON cache."""
    global patterns_json
    patterns_json.clear()

def set_patterns_json(data: dict):
    """Set the patterns JSON data."""
    global patterns_json
    patterns_json = data