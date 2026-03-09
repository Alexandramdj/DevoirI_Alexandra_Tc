# Devoir I — INF-5183 (DFS / BFS / A*)

## Contenu
Ce projet génère un labyrinthe 16×16 avec :
- Bordures en murs
- S en (1,1) et G en (14,14)
- Un chemin garanti entre S et G

Ensuite, il exécute :
- DFS (pile LIFO)
- BFS (file FIFO)
- A* (heuristique Manhattan)

Le programme affiche :
- le labyrinthe initial
- l'exploration (p)
- la solution (chemin avec *)
- la liste des coordonnées du chemin
- les statistiques (noeuds explorés, longueur, temps)
- un tableau comparatif des 3 algorithmes

## Exécution (Windows)
Ouvre PowerShell dans le dossier du projet puis :

```bash
python main.py