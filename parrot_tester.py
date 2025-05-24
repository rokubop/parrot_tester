
from talon import Module, actions
from .src.ui.parrot_tester_ui import parrot_tester_ui

mod = Module()
mod.tag("parrot_tester", "mode for testing parrot")

@mod.action_class
class Actions:
    def parrot_tester_toggle():
        """Toggle parrot tester"""
        actions.user.ui_elements_toggle(parrot_tester_ui, show_hints=False)

    def parrot_tester_wrap_parrot_integration():
        """Wrap parrot_integration file"""
        actions.skip()

    def parrot_tester_restore_parrot_integration():
        """Restore parrot_integration file"""
        actions.skip()