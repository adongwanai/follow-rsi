"""Independent retention selectors and their shared message calculations."""

from dataclasses import dataclass

from ..types import ChatTokenCounter, PolicyRequest
from .tools import CacheTool, tool_actions
from .utils.common import positive_integer
from .utils.context import PolicyContext


def check_target(target: str) -> None:
    if target not in ("tool", "assistant", "both"):
        raise ValueError("target must be tool, assistant, or both")


@dataclass(frozen=True)
class TurnSelection:
    """Select older messages for Drop while retaining the latest ``count`` complete turns."""

    count: int
    target: str = "tool"

    def __post_init__(self) -> None:
        positive_integer(self.count, "count")
        check_target(self.target)

    def __call__(self, context: PolicyContext) -> set[int]:
        boundaries = context.request.completed_call_message_ids
        cutoff = boundaries[-self.count - 1] if len(boundaries) > self.count else -1
        tools = {i for unit in context.request.message_units for i in unit[1:]}
        hidden = context.hidden
        expired = (tools & hidden) | {i for i in tools if i <= cutoff}
        return expired_messages(context.request, expired, self.target) - hidden


@dataclass(frozen=True)
class TokenSelection:
    """Select older messages for Drop using a retained-token budget of ``tokens``."""

    tokens: int
    counter: ChatTokenCounter
    target: str = "tool"

    def __post_init__(self) -> None:
        positive_integer(self.tokens, "tokens")
        check_target(self.target)

    def __call__(self, context: PolicyContext) -> set[int]:
        tools = {i for unit in context.request.message_units for i in unit[1:]}
        hidden = context.hidden
        expired, selected = tools & hidden, set()
        remaining = context.layout(self.counter).prompt_tokens - context.tokens(self.counter, hidden)
        for i in sorted(tools - hidden):
            if remaining <= self.tokens:
                break
            expired.add(i)
            next_selected = expired_messages(context.request, expired, self.target) - hidden
            remaining -= context.tokens(self.counter, next_selected - selected)
            selected = next_selected
        return selected


def expired_messages(request: PolicyRequest, expired: set[int], target: str) -> set[int]:
    """An assistant expires after every result in its tool batch has expired."""
    selected = set(expired) if target in ("tool", "both") else set()
    if target == "tool":
        return selected
    pending = []
    for unit in request.message_units:
        assistant, *results = unit
        if request.messages[assistant]["role"] != "assistant":
            continue
        pending.append(assistant)
        if results:
            if all(i in expired for i in results):
                selected.update(pending)
            pending = []
    return selected


@dataclass(frozen=True)
class ModelSelection:
    tool: CacheTool

    def __call__(self, context: PolicyContext) -> set[int]:
        return set(tool_actions(context, self.tool).drop_message_ids)
