"""User project context for storage operations.

This module provides a context manager for setting a user/billing project that
storage backends can use for operations requiring project-based billing or access
control. The specific use of this context is backend-dependent:

- Google Cloud Storage: Used for requester-pays buckets
- Other providers: Can implement similar functionality as needed

The context variable approach allows the project to be set at the task level
without modifying storage backend APIs.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar

_user_project_id: ContextVar[str | None] = ContextVar('user_project_id', default=None)


def get_user_project() -> str | None:
    """Get the current user/billing project identifier.

    Returns the project identifier for the current context, which storage
    backends may use for billing or access control purposes.
    """
    return _user_project_id.get()


@contextmanager
def user_project_context(project_id: str | None) -> Generator[None]:
    """Set user/billing project context for storage operations.

    Args:
        project_id: Project identifier to use for billing/access control.
                   Interpretation is backend-specific.

    Example:
        with user_project_context('my-billing-project'):
            # Storage operations within this block will use the project
            handle.copy_to(destination)
    """
    if project_id is None:
        yield
        return

    token = _user_project_id.set(project_id)
    try:
        yield
    finally:
        _user_project_id.reset(token)
