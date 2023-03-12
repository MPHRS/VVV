from typing import Final, List, Tuple

Bondtype = List[Tuple[int, int]]

EMPTY: Final[Bondtype] = []
LINEAR: Final[Bondtype] = [(0, 1), (1, 2), (2, 3)]
NEGATIVE: Final[Bondtype] = [(-1, 0), (0, 1), (1, 2)]