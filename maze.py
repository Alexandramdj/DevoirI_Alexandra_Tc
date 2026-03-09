from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Iterable, Optional
import random

Pos = Tuple[int, int]  # (row, col)

WALL = "#"
FREE = "."
START = "S"
GOAL = "G"
VISITED = "p"
PATH = "*"


@dataclass
class Maze:
    grid: List[List[str]]
    start: Pos
    goal: Pos

    @property
    def n(self) -> int:
        return len(self.grid)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.n and 0 <= c < self.n

    def passable(self, r: int, c: int) -> bool:
        return self.grid[r][c] != WALL

    def neighbors(self, r: int, c: int) -> List[Pos]:
        # ordre imposé : droite, bas, gauche, haut
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        out: List[Pos] = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.passable(nr, nc):
                out.append((nr, nc))
        return out

    def copy_grid(self) -> List[List[str]]:
        return [row[:] for row in self.grid]

    def render(self, grid: Optional[List[List[str]]] = None) -> str:
        g = self.grid if grid is None else grid
        return "\n".join(" ".join(row) for row in g)


def _carve_random_walk_path(n: int, rng: random.Random, start: Pos, goal: Pos) -> List[Pos]:
    """Creuse un chemin garanti de start vers goal."""
    r, c = start
    gr, gc = goal
    path = [(r, c)]
    visited = {start}

    while (r, c) != (gr, gc):
        moves = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                moves.append((nr, nc))

        if not moves:
            # backtrack si coincé
            path.pop()
            r, c = path[-1]
            continue

        def score(p: Pos) -> int:
            return abs(p[0] - gr) + abs(p[1] - gc)

        best = min(moves, key=score)
        nxt = rng.choice(moves) if rng.random() < 0.25 else best

        r, c = nxt
        visited.add((r, c))
        path.append((r, c))

    return path


def generate_maze(size: int = 16, wall_prob: float = 0.28, seed: Optional[int] = None) -> Maze:
    """
    - size x size (défaut 16)
    - bordures en murs
    - S=(1,1), G=(size-2, size-2)
    - chemin garanti S->G
    """
    if size < 5:
        raise ValueError("size doit être >= 5")

    rng = random.Random(seed)
    start = (1, 1)
    goal = (size - 2, size - 2)

    grid = [[WALL for _ in range(size)] for _ in range(size)]

    # chemin garanti
    path_cells = _carve_random_walk_path(size, rng, start, goal)
    path_set = set(path_cells)

    # intérieur : chemin + aléatoire
    for r in range(1, size - 1):
        for c in range(1, size - 1):
            if (r, c) in path_set:
                grid[r][c] = FREE
            else:
                grid[r][c] = WALL if rng.random() < wall_prob else FREE

    sr, sc = start
    gr, gc = goal
    grid[sr][sc] = START
    grid[gr][gc] = GOAL

    return Maze(grid=grid, start=start, goal=goal)


def mark_exploration(original: Maze, explored: Iterable[Pos]) -> List[List[str]]:
    g = original.copy_grid()
    for (r, c) in explored:
        if g[r][c] == FREE:
            g[r][c] = VISITED
    return g


def mark_path(original: Maze, path: List[Pos]) -> List[List[str]]:
    g = original.copy_grid()
    for (r, c) in path:
        if g[r][c] in (FREE, VISITED):
            g[r][c] = PATH
    sr, sc = original.start
    gr, gc = original.goal
    g[sr][sc] = START
    g[gr][gc] = GOAL
    return g