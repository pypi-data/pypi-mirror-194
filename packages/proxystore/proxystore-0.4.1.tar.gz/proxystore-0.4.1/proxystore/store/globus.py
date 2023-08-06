"""Globus Endpoint Implementation."""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from typing import Any
from typing import Callable
from typing import Collection
from typing import Generator
from typing import Iterator
from typing import NamedTuple
from typing import Pattern
from typing import Sequence

if sys.version_info >= (3, 9):  # pragma: >=3.9 cover
    from typing import Literal
else:  # pragma: <3.9 cover
    from typing_extensions import Literal

import globus_sdk

import proxystore.utils as utils
from proxystore.globus import get_proxystore_authorizer
from proxystore.globus import GlobusAuthFileError
from proxystore.serialize import serialize as default_serializer
from proxystore.store.base import Store

logger = logging.getLogger(__name__)
GLOBUS_MKDIR_EXISTS_ERROR_CODE = 'ExternalError.MkdirFailed.Exists'

SerializerT = Callable[[Any], bytes]


class GlobusEndpoint:
    """Globus endpoint representation.

    Args:
        uuid: UUID of Globus endpoint.
        endpoint_path: Path within endpoint to directory to use
            for storing objects.
        local_path: Local path (as seen by the host filesystem) that
            corresponds to the directory specified by `endpoint_path`.
        host_regex: String that matches the host where
            the Globus endpoint exists or regex pattern than can be used
            to match the host. The host pattern is needed so that proxies
            can figure out what the local endpoint is when they are resolved.
    """

    def __init__(
        self,
        uuid: str,
        endpoint_path: str,
        local_path: str | None,
        host_regex: str | Pattern[str],
    ) -> None:
        if not isinstance(uuid, str):
            raise TypeError('uuid must be a str.')
        if not isinstance(endpoint_path, str):
            raise TypeError('endpoint_path must be a str.')
        if not isinstance(local_path, str):
            raise TypeError('local_path must be a str.')
        if not (
            isinstance(host_regex, str) or isinstance(host_regex, Pattern)
        ):
            raise TypeError('host_regex must be a str or re.Pattern.')

        self.uuid = uuid
        self.endpoint_path = endpoint_path
        self.local_path = local_path
        self.host_regex = host_regex

    def __eq__(self, endpoint: object) -> bool:
        if not isinstance(endpoint, GlobusEndpoint):
            raise NotImplementedError
        if (
            self.uuid == endpoint.uuid
            and self.endpoint_path == endpoint.endpoint_path
            and self.local_path == endpoint.local_path
            and self.host_regex == endpoint.host_regex
        ):
            return True
        return False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(uuid='{self.uuid}', "
            f"endpoint_path='{self.endpoint_path}', "
            f"local_path='{self.local_path}', "
            f"host_regex='{self.host_regex}')"
        )


class GlobusEndpoints:
    """A collection of Globus endpoints.

    Args:
        endpoints: Iterable of
            [`GlobusEndpoints`][proxystore.store.globus.GlobusEndpoints]
            instances.

    Raises:
        ValueError: If `endpoints` has length 0 or if multiple endpoints with \
            the same UUID are provided.
    """

    def __init__(self, endpoints: Collection[GlobusEndpoint]) -> None:
        if len(endpoints) == 0:
            raise ValueError(
                'GlobusEndpoints must be passed at least one GlobusEndpoint '
                'object',
            )
        self._endpoints: dict[str, GlobusEndpoint] = {}
        for endpoint in endpoints:
            if endpoint.uuid in self._endpoints:
                raise ValueError(
                    'Cannot pass multiple GlobusEndpoint objects with the '
                    'same Globus endpoint UUID.',
                )
            self._endpoints[endpoint.uuid] = endpoint

    def __getitem__(self, uuid: str) -> GlobusEndpoint:
        try:
            return self._endpoints[uuid]
        except KeyError:
            raise KeyError(
                f'Endpoint with UUID {uuid} does not exist.',
            ) from None

    def __iter__(self) -> Iterator[GlobusEndpoint]:
        def _iterator() -> Generator[GlobusEndpoint, None, None]:
            yield from self._endpoints.values()

        return _iterator()

    def __len__(self) -> int:
        return len(self._endpoints)

    def __repr__(self) -> str:
        s = f'{self.__class__.__name__}(['
        s += ', '.join(str(ep) for ep in self._endpoints.values())
        s += '])'
        return s

    @classmethod
    def from_dict(
        cls: type[GlobusEndpoints],
        json_object: dict[str, dict[str, str]],
    ) -> GlobusEndpoints:
        """Construct an endpoints collection from a dictionary.

        Example:

            ```python
            {
              "endpoint-uuid-1": {
                "host_regex": "host1-regex",
                "endpoint_path": "/path/to/endpoint/dir",
                "local_path": "/path/to/local/dir"
              },
              "endpoint-uuid-2": {
                "host_regex": "host2-regex",
                "endpoint_path": "/path/to/endpoint/dir",
                "local_path": "/path/to/local/dir"
              }
            }
            ```
        """  # noqa: D412
        endpoints = []
        for uuid, params in json_object.items():
            endpoints.append(
                GlobusEndpoint(
                    uuid=uuid,
                    endpoint_path=params['endpoint_path'],
                    local_path=params['local_path'],
                    host_regex=params['host_regex'],
                ),
            )
        return GlobusEndpoints(endpoints)

    @classmethod
    def from_json(cls, json_file: str) -> GlobusEndpoints:
        """Construct a GlobusEndpoints object from a json file.

        The `dict` read from the JSON file will be passed to
        [`from_dict()`][proxystore.store.globus.GlobusEndpoints.from_dict] and
        should match the format expected by
        [`from_dict()`][proxystore.store.globus.GlobusEndpoints.from_dict].
        """
        with open(json_file) as f:
            data = f.read()
        return cls.from_dict(json.loads(data))

    def dict(self) -> dict[str, dict[str, str]]:
        """Convert the GlobusEndpoints to a dict.

        Note that the
        [`GlobusEndpoints`][proxystore.store.globus.GlobusEndpoints]
        object can be reconstructed by passing the `dict` to.
        [`from_dict()`][proxystore.store.globus.GlobusEndpoints.from_dict].
        """
        data = {}
        for endpoint in self:
            data[endpoint.uuid] = {
                'endpoint_path': endpoint.endpoint_path,
                'local_path': endpoint.local_path,
                'host_regex': endpoint.host_regex.pattern
                if isinstance(endpoint.host_regex, Pattern)
                else endpoint.host_regex,
            }
        return data

    def get_by_host(self, host: str) -> GlobusEndpoint:
        """Get endpoint by host.

        Searches the endpoints for a endpoint who's `host_regex` matches
        `host`.

        Args:
            host: Host to match.

        Returns:
            Globus endpoint.

        Raises:
            ValueError: If `host` does not match any of the endpoints.
        """
        for endpoint in self._endpoints.values():
            if re.fullmatch(endpoint.host_regex, host) is not None:
                return endpoint
        raise ValueError(f'Cannot find endpoint matching host {host}')


class GlobusStoreKey(NamedTuple):
    """Key to object in a GlobusStore."""

    filename: str
    """Unique object filename."""
    task_id: str
    """Globus transfer task ID for the file."""

    def __eq__(self, other: Any) -> bool:
        """Match keys by filename only.

        This is a hack around the fact that the task_id is not created until
        after the filename is so there can be a state where the task_id
        is empty.
        """
        if isinstance(other, tuple):
            return self[0] == other[0]
        return False

    def __ne__(self, other: Any) -> bool:
        # Match keys by filename only.
        return not self == other


class GlobusStore(Store[GlobusStoreKey]):
    """Globus backend class.

    The [`GlobusStore`][proxystore.store.globus.GlobusStore] is similar to a
    [`FileStore`][proxystore.store.file.FileStore] in that objects in the
    store are saved to disk but allows for the transfer of objects between two
    remote file systems. The two directories on the separate file systems are
    kept in sync via Globus transfers. The
    [`GlobusStore`][proxystore.store.globus.GlobusStore]
    is useful when moving data between hosts that have a Globus endpoint but
    may have restrictions that prevent the use of other store backends
    (e.g., ports cannot be opened for using a
    [`RedisStore`][proxystore.store.redis.RedisStore].

    Note:
        To use Globus for data transfer, Globus authentication needs to be
        performed otherwise an error will be raised. Authentication can be
        performed on the command line with `#!bash proxystore-globus-auth`.
        Authentication only needs to be performed once per system.

    Args:
        name: Name of the store instance.
        endpoints: Globus endpoints to keep in sync. If passed as a `dict`,
            the dictionary must match the format expected by
            [`GlobusEndpoints.from_dict()`][proxystore.store.globus.GlobusEndpoints.from_dict].
        polling_interval: Interval in seconds to check if Globus
            tasks have finished.
        sync_level: Globus transfer sync level.
        timeout: Timeout in seconds for waiting on Globus tasks.
        cache_size: Size of LRU cache (in # of objects). If 0,
            the cache is disabled. The cache is local to the Python process.
        stats: Collect stats on store operations.

    Raise:
        GlobusAuthFileError: If the Globus authentication file cannot be found.
        ValueError: If `endpoints` is of an incorrect type.
        ValueError: If the :code:`len(endpoints) != 2` because this
            implementation can currently only keep two endpoints in sync.
    """

    def __init__(
        self,
        name: str,
        *,
        endpoints: GlobusEndpoints
        | list[GlobusEndpoint]
        | dict[str, dict[str, str]],
        polling_interval: int = 1,
        sync_level: int
        | Literal['exists', 'size', 'mtime', 'checksum'] = 'mtime',
        timeout: int = 60,
        cache_size: int = 16,
        stats: bool = False,
    ) -> None:
        if isinstance(endpoints, GlobusEndpoints):
            self.endpoints = endpoints
        elif isinstance(endpoints, list):
            self.endpoints = GlobusEndpoints(endpoints)
        elif isinstance(endpoints, dict):
            self.endpoints = GlobusEndpoints.from_dict(endpoints)
        else:
            raise ValueError(
                'endpoints must be of type GlobusEndpoints or a list of '
                f'GlobusEndpoint. Got {type(endpoints)}.',
            )
        if len(endpoints) != 2:
            raise ValueError(
                'ProxyStore only supports two endpoints at a time',
            )
        self.polling_interval = polling_interval
        self.sync_level = sync_level
        self.timeout = timeout

        try:
            authorizer = get_proxystore_authorizer()
        except GlobusAuthFileError as e:
            raise GlobusAuthFileError(
                'Error loading Globus auth tokens. Complete the '
                'authentication process with the proxystore-globus-auth tool.',
            ) from e

        self._transfer_client = globus_sdk.TransferClient(
            authorizer=authorizer,
        )

        super().__init__(
            name,
            cache_size=cache_size,
            stats=stats,
            kwargs={
                # Pass endpoints as a dict to make kwargs JSON serializable
                'endpoints': self.endpoints.dict(),
                'polling_interval': self.polling_interval,
                'sync_level': self.sync_level,
                'timeout': self.timeout,
            },
        )

    def create_key(self, obj: Any) -> GlobusStoreKey:
        # We do not know task ID at the time we need a filename so we leave
        # task_id empty and update it later.
        return GlobusStoreKey(filename=utils.create_key(obj), task_id='')

    def _get_filepath(
        self,
        filename: str,
        endpoint: GlobusEndpoint | None = None,
    ) -> str:
        """Get filepath from filename.

        Args:
            filename: Name of file in Globus.
            endpoint: Optionally specify a GlobusEndpoint
                to get the filepath relative to. If not specified, the endpoint
                associated with the local host will be used.

        Returns:
            Full local path to file.
        """
        if endpoint is None:
            endpoint = self._get_local_endpoint()
        local_path = os.path.expanduser(endpoint.local_path)
        return os.path.join(local_path, filename)

    def _get_local_endpoint(self) -> GlobusEndpoint:
        """Get endpoint local to current host."""
        return self.endpoints.get_by_host(utils.hostname())

    def _validate_task_id(self, task_id: str) -> bool:
        """Validate key contains a real Globus task id."""
        try:
            self._transfer_client.get_task(task_id)
        except globus_sdk.TransferAPIError as e:
            if e.http_status == 400:
                return False
            raise e
        return True

    def _wait_on_tasks(self, *tasks: str) -> None:
        """Wait on list of Globus tasks."""
        for task in tasks:
            done = self._transfer_client.task_wait(
                task,
                timeout=self.timeout,
                polling_interval=self.polling_interval,
            )
            if not done:
                raise RuntimeError(
                    f'Task {task} did not complete within the timeout',
                )

    def _transfer_files(
        self,
        filenames: str | list[str],
        delete: bool = False,
    ) -> str:
        """Launch Globus Transfer to sync endpoints.

        Args:
            filenames: Filename or list of filenames to transfer.
                Note must be filenames, not filepaths.
            delete: If `True`, delete the filenames rather than syncing them.

        Returns:
            Globus Task UUID that can be used to check the status of the
            transfer.
        """
        src_endpoint = self._get_local_endpoint()
        dst_endpoints = [ep for ep in self.endpoints if ep != src_endpoint]
        assert len(dst_endpoints) == 1
        dst_endpoint = dst_endpoints[0]

        transfer_task: globus_sdk.DeleteData | globus_sdk.TransferData
        if delete:
            transfer_task = globus_sdk.DeleteData(
                self._transfer_client,
                endpoint=dst_endpoint.uuid,
            )
        else:
            transfer_task = globus_sdk.TransferData(
                self._transfer_client,
                source_endpoint=src_endpoint.uuid,
                destination_endpoint=dst_endpoint.uuid,
                sync_level=self.sync_level,
            )

        transfer_task['notify_on_succeeded'] = False
        transfer_task['notify_on_failed'] = False
        transfer_task['notify_on_inactive'] = False

        if isinstance(filenames, str):
            filenames = [filenames]

        for filename in filenames:
            if isinstance(transfer_task, globus_sdk.DeleteData):
                transfer_task.add_item(
                    path=os.path.join(dst_endpoint.endpoint_path, filename),
                )
            elif isinstance(transfer_task, globus_sdk.TransferData):
                transfer_task.add_item(
                    source_path=os.path.join(
                        src_endpoint.endpoint_path,
                        filename,
                    ),
                    destination_path=os.path.join(
                        dst_endpoint.endpoint_path,
                        filename,
                    ),
                )
            else:
                raise AssertionError('Unreachable.')

        tdata = _submit_transfer_action(self._transfer_client, transfer_task)
        return tdata['task_id']

    def close(self) -> None:
        """Cleanup directories used by ProxyStore in the Globus endpoints.

        Warning:
            Will delete the directory at `local_path` on each endpoint.

        Warning:
            This method should only be called at the end of the program when
            the store will no longer be used, for example once all proxies
            have been resolved.
        """
        for endpoint in self.endpoints:
            delete_task = globus_sdk.DeleteData(
                self._transfer_client,
                endpoint=endpoint.uuid,
                recursive=True,
            )
            delete_task['notify_on_succeeded'] = False
            delete_task['notify_on_failed'] = False
            delete_task['notify_on_inactive'] = False
            delete_task.add_item(endpoint.endpoint_path)
            tdata = _submit_transfer_action(self._transfer_client, delete_task)
            self._wait_on_tasks(tdata['task_id'])

    def evict(self, key: GlobusStoreKey) -> None:
        if not self.exists(key):
            return

        path = self._get_filepath(key.filename)
        os.remove(path)
        self._cache.evict(key)
        self._transfer_files(key.filename, delete=True)
        logger.debug(
            f"EVICT key='{key}' FROM {self.__class__.__name__}"
            f"(name='{self.name}')",
        )

    def exists(self, key: GlobusStoreKey) -> bool:
        if not self._validate_task_id(key.task_id):
            return False
        self._wait_on_tasks(key.task_id)
        return os.path.exists(self._get_filepath(key.filename))

    def get_bytes(self, key: GlobusStoreKey) -> bytes | None:
        if not self.exists(key):
            return None

        path = self._get_filepath(key.filename)
        with open(path, 'rb') as f:
            return f.read()

    def set_bytes(self, key: GlobusStoreKey, data: bytes) -> None:
        path = self._get_filepath(key.filename)
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb', buffering=0) as f:
            f.write(data)

    def set(
        self,
        obj: Any,
        *,
        serializer: SerializerT | None = None,
    ) -> GlobusStoreKey:
        if serializer is not None:
            obj = serializer(obj)
        else:
            obj = default_serializer(obj)

        if not isinstance(obj, bytes):
            raise TypeError('Serializer must produce bytes.')

        temp_key = self.create_key(obj)
        self.set_bytes(temp_key, obj)
        tid = self._transfer_files(temp_key.filename)
        key = temp_key._replace(task_id=tid)

        logger.debug(
            f"SET key='{key}' IN {self.__class__.__name__}"
            f"(name='{self.name}')",
        )
        return key

    def set_batch(
        self,
        objs: Sequence[Any],
        *,
        serializer: SerializerT | None = None,
    ) -> list[GlobusStoreKey]:
        temp_keys = []
        for obj in objs:
            if serializer is not None:
                obj = serializer(obj)
            else:
                obj = default_serializer(obj)

            if not isinstance(obj, bytes):
                raise TypeError('Serializer must produce bytes.')

            temp_key = self.create_key(obj)
            temp_keys.append(temp_key)
            self.set_bytes(temp_key, obj)

        # Batch of objs written to disk so we can trigger Globus transfer
        tid = self._transfer_files([k.filename for k in temp_keys])

        keys = [key._replace(task_id=tid) for key in temp_keys]
        logger.debug(
            f"SET keys='{keys}' IN {self.__class__.__name__}"
            f"(name='{self.name}')",
        )

        return keys


def _submit_transfer_action(
    client: globus_sdk.TransferClient,
    task: globus_sdk.DeleteData | globus_sdk.TransferData,
) -> globus_sdk.response.GlobusHTTPResponse:
    """Submit Globus transfer task via the client.

    This helper function primarily adds some additional feedback on raised
    exceptions.

    Args:
        client: Globus transfer client.
        task: Globus transfer task.

    Returns:
        A `GlobusHTTPResponse`.
    """
    try:
        if isinstance(task, globus_sdk.DeleteData):
            return client.submit_delete(task)
        elif isinstance(task, globus_sdk.TransferData):
            return client.submit_transfer(task)
        else:
            raise AssertionError('Unreachable.')
    except globus_sdk.TransferAPIError as e:  # pragma: no cover
        # https://github.com/globus/globus-sdk-python/blob/054a29167c86f66b77bb99beca45ce317b02a5a7/src/globus_sdk/exc/err_info.py#L93  # noqa: E501
        raise Exception(
            f'Failure initiating Globus Transfer. Error info: {e.info}',
        ) from e
