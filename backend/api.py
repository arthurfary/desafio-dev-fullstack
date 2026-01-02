from flask import Flask, request, jsonify
from flask_cors import CORS
from database_handler import Todos

app = Flask(__name__)
db = Todos()

CORS(
    app,
    resources={
        r"/tasks*": {
            "origins": ["http://localhost:5173", "http://localhost:5000"],
            "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    todos = db.get_todos()
    response = {
        "status": 200,
        "values": [
            {
                "id": todo.id,
                "titulo": todo.titulo,
                "descricao": todo.descricao,
                "status": todo.status,
                "dataCriacao": todo.data_criacao,
            }
            for todo in todos
        ],
    }
    return jsonify(response)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    db.insert(titulo=data["titulo"], descricao=data["descricao"], is_concluida=data["status"] == "concluida")

    return jsonify({"status": 200}), 201


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()

    db.update(
        id=id, novo_titulo=data.get("titulo"), nova_descricao=data.get("descricao"), is_concluida=data.get("status")
    )

    return jsonify({"status": 200})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    db.delete(id)
    return jsonify({"status": 200})


# For cors
@app.route("/tasks/<int:id>", methods=["OPTIONS"])
@app.route("/tasks", methods=["OPTIONS"])
def handle_options(id=None):
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
