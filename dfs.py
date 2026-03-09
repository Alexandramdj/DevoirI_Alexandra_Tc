from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import time
from maze import Maze, Pos


@dataclass
class SearchResult:
    path: List[Pos]
    explored_order: List[Pos]
    nodes_explored: int
    path_length: int
    time_ms: float


def reconstruct(came_from: Dict[Pos, Optional[Pos]], goal: Pos) -> List[Pos]:
    if goal not in came_from:
        return []
    cur: Optional[Pos] = goal
    out: List[Pos] = []
    while cur is not None:
        out.append(cur)
        cur = came_from[cur]
    out.reverse()
    return out


def dfs(maze: Maze) -> SearchResult:
    t0 = time.perf_counter()

    start, goal = maze.start, maze.goal
    stack: List[Pos] = [start]        # pile LIFO
    came_from: Dict[Pos, Optional[Pos]] = {start: None}
    visited: Set[Pos] = {start}
    explored_order: List[Pos] = []

    while stack:
        current = stack.pop()
        explored_order.append(current)

        if current == goal:
            break

        r, c = current
        for nxt in maze.neighbors(r, c):   # droite, bas, gauche, haut
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                stack.append(nxt)

    path = reconstruct(came_from, goal)

    t1 = time.perf_counter()
    return SearchResult(
        path=path,
        explored_order=explored_order,
        nodes_explored=len(explored_order),
        path_length=max(0, len(path) - 1),
        time_ms=(t1 - t0) * 1000.0,
    )