from abc import ABC, abstractmethod
from typing import Union, Iterable, List, Iterator

from sortedcontainers import SortedDict

from pysqlitekg2vec.typings import SWalk

EntityID = Union[str, int]


class CorpusVault(ABC, Iterable[SWalk]):
    """ a vault of all generated walks representing the corpus. The walks have
     always been returned in the same order to keep determinism. """

    def __init__(self):
        """ creates a new abstract corpus vault. """
        self._walker_id = 0

    def set_walker_id(self, walker_id: int) -> None:
        """sets the ID of the current walker from which walks are added.

        :param walker_id: ID of the current walker from which walks are added.
        """
        self._walker_id = walker_id

    @abstractmethod
    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        """adds generated walks of arbitrary length to this vault for the
        given entity.

        :param entity_id: id of the entity for which the walk was generated.
        :param walks: generated walks that shall be added to the vault.
        """
        raise NotImplementedError('must be implemented')

    def __iter__(self) -> Iterator[SWalk]:
        """ """
        raise NotImplementedError('must be implemented')

    def __len__(self):
        """returns the number of stored walks."""
        raise NotImplementedError('must be implemented')

    @abstractmethod
    def close(self):
        """closes this vault and frees up resources."""
        raise NotImplementedError('must be implemented')


class _WalkIterator(Iterator[SWalk]):
    """ a iterator over the walks of an in-memory vault. """

    def __init__(self, walk_iter: Iterator[List[SWalk]]):
        self._walk_iter = walk_iter
        self._walk_list_iter = None

    def __next__(self) -> SWalk:
        if self._walk_list_iter is None:
            self._walk_list_iter = iter(next(self._walk_iter))
        try:
            return next(self._walk_list_iter)
        except StopIteration:
            self._walk_list_iter = None
            return next(self)


class InMemoryCorpusVault(CorpusVault):
    """ a vault of all generated walks which are stored in memory. """

    def __init__(self):
        """creates a new in-memory vault."""
        super().__init__()
        self._vault = SortedDict()
        self._n_walks = 0

    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        self._vault['%s_%s' % (str(self._walker_id), str(entity_id))] = walks
        self._n_walks += len(walks)

    def __iter__(self) -> Iterator[SWalk]:
        return _WalkIterator(iter(self._vault.values()))

    def __len__(self):
        return self._n_walks

    def close(self):
        self._vault = None
        self._n_walks = 0


class CorpusVaultFactory(ABC):
    """ an abstract factory to create corpus vaults of a specific type. """

    @abstractmethod
    def create(self) -> CorpusVault:
        """creates a new corpus vault.

        :return: a new corpus vault.
        """
        raise NotImplementedError('must be implemented')


class InMemoryCorpusVaultFactory(CorpusVaultFactory):
    """ a factory for creating new in-memory corpus vaults. """

    def create(self) -> CorpusVault:
        return InMemoryCorpusVault()



