import abc
import asyncio
import logging
from collections import deque
from concurrent.futures import Future
from typing import List, Optional, Sequence, Union

from uqbar.objects import new

from ..osc import BUNDLE_PREFIX, OscBundle
from ..system import SupriyaValueObject

logger = logging.getLogger("supriya.osc")


class Requestable(SupriyaValueObject):
    ### PRIVATE METHODS ###

    def _get_response_patterns_and_requestable(self, server):
        raise NotImplementedError

    def _handle_async(self, sync, server):
        raise NotImplementedError

    def _linearize(self):
        raise NotImplementedError

    def _sanitize_node_id(self, node_id, with_placeholders):
        if not isinstance(node_id, int) and with_placeholders:
            return -1
        return int(node_id)

    ### PUBLIC METHODS ###

    def communicate(self, server, sync=True, timeout=1.0, apply_local=True):
        if apply_local:
            with server._lock:
                for request in self._linearize():
                    request._apply_local(server)
        if self._handle_async(sync, server):
            return
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        future = Future()
        server._osc_protocol.register(
            pattern=success_pattern,
            failure_pattern=failure_pattern,
            procedure=lambda message: future.set_result(
                Response.from_osc_message(message)
            ),
            once=True,
        )
        server.send(requestable.to_osc())
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            logger.warning("Timed out: {!r}".format(self))
            return None

    async def communicate_async(self, server, sync=True, timeout=1.0):
        (
            success_pattern,
            failure_pattern,
            requestable,
        ) = self._get_response_patterns_and_requestable(server)
        if self._handle_async(sync, server):
            return
        future = asyncio.get_running_loop().create_future()
        server._osc_protocol.register(
            pattern=success_pattern,
            failure_pattern=failure_pattern,
            procedure=lambda message: future.set_result(
                Response.from_osc_message(message)
            ),
            once=True,
        )
        server.send(requestable.to_osc())
        await asyncio.wait_for(future, timeout=timeout)
        return future.result()

    def to_datagram(self, *, with_placeholders=False):
        return self.to_osc(with_placeholders=with_placeholders).to_datagram()

    def to_list(self, *, with_placeholders=False):
        return self.to_osc(with_placeholders=with_placeholders).to_list()

    @abc.abstractmethod
    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError


class Request(Requestable):
    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        pass

    def _get_response_patterns_and_requestable(self, server):
        success_pattern, failure_pattern = self.response_patterns
        return success_pattern, failure_pattern, self

    def _handle_async(self, sync, server):
        if not sync or self.response_patterns[0] is None:
            message = self.to_osc()
            server.send(message)
            return True

    def _linearize(self):
        if hasattr(self, "callback") and self.callback:
            yield new(self, callback=None)
            yield from self.callback._linearize()
        else:
            yield self

    ### PUBLIC METHODS ###

    @classmethod
    def merge(cls, requests: List["Request"]) -> List["Request"]:
        return requests

    ### PUBLIC PROPERTIES ###

    @property
    def request_name(self):
        return self.request_id.request_name

    @property
    def response_patterns(self):
        return None, None

    @property
    @abc.abstractmethod
    def request_id(self):
        return NotImplementedError


class RequestBundle(Requestable):
    """
    A Request bundle.

    ::

        >>> request_one = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=1,
        ... )
        >>> request_two = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=24,
        ...     frame_count=512,
        ...     channel_count=1,
        ... )
        >>> request_bundle = supriya.commands.RequestBundle(
        ...     timestamp=10.5,
        ...     contents=[request_one, request_two],
        ... )

    ::

        >>> request_bundle.to_osc()
        OscBundle(
            contents=(
                OscMessage('/b_alloc', 23, 512, 1),
                OscMessage('/b_alloc', 24, 512, 1),
            ),
            timestamp=10.5,
        )

    ::

        >>> request_bundle.to_list()
        [10.5, [['/b_alloc', 23, 512, 1], ['/b_alloc', 24, 512, 1]]]
    """

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp: Optional[float] = None,
        contents: Optional[Sequence[Union[Request, "RequestBundle"]]] = None,
    ) -> None:
        self._timestamp = timestamp
        if contents is not None:
            prototype = (Request, type(self))
            assert all(isinstance(x, prototype) for x in contents)
            contents = tuple(contents)
        else:
            contents = ()
        self._contents = contents

    ### PRIVATE METHODS ###

    def _get_response_patterns_and_requestable(self, server):
        from .server import SyncRequest

        sync_id = server.next_sync_id
        contents = list(self.contents)
        contents.append(SyncRequest(sync_id=sync_id))
        request_bundle = type(self)(contents=contents)
        response_pattern = ["/synced", sync_id]
        return response_pattern, None, request_bundle

    def _handle_async(self, sync, server):
        if not sync:
            message = self.to_osc()
            server.send(message)
            return True

    def _linearize(self):
        for x in self.contents:
            yield from x._linearize()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        contents = []
        for x in self.contents:
            if isinstance(x, type(self)):
                contents.append(x.to_osc(with_placeholders=with_placeholders))
            else:
                contents.append(x.to_osc(with_placeholders=with_placeholders))
        bundle = OscBundle(timestamp=self.timestamp, contents=contents)
        return bundle

    @classmethod
    def partition(cls, requests, timestamp=None):
        bundles = []
        contents = []
        requests = deque(requests)
        remaining = maximum = 8192 - len(BUNDLE_PREFIX) - 4
        while requests:
            request = requests.popleft()
            datagram = request.to_datagram()
            remaining -= len(datagram) + 4
            if remaining > 0:
                contents.append(request)
            else:
                bundles.append(cls(timestamp=timestamp, contents=contents))
                contents = [request]
                remaining = maximum
        if contents:
            bundles.append(cls(timestamp=timestamp, contents=contents))
        return bundles

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp


class Response(SupriyaValueObject):
    ### PRIVATE METHODS ###

    @staticmethod
    def _group_items(items, length):
        iterators = [iter(items)] * length
        iterator = zip(*iterators)
        return iterator

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, message):
        import supriya.commands

        return {
            "/b_info": supriya.commands.BufferInfo,
            "/b_set": supriya.commands.BufferSetResponse,
            "/b_setn": supriya.commands.BufferSetContiguousResponse,
            "/c_set": supriya.commands.ControlBusSetResponse,
            "/c_setn": supriya.commands.ControlBusSetContiguousResponse,
            "/d_removed": supriya.commands.SynthDefRemovedResponse,
            "/done": supriya.commands.DoneResponse,
            "/fail": supriya.commands.FailResponse,
            "/g_queryTree.reply": supriya.commands.QueryTreeResponse,
            "/n_end": supriya.commands.NodeInfo,
            "/n_go": supriya.commands.NodeInfo,
            "/n_info": supriya.commands.NodeInfo,
            "/n_move": supriya.commands.NodeInfo,
            "/n_off": supriya.commands.NodeInfo,
            "/n_on": supriya.commands.NodeInfo,
            "/n_set": supriya.commands.NodeSetResponse,
            "/n_setn": supriya.commands.NodeSetContiguousResponse,
            "/status.reply": supriya.commands.StatusResponse,
            "/synced": supriya.commands.SyncedResponse,
            "/tr": supriya.commands.TriggerResponse,
        }[message.address].from_osc_message(message)

    def to_dict(self):
        result = {}
        for key, value in self.__getstate__().items():
            key = key[1:]
            if key == "osc_message":
                continue
            result[key] = value
        return result
