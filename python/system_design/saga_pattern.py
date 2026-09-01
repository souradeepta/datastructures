"""A callable, in-memory Saga orchestrator for interview practice.

Each step contains a named zero-argument action and compensation. An action
that raises stops the saga; completed steps are then compensated in reverse
order. This is an orchestration teaching model, not a durable workflow engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


Action = Callable[[], object]


@dataclass(frozen=True)
class SagaStep:
    """A named action and its best-effort reverse operation."""

    name: str
    action: Action
    compensation: Action

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("saga step name must not be empty")
        if not callable(self.action) or not callable(self.compensation):
            raise TypeError("action and compensation must be callable")


@dataclass
class SagaResult:
    """Outcome of one saga execution."""

    success: bool
    failed_step: Optional[str]
    completed_steps: List[str]
    compensation_failures: List[str]


class SagaOrchestrator:
    """Execute registered steps and compensate completed work on failure."""

    def __init__(self) -> None:
        self.steps: List[SagaStep] = []
        self.executed: List[str] = []

    def add_step(self, step: SagaStep) -> None:
        if not isinstance(step, SagaStep):
            raise TypeError("step must be a SagaStep")
        self.steps.append(step)

    def execute(self) -> SagaResult:
        """Run the saga and return a fresh result for this execution."""
        completed: List[SagaStep] = []
        failed_step: Optional[str] = None

        for step in self.steps:
            try:
                step.action()
            except Exception:
                failed_step = step.name
                break
            completed.append(step)

        compensation_failures: List[str] = []
        if failed_step is not None:
            for step in reversed(completed):
                try:
                    step.compensation()
                except Exception:
                    compensation_failures.append(step.name)

        self.executed = [step.name for step in completed]
        return SagaResult(
            success=failed_step is None,
            failed_step=failed_step,
            completed_steps=list(self.executed),
            compensation_failures=compensation_failures,
        )


if __name__ == "__main__":
    saga = SagaOrchestrator()
    saga.add_step(SagaStep("reserve", lambda: None, lambda: None))
    print(saga.execute())
