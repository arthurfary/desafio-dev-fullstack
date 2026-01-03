from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from database_handler import Todos

app = Flask(__name__)

api = Api(
    app,
    title="App Todos",
    description="Backend aplicativo de To-dos",
)

db = Todos()

CORS(
    app,
    resources={
        r"/tasks*": {
            "origins": ["http://localhost:5173", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

# modelos, usados para a documetação swagger com restx

task_model = api.model(
    "Task",
    {
        "id": fields.Integer(required=True),
        "titulo": fields.String(required=True),
        "descricao": fields.String(required=True),
        "status": fields.String(
            required=True,
            enum=["pendente", "concluida"],
        ),
        "dataCriacao": fields.String(required=True),
    },
)

task_input = api.model(
    "TaskInput",
    {
        "titulo": fields.String(required=True),
        "descricao": fields.String(required=True),
        "status": fields.String(
            required=True,
            enum=["pendente", "concluida"],
        ),
    },
)

message_model = api.model(
    "Message",
    {
        "message": fields.String,
    },
)


@api.route("/tasks")
class Tasks(Resource):
    @api.marshal_list_with(task_model)
    def get(self):
        todos = db.get_todos()

        return [
            {
                "id": todo.id,
                "titulo": todo.titulo,
                "descricao": todo.descricao,
                "status": todo.status,
                "dataCriacao": todo.data_criacao,
            }
            for todo in todos
        ], 200

    @api.expect(task_input)
    @api.marshal_with(message_model)
    def post(self):
        data = request.get_json()

        db.insert(
            titulo=data["titulo"],
            descricao=data["descricao"],
            is_concluida=data["status"] == "concluida",
        )

        return {"message": "Task created"}, 201


@api.route("/tasks/<int:id>")
class Task(Resource):
    @api.expect(task_input)
    @api.marshal_with(message_model)
    def put(self, id):
        data = request.get_json()

        updated = db.update(
            id=id,
            novo_titulo=data.get("titulo"),
            nova_descricao=data.get("descricao"),
            is_concluida=data.get("status") == "concluida",
        )

        if not updated:
            api.abort(404, "Task not found")

        return {"message": "Task updated"}, 200

    @api.marshal_with(message_model)
    def delete(self, id):
        deleted = db.delete(id)

        if not deleted:
            api.abort(404, "Task not found")

        return {"message": "Task deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

