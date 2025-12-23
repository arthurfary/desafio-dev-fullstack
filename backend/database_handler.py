import sqlite3


class Todos:
    def __init__(self, path="todos.db"):
        self.path = path

    # TODO: DOCUMENT:
    # Connecting everytime makes sense here
    # prevents from needing to use `check_same_thread=False`
    # ensures it's clear, well define, in-and-out behaviour
    def _get_connection(self):
        return sqlite3.connect(self.path)

    def get_todos(self) -> list[tuple]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos")
            return cursor.fetchall()

    def insert(self, titulo: str, descricao: str, is_concluida: bool = False):
        status = "concluida" if is_concluida else "pendente"
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO todos (titulo, descricao, status) VALUES (?, ?, ?)",
                (titulo, descricao, status),
            )

    def delete(self, id: int):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM todos WHERE id = ?", (id,))

    def update(self, id: int, novo_titulo: str, nova_descricao: str, is_concluida: bool = False):
        status = "concluida" if is_concluida else "pendente"
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE todos SET titulo=?, descricao=?, status=? WHERE id=?",
                (novo_titulo, nova_descricao, status, id),
            )


if __name__ == "__main__":
    class_obj = Todos()
    # class_obj.insert("Teste tit", "teste desc")
    print(class_obj.get_todos())
    class_obj.update(1, "Titulo", "desc", True)
    # class_obj.delete("9")
    print(class_obj.get_todos())
