from typing import Generic, TypeVar, Tuple, List, Generator
from priodict import PrioDict, EmptyDict

T = TypeVar("T")


class NaiveDict(PrioDict[T]):
    """Version naïve avec une liste non triée"""

    t: List[Tuple[T, int]]

    def __init__(self) -> None:
        self.t = []

    def __contains__(self, key: T) -> bool:
        for k, _ in self.t:
            if k == key:
                return True
        return False

    def __getitem__(self, key: T) -> int:
        for k, v in self.t:
            if k == key:
                return v
        raise KeyError(key)

    def __iter__(self) -> Generator[T, None, None]:
        for k, _ in self.t:
            yield k

    def __setitem__(self, key: T, newprio: int) -> None:
        for i,(k,v) in enumerate(self.t):
            if k==key:
                self.t[i]=(key, newprio)
                break
        else:
            self.t.append((key, newprio))
        "TODO TODO TODO"
        #raise NotImplementedError("il faut coder __setitem__ !")

    def __bool__(self) -> bool:
        return bool(self.t)

    def pop_smallest(self) -> Tuple[T, int]:
        if not self.t:
            raise EmptyDict
        minprio = self.t[0][1]
        minidx = 0
        for i, (k, p) in enumerate(self.t):
            if p < minprio:
                minprio, minidx = p, i
        return self.t.pop(minidx)