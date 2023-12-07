from dataclasses import dataclass
from typing import Callable, List

from inferio_x._method import Method


@dataclass
class Endpoint:
    path: str
    handler: Callable
    methods: List[Method]
    monitor: bool = True
    logger: bool = False

    def __post_init__(self):
        if not self.path.startswith("/"):
            raise ValueError("Routed paths must start with '/'")
        if len(self.methods) == 0:
            raise ValueError("Methods must include at least one HTTP method")
