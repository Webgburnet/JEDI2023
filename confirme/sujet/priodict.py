from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Tuple, Generator

T = TypeVar("T")


class EmptyDict(Exception):
    pass


class PrioDict(ABC, Generic[T]):
    "classe abstraire dictionnaire de priorité"

    @abstractmethod
    def __contains__(self, key: T) -> bool:
        """Teste si [key] est dans le dictionnaire"""
        pass

    @abstractmethod
    def __getitem__(self, key: T) -> int:
        """Retourne la priorité de [key]"""
        pass

    @abstractmethod
    def __setitem__(self, key: T, newval: int) -> None:
        """Modifie la priorité de [key]"""
        pass

    @abstractmethod
    def __bool__(self) -> bool:
        """Test si le dictionnaire est vide"""
        pass

    @abstractmethod
    def __iter__(self) -> Generator[T, None, None]:
        """Énumère les éléments contenus dans la file"""
        pass

    @abstractmethod
    def pop_smallest(self) -> Tuple[T, int]:
        """Supprime et retourne l'élément de plus petite priorité
        Retourne l'élément et sa priorité"""
        pass
