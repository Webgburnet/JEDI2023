from typing import Generic, TypeVar, Dict, Optional, Type
from priodict import PrioDict

S = TypeVar("S")

class Dijkstra(Generic[S]):
    """Instance de l'algorithme de Dijstra"""

    F: PrioDict[S]
    p: Dict[S, Optional[S]]

    def __init__(self, priodict_class: Type[PrioDict[S]]):
        """Crée une nouvelle instance pour les dictionnaires
        de priorité de type [priodict_class]"""
        self.F = priodict_class()
        self.p = {}

    def shortest_path(self, to: S):
        """Retourne s'il existe un plus court chemin vers [to]
        tel qu'il apparaît en remontant [self.p]"""
        if to not in self.p or self.p[to] is None:
            return None
        cur = self.p[to]
        res = []
        while cur is not None and cur in self.p:
            res.append(cur)
            cur = self.p[cur]
        return res[::-1]

    def __call__(self, G: Dict[S, Dict[S, int]], s: S):
        """Effectue les calculs depuis la source [s] pour le
        graphe [G]. Pour l'instant ça ne fait pas grand chose..."""
        self.p[s] = None
        self.F[s] = 0

        while self.F:
            (u, du)  = self.F.pop_smallest()
            for v in G[u]:
                if (v not in self.p) or (v in self.F and du+G[u][v]<self.F[v]):
                    self.p[v]=u
                    self.F[v]=du+G[u][v]
        return self.p
        """for v in G[s]:
            self.p[v] = s 
            self.F[v] = 1
        while self.F:
            (u, du) = self.F.pop_smallest()
            print(u)
        return self.p"""