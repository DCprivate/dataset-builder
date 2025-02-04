from abc import ABC, abstractmethod
from dataharvester_shared.models.task import TaskContext

class Node(ABC):
    """Abstract base class for pipeline nodes."""
    @abstractmethod
    def process(self, task_context: TaskContext) -> TaskContext:
        """Process the task context."""
        pass 