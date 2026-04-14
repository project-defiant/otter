"""Requester-pays context helpers for GCS operations."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generator

_requester_pays_project_id: ContextVar[str | None] = ContextVar('requester_pays_project_id', default=None)


def get_requester_pays_project_id() -> str | None:
    """Get the current requester-pays billing project id."""
    return _requester_pays_project_id.get()


@contextmanager
def requester_pays_project(project_id: str | None) -> Generator[None, None, None]:
    """Temporarily set requester-pays billing project id for storage operations."""
    if project_id is None:
        yield
        return

    token = _requester_pays_project_id.set(project_id)
    try:
        yield
    finally:
        _requester_pays_project_id.reset(token)
