# AUTO-GENERATED: Do not edit manually.
# This provides Talon access to parrot_delegate via actions,
# while preserving the integrity of the original source.
try:
    from talon import Context
    from ...roku.roku_parrot_model.parrot_integration import parrot_delegate
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
