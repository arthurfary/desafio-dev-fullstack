import sqlite3

connection = sqlite3.connect(r"todos.db")

cur = connection.cursor()

# if explicitly with autoincrement prevents
# reuse of ROWIDs from previously deleted rows.
#
# data_criacao set as utc as it is best practice, convert when presenting
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS todos( 
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        descricao TEXT,
        status TEXT CHECK(status IN ('pendente', 'concluida')),
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
)

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

print(cur.fetchall())
