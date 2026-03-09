from __future__ import annotations
from typing import List, Tuple, Callable
from maze import generate_maze, mark_exploration, mark_path, Maze, Pos
from dfs import dfs
from bfs import bfs
from astar import astar


def format_path(path: List[Pos]) -> str:
    if not path:
        return "Chemin : (aucun chemin trouvé)"
    parts = []
    for i, (r, c) in enumerate(path):
        if i == 0:
            parts.append(f"S ({r} , {c})")
        elif i == len(path) - 1:
            parts.append(f"G ({r} , {c})")
        else:
            parts.append(f"({r} , {c})")
    return "Chemin : " + " -> ".join(parts)


def run_one(name: str, maze: Maze, algo: Callable[[Maze], object]) -> Tuple[str, int, int, float]:
    res = algo(maze)

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    explored_grid = mark_exploration(maze, res.explored_order)
    print("\n--- Exploration (p) ---")
    print(maze.render(explored_grid))

    solved_grid = mark_path(maze, res.path)
    print("\n--- Solution (*) ---")
    print(maze.render(solved_grid))

    print("\n" + format_path(res.path))
    print("\n--- Statistiques ---")
    print(f"Nombre de noeuds explorés : {res.nodes_explored}")
    print(f"Longueur du chemin trouvé : {res.path_length}")
    print(f"Temps d'exécution (ms)     : {res.time_ms:.3f}")

    return (name, res.nodes_explored, res.path_length, res.time_ms)


def main():
    seed = 42
    maze = generate_maze(size=16, wall_prob=0.28, seed=seed)

    print("Labyrinthe initial:")
    print(maze.render())

    results = []
    results.append(run_one("DFS", maze, dfs))
    results.append(run_one("BFS", maze, bfs))
    results.append(run_one("A* (manhattan)", maze, astar))

    print("\n" + "=" * 60)
    print("Tableau comparatif")
    print("=" * 60)
    print(f"{'Algorithme':<15} {'Noeuds':>8} {'Longueur':>10} {'Temps (ms)':>12}")
    print("-" * 60)
    for name, nodes, length, tms in results:
        print(f"{name:<15} {nodes:>8} {length:>10} {tms:>12.3f}")


if __name__ == "__main__":
    main()