from datetime import datetime
import sqlite3

"""
id INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT,
descricao TEXT,
status TEXT CHECK(status IN ('pendente', 'concluida')),
data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
"""


class Todo:
    def __init__(
        self,
        id: int,
        titulo: str,
        descricao: str,
        status: str,
        data_criacao: datetime,
    ) -> None:
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.data_criacao = data_criacao


class Todos:
    def __init__(self, path="todos.db"):
        self.path = path

    def _get_connection(self):
        return sqlite3.connect(self.path)

    def get_todos(self) -> list[Todo]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos")
            rows = cursor.fetchall()
            return [Todo(*row) for row in rows]

    def insert(self, titulo: str, descricao: str, is_concluida: bool = False) -> None:
        status = "concluida" if is_concluida else "pendente"
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO todos (titulo, descricao, status) VALUES (?, ?, ?)",
                (titulo, descricao, status),
            )

    def update(
        self,
        id: int,
        novo_titulo: str,
        nova_descricao: str,
        is_concluida: bool = False,
    ) -> bool:
        status = "concluida" if is_concluida else "pendente"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE todos
                SET titulo = ?, descricao = ?, status = ?
                WHERE id = ?
                """,
                (novo_titulo, nova_descricao, status, id),
            )
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM todos WHERE id = ?",
                (id,),
            )
            return cursor.rowcount > 0
