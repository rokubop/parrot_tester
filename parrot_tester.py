
from talon import Module, actions
from .ui.app import parrot_tester_toggle

mod = Module()
mod.tag("parrot_tester", "mode for testing parrot")

@mod.action_class
class Actions:
    def parrot_tester_toggle():
        """Toggle parrot tester"""
        parrot_tester_toggle()

    def parrot_tester_wrap_parrot_integration():
        """Wrap parrot_integration file for introspection - Automatically overwritten by context"""
        actions.skip()

    def parrot_tester_restore_parrot_integration():
        """Restore parrot_integration file - Automatically overwritten by context"""
        actions.skip()