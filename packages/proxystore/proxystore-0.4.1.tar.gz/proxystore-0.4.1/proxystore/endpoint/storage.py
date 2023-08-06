"""Storage interface for blobs."""
from __future__ import annotations

import collections
import enum
import os
import shutil
import sys
from typing import Deque
from typing import Iterator

if sys.version_info >= (3, 9):  # pragma: >=3.9 cover
    from collections.abc import MutableMapping
else:  # pragma: <3.9 cover
    from typing import MutableMapping

from proxystore.endpoint.exceptions import FileDumpNotAvailableError
from proxystore.endpoint.exceptions import ObjectSizeExceededError
from proxystore.utils import bytes_to_readable


class BlobLocation(enum.Enum):
    """Location of Blob."""

    MEMORY = 1
    """Blob is loaded in memory."""
    FILE = 2
    """Blob is stored on disk."""


class Blob:
    """Representation of entry in [`EndpointStorage`][proxystore.endpoint.storage.EndpointStorage].

    Args:
        key: Key associated with the blob.
        value: The blob being stored.
        filepath: Optional filepath for dumping the blob.
    """  # noqa: E501

    def __init__(
        self,
        key: str,
        value: bytes,
        filepath: str | None = None,
    ) -> None:
        self.key = key
        self.size = len(value)
        self._value: bytes | None = value
        self.filepath = filepath

    @property
    def location(self) -> BlobLocation:
        """Location of the blob."""
        return (
            BlobLocation.FILE if self._value is None else BlobLocation.MEMORY
        )

    @property
    def value(self) -> bytes:
        """Blob bytes."""
        if self._value is None:
            self.load()
        assert self._value is not None
        return self._value

    def delete_file(self) -> None:
        """Delete the file dump of the blob if it exists."""
        if self.filepath is not None and os.path.isfile(self.filepath):
            os.remove(self.filepath)

    def dump(self) -> None:
        """Dump the blob to disk."""
        if self.filepath is None:
            raise FileDumpNotAvailableError(
                'The blob was not initialized with a filepath '
                'to dump data to.',
            )
        assert self._value is not None
        with open(self.filepath, 'wb') as f:
            f.write(self._value)
        self._value = None

    def load(self) -> None:
        """Load the blob from disk."""
        if self._value is not None:
            return

        assert self.filepath is not None
        with open(self.filepath, 'rb') as f:
            self._value = f.read()
        self.delete_file()


class EndpointStorage(MutableMapping[str, bytes]):
    """Endpoint in-memory blob storage with filesystem fallback.

    Provides a dict-like storage of key-bytes pairs. Optionally, a maximum
    in-memory size for the data structure can be specified and least-recently
    used key-bytes pairs will be dumped to a file in a specified directory.

    Args:
        max_size: Optional maximum size in bytes for in-memory
            storage of blobs. If the memory limit is exceeded, least
            recently used blobs will be dumped to disk (if configured).
        max_object_size: Optional maximum size in bytes for any single blob.
        dump_dir: Optional directory to dump blobs to when `max_object_size`
            is reached.
    """

    def __init__(
        self,
        max_size: int | None = None,
        max_object_size: int | None = None,
        dump_dir: str | None = None,
    ) -> None:
        if (max_size is not None or dump_dir is not None) and (
            max_size is None or dump_dir is None
        ):
            raise ValueError(
                'Either both of max_size and dump_dir should be specified '
                'or neither.',
            )
        self.max_size = max_size
        self.max_object_size = max_object_size
        self.dump_dir = dump_dir

        if self.dump_dir is not None:
            os.makedirs(self.dump_dir, exist_ok=True)

        self._in_memory_size = 0
        self._blobs: dict[str, Blob] = {}

        # Only in-memory objects should be in this.
        # Recently used keys are appended to right side, LRU keys are
        # popped from left side.
        self._lru_queue: Deque[str] = collections.deque()

    def __getitem__(self, key: str) -> bytes:
        """Get bytes associated with key."""
        if key not in self._blobs:
            raise KeyError(key)

        blob = self._blobs[key]

        if blob.location == BlobLocation.MEMORY:
            # Move to right side because recently used
            self._lru_queue.remove(key)
            self._lru_queue.append(key)
            return blob.value

        self._make_space(blob.size)
        self._in_memory_size += blob.size
        blob.load()

        # Add to queue because it is back in memory
        self._lru_queue.append(key)

        return blob.value

    def __setitem__(self, key: str, value: bytes) -> None:
        """Set key to value.

        Raises:
            ValueError: If `value` is larger than `max_size`.
        """
        if (
            self.max_object_size is not None
            and len(value) > self.max_object_size
        ):
            raise ObjectSizeExceededError(
                f'Bytes value has size {bytes_to_readable(len(value))} which '
                f'exceeds the {bytes_to_readable(self.max_object_size)} '
                'object limit.',
            )
        if self.max_size is not None and len(value) > self.max_size:
            raise ObjectSizeExceededError(
                f'Bytes value has size {bytes_to_readable(len(value))} which '
                f'exceeds the {bytes_to_readable(self.max_size)} '
                'memory limit.',
            )
        filepath = (
            None if self.dump_dir is None else os.path.join(self.dump_dir, key)
        )
        blob = Blob(key, value, filepath)
        self._make_space(blob.size)
        self._blobs[key] = blob
        self._in_memory_size += blob.size
        self._lru_queue.append(key)

    def __delitem__(self, key: str) -> None:
        """Remove a key from the storage."""
        if key not in self._blobs:
            raise KeyError(key)

        blob = self._blobs.pop(key)
        assert blob is not None
        if blob.location == BlobLocation.MEMORY:
            self._in_memory_size -= blob.size
            self._lru_queue.remove(key)
        blob.delete_file()

    def __iter__(self) -> Iterator[str]:
        """Iterate over keys in the storage."""
        yield from self._blobs

    def __len__(self) -> int:
        """Return number of keys in the storage."""
        return len(self._blobs)

    def __contains__(self, key: object) -> bool:
        """Check if storage contains a key."""
        return key in self._blobs

    def clear(self) -> None:
        """Clear all keys in the storage."""
        keys = list(self._blobs.keys())
        for key in keys:
            del self._blobs[key]
        self._lru_queue.clear()

    def cleanup(self) -> None:
        """Clear all keys in the storage and remove the data dump."""
        if self.dump_dir is not None:
            shutil.rmtree(self.dump_dir)
        self._blobs.clear()

    def _fits(self, size: int) -> bool:
        """Check if there is `size` bytes available in the storage."""
        if self.max_size is None:
            return True

        assert size <= self.max_size
        return self._in_memory_size + size <= self.max_size

    def _make_space(self, size: int) -> None:
        """Demote LRU keys to the file dump until `size` bytes is clear."""
        while not self._fits(size) and len(self._lru_queue) > 0:
            lru_key = self._lru_queue.popleft()
            blob = self._blobs[lru_key]
            blob.dump()
            self._in_memory_size -= blob.size
