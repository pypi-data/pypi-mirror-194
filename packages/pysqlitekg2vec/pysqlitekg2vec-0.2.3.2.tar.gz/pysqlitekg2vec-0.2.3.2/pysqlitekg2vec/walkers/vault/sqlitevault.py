from collections import deque
from os import remove
from os.path import exists
from sqlite3 import connect, Connection
from typing import List, Iterator

from pysqlitekg2vec.typings import SWalk
from pysqlitekg2vec.walkers.vault.vault import CorpusVault, EntityID, \
    CorpusVaultFactory, WalkImporter


class _DBWriteCmd:
    """ a class that maintains write commands for the SQLite database. """

    CREATE_WALK_TABLE = '''
CREATE TABLE corpus (
    walker_id INTEGER NOT NULL,
    entity_id TEXT NOT NULL,
    walk_no INTEGER NOT NULL,
    hop_no INTEGER NOT NULL,
    hop_id TEXT NOT NULL,
    PRIMARY KEY (walker_id, entity_id, walk_no, hop_no)
);
'''
    INSERT_WALK = '''
INSERT INTO corpus (walker_id, entity_id, walk_no, hop_no, hop_id)
VALUES (?, ?, ?, ?, ?);
'''


class _DBReadCmd:
    """ a class that maintains query commands for the SQLite database. """

    WALKS_FETCH = '''
SELECT walker_id, entity_id, walk_no, hop_no, hop_id
FROM corpus
ORDER BY walker_id, entity_id, walk_no, hop_no
LIMIT ?
OFFSET ?;
'''

    COUNT_WALKS = '''
SELECT sum(c) as walk_count
FROM (SELECT count(DISTINCT walk_no) as c FROM corpus GROUP BY walker_id,
      entity_id);
'''


class _DBRowIterator(Iterator[SWalk]):
    """ an iterator over the walks stored in vault DB. """

    def __init__(self, con: Connection, *, cache_size: int):
        """creates a new DB iterator over the vault DB.

        :param con: of the SQLite database.
        :param cache_size: the number of walks to keep in memory.
        """
        self._con = con
        self._cache_size = cache_size
        self._queue = deque()
        self._n = 0

    def _fetch(self):
        cursor = self._con.cursor()
        try:
            results = cursor.execute(_DBReadCmd.WALKS_FETCH,
                                     (self._cache_size, self._n))
            for r in results:
                self._queue.append(r)
            self._n += self._cache_size
        finally:
            cursor.close()

    def __next__(self) -> SWalk:
        # fetch rows first
        if not self._queue:
            self._fetch()
            if not self._queue:
                raise StopIteration()
        # fetch walks
        wid, eid, wno, _, hop_id = self._queue[0]
        self._queue.popleft()
        walk = [hop_id]
        while True:
            if not self._queue:
                self._fetch()
                if not self._queue:
                    return tuple(walk)
            nh_wid, nh_eid, nh_wno, _, nh_hid = self._queue[0]
            if wid == nh_wid and eid == nh_eid and wno == nh_wno:
                walk.append(nh_hid)
                self._queue.popleft()
            else:
                return tuple(walk)


class _SQLiteWalkImporter(WalkImporter):
    """  """

    @staticmethod
    def _create_schema(con: Connection):
        """creates a table schema for storing generated walks.

        :param con: connection of the SQLite database in which the new tale
        shall be created.
        """
        cursor = con.cursor()
        try:
            cursor.execute(_DBWriteCmd.CREATE_WALK_TABLE)
        finally:
            cursor.close()

    def __init__(self, con: Connection,cache_size: int):
        super().__init__()
        self._cache_size = cache_size
        self._con = con
        self._n = 0

    def __enter__(self):
        self._create_schema(self._con)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self._con.commit()

    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        cursor = self._con.cursor()
        try:
            for walk_no, walk in enumerate(walks):
                for hop_no, hop_id in enumerate(walk):
                    cursor.execute(_DBWriteCmd.INSERT_WALK,
                                   (self._walker_id, str(entity_id),
                                    walk_no, hop_no, hop_id))
                    self._n += 1
            if (self._n % self._cache_size) == 0:
                self._con.commit()
        finally:
            cursor.close()

    def stored_walks(self) -> int:
        cursor = self._con.cursor()
        try:
            return int(cursor.execute(_DBReadCmd.COUNT_WALKS).fetchone()[0])
        finally:
            cursor.close()


class SQLiteCorpusVault(CorpusVault):
    """ a vault of all generated walks which are stored in a single SQLite
    table. """

    def __init__(self, db_path: str, *, cache_size: int = 1000000):
        """creates a new SQLite database at the given path representing the
        corpus vault.

        :param db_path: path to the database file.
        :param cache_size: the number of walks to keep in memory.
        """
        super().__init__()
        self._cache_size = cache_size
        self._db_path = db_path
        self._con = connect(db_path, check_same_thread=False)
        self._importer = _SQLiteWalkImporter(self._con, cache_size)

    def walk_importer(self) -> WalkImporter:
        return self._importer

    def __iter__(self) -> Iterator[SWalk]:
        return _DBRowIterator(self._con, cache_size=self._cache_size)

    def __len__(self):
        return self._importer.stored_walks()

    def free(self):
        if self._con is not None:
            self._con.close()
        if exists(self._db_path):
            remove(self._db_path)


class SQLiteCorpusVaultFactory(CorpusVaultFactory):
    """ a factory for creating new in-memory corpus vaults. """

    @staticmethod
    def _prepare_path(db_path: str) -> str:
        """checks whether the given database file already exists. If that is
        the case, then a new path is generated with a new postfix.

        :param db_path: the original path to the database.
        :return: a path for the database file that is ensured to be non
        existing.
        """
        n = 0
        new_db_path = db_path
        while exists(new_db_path):
            new_db_path = '%s_%d' % (db_path, n)
            n += 1
        return new_db_path

    def __init__(self, db_path: str, *, cache_size: int = 1000000):
        """creates a new factory to create new SQLite corpus vaults.

        :param db_path: path to the database file.
        :param cache_size: optionally, the number of walks to keep in memory.
        """
        self._db_path = db_path
        self._cache_size = cache_size

    def create(self) -> CorpusVault:
        db_path = self._prepare_path(self._db_path)
        return SQLiteCorpusVault(db_path, cache_size=self._cache_size)
