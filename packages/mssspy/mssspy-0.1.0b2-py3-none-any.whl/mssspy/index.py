from typing import List, Optional


class Index(list):
    complete: bool
    path: Optional[str]

    def __init__(self, offsets: List[int] = [], complete: bool = False,
                 path: Optional[str] = None) -> None:
        super().__init__(offsets)
        self.complete = complete
        self.path = path
