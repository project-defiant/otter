"""Tests for the copy task."""

from unittest.mock import MagicMock, patch

from otter.scratchpad.model import Scratchpad
from otter.task.model import TaskContext
from otter.tasks.copy import Copy, CopySpec
from test.mocks import fake_config


class TestCopyTask:
    def test_spec_defaults_to_no_project_id(self) -> None:
        spec = CopySpec(
            name='copy test copy',
            source='gs://source-bucket/source.txt',
            destination='dest.txt',
        )

        assert spec.project_id is None

    def test_run_uses_project_id_context(self) -> None:
        spec = CopySpec(
            name='copy test copy',
            source='gs://source-bucket/source.txt',
            destination='dest.txt',
            project_id='billing-project',
        )
        task = Copy(spec, TaskContext(config=fake_config(), scratchpad=Scratchpad()))

        src_handle = MagicMock()
        src_handle.absolute = 'gs://source-bucket/source.txt'
        dst_handle = MagicMock()
        dst_handle.absolute = 'gs://test-bucket/release/path/dest.txt'

        with (
            patch('otter.tasks.copy.requester_pays_project') as mock_project_context,
            patch('otter.tasks.copy.StorageHandle') as mock_storage_handle,
        ):
            mock_storage_handle.side_effect = [src_handle, dst_handle]

            task.run()

        mock_project_context.assert_called_once_with('billing-project')
        src_handle.copy_to.assert_called_once_with(dst_handle)

    def test_validate_uses_project_id_context(self) -> None:
        spec = CopySpec(
            name='copy test copy',
            source='gs://source-bucket/source.txt',
            destination='dest.txt',
            project_id='billing-project',
        )
        task = Copy(spec, TaskContext(config=fake_config(), scratchpad=Scratchpad()))

        with (
            patch('otter.tasks.copy.requester_pays_project') as mock_project_context,
            patch('otter.tasks.copy.file.exists') as mock_exists,
            patch('otter.tasks.copy.file.size') as mock_size,
        ):
            task.validate()

        mock_project_context.assert_called_once_with('billing-project')
        mock_exists.assert_called_once()
        mock_size.assert_called_once()
