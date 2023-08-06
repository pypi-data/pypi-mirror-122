from typing import Dict, Optional, Type

from dinject.executors.bash import BashExecutor
from dinject.executors.python import PythonExecutor
from dinject.types import Block, Executor

executors: Dict[str, Type[Executor]] = {
    "bash": BashExecutor,
    "python": PythonExecutor,
}


def get_executor(block: Block) -> Optional[Executor]:
    """Gets an executor for `block`."""

    if t := executors.get(block.lang, None):
        return t(block.script)
    return None
