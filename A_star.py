from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import heapq
import time
from maze import Maze, Pos


@dataclass
class SearchResult:
    path: List[Pos]
    explored_order: List[Pos]
    nodes_explored: int
    path_length: int
    time_ms: float


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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


def astar(maze: Maze) -> SearchResult:
    t0 = time.perf_counter()

    start, goal = maze.start, maze.goal

    # éléments du tas : (f, g, position)
    open_heap: List[Tuple[int, int, Pos]] = []
    heapq.heappush(open_heap, (manhattan(start, goal), 0, start))

    came_from: Dict[Pos, Optional[Pos]] = {start: None}
    g_score: Dict[Pos, int] = {start: 0}

    explored_order: List[Pos] = []
    closed = set()

    while open_heap:
        f, g, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)
        explored_order.append(current)

        if current == goal:
            break

        r, c = current
        for nxt in maze.neighbors(r, c):
            tentative_g = g_score[current] + 1
            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                came_from[nxt] = current
                fn = tentative_g + manhattan(nxt, goal)
                heapq.heappush(open_heap, (fn, tentative_g, nxt))

    path = reconstruct(came_from, goal)

    t1 = time.perf_counter()
    return SearchResult(
        path=path,
        explored_order=explored_order,
        nodes_explored=len(explored_order),
        path_length=max(0, len(path) - 1),
        time_ms=(t1 - t0) * 1000.0,
    )