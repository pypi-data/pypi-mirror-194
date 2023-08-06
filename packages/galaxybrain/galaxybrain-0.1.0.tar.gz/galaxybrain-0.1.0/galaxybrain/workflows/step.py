from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from attrs import define, field

if TYPE_CHECKING:
    from galaxybrain.workflows import Step, StepInput, StepOutput, Workflow


@define
class Step(ABC):
    input: Optional[StepInput] = field(default=None, kw_only=True)
    parent: Optional[Step] = field(default=None, kw_only=True)
    child: Optional[Step] = field(default=None, kw_only=True)

    output: Optional[StepOutput] = field(default=None, init=False)
    workflow: Optional[Workflow] = field(default=None, init=False)

    def add_child(self, child: Step) -> None:
        self.child = child
        child.parent = self

    def add_parent(self, parent: Step) -> None:
        parent.child = self
        self.parent = parent

    def name(self) -> str:
        return type(self).__name__

    def is_finished(self) -> bool:
        return self.output is not None

    def before_run(self) -> None:
        self.workflow.memory.before_run(self)

    def after_run(self) -> None:
        if self.child:
            self.child.input = self.output

        self.workflow.memory.after_run(self)

    def execute(self) -> StepOutput:
        self.before_run()

        output = self.run()

        self.after_run()

        return output

    @abstractmethod
    def run(self, **kwargs) -> StepOutput:
        pass

