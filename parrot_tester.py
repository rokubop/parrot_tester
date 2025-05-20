
from talon import Module
from .src.ui.parrot_tester_ui import (
    parrot_tester_toggle,
)

mod = Module()
mod.tag("parrot_tester", "mode for testing parrot")

@mod.action_class
class Actions:
    def parrot_tester_toggle():
        """Toggle parrot tester"""
        parrot_tester_toggle()