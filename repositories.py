"""Repository over data.database. Every query is scoped by user_id and parameterised."""
import json
from typing import List
from data.database import connect


class Repository:
    def __init__(self, user_id: str, kind: str):
        self.user_id, self.kind = user_id, kind

    def add(self, record: dict) -> None:
        with connect() as con:
            con.execute("INSERT INTO records (user_id, kind, body) VALUES (?,?,?)", (self.user_id, self.kind, json.dumps(record)))

    def all(self) -> List[dict]:
        with connect() as con:
            rows = con.execute("SELECT body FROM records WHERE user_id=? AND kind=?", (self.user_id, self.kind)).fetchall()
        return [json.loads(r[0]) for r in rows]

    def delete_all(self) -> None:
        with connect() as con:
            con.execute("DELETE FROM records WHERE user_id=? AND kind=?", (self.user_id, self.kind))
