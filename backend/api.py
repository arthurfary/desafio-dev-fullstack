from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from database_handler import Todos

app = Flask(__name__)
api = Api(app, title="App Todos", description="Backend aplicativo de To-dos")
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

task_model = api.model(
    "Task",
    {
        "id": fields.Integer,
        "titulo": fields.String,
        "descricao": fields.String,
        "status": fields.String(enum=["pendente", "concluida"]),
        "dataCriacao": fields.String,
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
        ]

    @api.expect(task_input)
    def post(self):
        data = request.get_json()
        db.insert(
            titulo=data["titulo"],
            descricao=data["descricao"],
            is_concluida=data["status"] == "concluida",
        )
        return {"status": 200}, 201


@api.route("/tasks/<int:id>")
class Task(Resource):
    @api.expect(task_input)
    def put(self, id):
        data = request.get_json()
        db.update(
            id=id,
            novo_titulo=data.get("titulo"),
            nova_descricao=data.get("descricao"),
            is_concluida=data.get("status"),
        )
        return {"status": 200}

    def delete(self, id):
        db.delete(id)
        return {"status": 200}


if __name__ == "__main__":
    app.run(debug=True)
