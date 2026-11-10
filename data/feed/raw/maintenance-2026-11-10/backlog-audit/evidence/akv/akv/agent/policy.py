"""Compose independent Drop triggers, message selectors, and Reposition rules."""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

from .policies.utils.context import PolicyContext
from .policies.utils.request import (
    check_cache_operation_history,
    parse_actions,
    prefix_digest,
    prepare_payload,
    read_request,
)
from .types import CacheAction, CacheOperation, CacheOperationHistory, JsonDict, PolicyRequest

DropTrigger = Callable[[PolicyContext], bool]
MessageSelector = Callable[[PolicyContext], set[int]]
RepositionRule = Callable[[PolicyContext, set[int]], bool]


@dataclass(frozen=True, kw_only=True)
class CachePolicy:
    """Combine three callables; omitted components choose no operation.

    The caller owns message history and cache operation history. Shared helpers
    parse and validate requests; this class evaluates decisions and records them.
    """

    trigger: DropTrigger | None = None
    selector: MessageSelector | None = None
    reposition: RepositionRule | None = None

    def __post_init__(self) -> None:
        for name in ("trigger", "selector", "reposition"):
            value = getattr(self, name)
            if value is not None and not callable(value):
                raise TypeError(f"{name} must be callable or None")

    def current_actions(
        self, request: PolicyRequest, cache_operation_history: CacheOperationHistory
    ) -> CacheAction:
        context = PolicyContext(request, cache_operation_history)
        selected = set()
        if self.trigger is not None and self.trigger(context) and self.selector is not None:
            selected = self.selector(context)
        reposition = self.reposition(context, selected) if self.reposition is not None else False
        return CacheAction(tuple(selected), reposition)

    def process(
        self,
        payload: Mapping[str, Any],
        *,
        cache_operation_history: CacheOperationHistory | None = None,
        options: Mapping[str, Any] | None = None,
        actions: CacheAction | Mapping[str, Any] | None = None,
        api_style: str | None = None,
        completed_call_message_ids: Sequence[int] | None = None,
    ) -> tuple[JsonDict, CacheOperationHistory]:
        """Return the adapted payload and updated cache operation history.

        Run the three decisions for new messages and preserve earlier operations.
        """
        if actions is not None and options is not None:
            raise ValueError("Pass either component options or explicit actions, not both")
        current = replace(self, **options) if options is not None else self
        cache_operation_history = (
            CacheOperationHistory() if cache_operation_history is None else cache_operation_history
        )
        request = read_request(
            payload,
            api_style=api_style,
            completed_call_message_ids=completed_call_message_ids,
        )
        context_digest = check_cache_operation_history(payload, request, cache_operation_history)
        size = len(request.messages)
        if actions is None:
            actions = (
                current.current_actions(request, cache_operation_history)
                if size > cache_operation_history.message_count
                else CacheAction()
            )
        hidden = {i for op in cache_operation_history.operations for i in op.drop_message_ids}
        selected, reposition = parse_actions(actions, size, hidden)
        if size > cache_operation_history.message_count:
            operations = cache_operation_history.operations
            if selected or reposition:
                operations = (*operations, CacheOperation(size - 1, tuple(selected), reposition))
            cache_operation_history = CacheOperationHistory(
                operations, size, prefix_digest(request, size), context_digest
            )
        return prepare_payload(payload, cache_operation_history), cache_operation_history
