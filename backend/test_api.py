import pytest
import os
import sqlite3
import api
from database_handler import Todos

TEST_DB_PATH = "test_todos.db"


# Usa um banco de dados temporário para os testes
@pytest.fixture
def client():
    app = api.app
    app.config["TESTING"] = True

    # Injeta o banco de teste
    api.db = Todos(TEST_DB_PATH)

    with app.test_client() as client:
        yield client

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def setup_test_db():
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY,
            titulo TEXT,
            descricao TEXT,
            status TEXT CHECK(status IN ('pendente', 'concluida')),
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    yield


def test_get_empty_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []


def test_create_task(client):
    task = {
        "titulo": "Test",
        "descricao": "Test desc",
        "status": "pendente",
    }

    response = client.post("/tasks", json=task)
    assert response.status_code == 201
    assert response.is_json
    assert response.get_json()["message"] == "Task created"

    tasks = client.get("/tasks").get_json()
    assert len(tasks) == 1
    assert tasks[0]["titulo"] == task["titulo"]
    assert tasks[0]["descricao"] == task["descricao"]
    assert tasks[0]["status"] == task["status"]
    assert "dataCriacao" in tasks[0]


def test_update_task(client):
    task_inicial = {
        "titulo": "Old",
        "descricao": "Old",
        "status": "pendente",
    }

    client.post("/tasks", json=task_inicial)

    tasks = client.get("/tasks").get_json()
    task_id = tasks[0]["id"]

    task_atualizada = {
        "titulo": "New",
        "descricao": "New desc",
        "status": "concluida",
    }

    response = client.put(f"/tasks/{task_id}", json=task_atualizada)
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()["message"] == "Task updated"

    updated = client.get("/tasks").get_json()[0]
    assert updated["titulo"] == task_atualizada["titulo"]
    assert updated["descricao"] == task_atualizada["descricao"]
    assert updated["status"] == task_atualizada["status"]


def test_delete_task(client):
    task = {
        "titulo": "Delete me",
        "descricao": "Desc",
        "status": "pendente",
    }

    client.post("/tasks", json=task)

    tasks = client.get("/tasks").get_json()
    task_id = tasks[0]["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()["message"] == "Task deleted"

    assert client.get("/tasks").get_json() == []


def test_multiple_tasks(client):
    num_tasks = 3

    for i in range(num_tasks):
        client.post(
            "/tasks",
            json={
                "titulo": f"Task {i}",
                "descricao": f"Desc {i}",
                "status": "pendente",
            },
        )

    tasks = client.get("/tasks").get_json()
    assert len(tasks) == num_tasks
    assert all(task["status"] == "pendente" for task in tasks)
