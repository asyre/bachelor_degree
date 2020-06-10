from typing import Optional


class TestCase:
    def __init__(self,
                 name: str,
                 description: Optional[str],
                 node: Optional[str],
                 func,
                 order: Optional[int],
                 skip: Optional[bool]):
        self.name = name
        self.description = description
        self.func = func
        self.order = order
        self.node = node
        self.skip = skip
