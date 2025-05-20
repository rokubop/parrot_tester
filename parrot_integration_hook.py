# AUTO-GENERATED: Do not edit manually.
# This provides Talon access to parrot_delegate via actions,
# while preserving the integrity of the original source.
try:
    from talon import Module
    from ...roku.roku_parrot_model.parrot_integration import parrot_delegate
    from .src.core import (
        parrot_tester_wrap_parrot_integration,
        parrot_tester_restore_parrot_integration
    )

    mod = Module()

    @mod.action_class
    class Actions:
        def parrot_tester_wrap_parrot_integration():
            """Wrap parrot_integration file"""
            parrot_tester_wrap_parrot_integration(parrot_delegate)

        def parrot_tester_restore_parrot_integration():
            """Restore parrot_integration file"""
            parrot_tester_restore_parrot_integration(parrot_delegate)
except ImportError:
    pass
