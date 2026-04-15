"""Storage model definitions."""

from dataclasses import dataclass

from pydantic import BaseModel, Field

Revision = float | str | None
"""Type alias for file revision identifiers."""


class GoogleStorageSettings(BaseModel):
    """Settings model for Google Cloud Storage context.

    Defines the allowed context parameters that can be used with Google Cloud Storage
    operations. These settings are passed via the storage_context() context manager.

    Attributes:
        user_project: Google Cloud project ID to use for requester-pays bucket access.
                     When accessing requester-pays buckets, this project will be billed
                     for the API requests and data egress costs.

    Example:
        with storage_context(user_project='my-billing-project'):
            # Operations on requester-pays buckets will bill to 'my-billing-project'
            handle.copy_to(destination)
    """

    user_project: str | None = Field(
        default=None,
        description='Project ID for requester-pays bucket billing',
    )


@dataclass
class StatResult:
    """Dataclass representing file metadata."""

    is_dir: bool
    """Whether the resource is a directory."""
    is_reg: bool
    """Whether the resource is a regular file."""
    size: int | None = None
    """The resource size in bytes, `None` if unknown."""
    revision: Revision = None
    """The resource revision identifier."""
    mtime: float | None = None
    """The resource modification time as a Unix timestamp, `None` if unknown."""
