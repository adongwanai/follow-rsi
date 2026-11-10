"""Decide when to run a Drop selector, independently of its retention rule."""

from dataclasses import dataclass

from ..types import ChatTokenCounter
from .tools import CacheTool, tool_actions
from .utils.common import check_schedule, positive_integer, scheduled
from .utils.context import PolicyContext


@dataclass(frozen=True)
class TurnTrigger:
    after: int = 1
    every: int | None = 1

    def __post_init__(self) -> None:
        check_schedule(self.after, self.every)

    def __call__(self, context: PolicyContext) -> bool:
        return context.new_turn and scheduled(context.request.call_index, self.after, self.every)


@dataclass(frozen=True)
class TokenTrigger:
    threshold: int
    counter: ChatTokenCounter

    def __post_init__(self) -> None:
        positive_integer(self.threshold, "threshold")

    def __call__(self, context: PolicyContext) -> bool:
        return (
            context.layout(self.counter).prompt_tokens - context.tokens(self.counter, context.hidden)
            > self.threshold
        )


@dataclass(frozen=True)
class ModelTrigger:
    tool: CacheTool

    def __call__(self, context: PolicyContext) -> bool:
        return bool(tool_actions(context, self.tool).drop_message_ids)
