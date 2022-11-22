"""
Database for the library project
"""
import tinydb


class DB:
    def __init__(self, db_path, db_file_prefix):
        self._db = tinydb.TinyDB(
            db_path / f"{db_file_prefix}.json", create_dirs=True
        )

    def create(self, item: dict) -> int:
        sn = self._db.insert(item)
        return sn

    def read(self, sn: int):
        item = self._db.get(doc_sn=sn)
        return item

    def read_all(self):
        return self._db

    def update(self, sn: int, mods) -> None:
        changes = {k: v for k, v in mods.items() if v is not None}
        self._db.update(changes, doc_ids=[sn])

    def delete(self, sn: int) -> None:
        self._db.remove(doc_ids=[sn])

    def delete_all(self) -> None:
        self._db.truncate()

    def count(self) -> int:
        return len(self._db)

    def close(self):
        self._db.close()
