from flask import Flask, request, jsonify
from database_handler import Todos

db = Todos()
app = Flask(__name__)


@app.route("/tasks", methods=["GET", "POST"])
def get_tasks():
    # using match so every thing is explicitly handled
    match request.method:
        case "POST":
            db.insert("Titulo", "Descrição...")
            return {"status": 200}
        case "GET":
            ret = [{"id": todo[0]} for todo in db.get_todos()]
            return jsonify(ret)
