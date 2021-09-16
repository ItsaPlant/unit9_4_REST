from flask import Flask, jsonify, abort, make_response
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "ni"

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(todos.all())

@app.route("/api/v1/todos/<int:todo_id>/", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

if __name__ == "__main__":
    app.run(debug=True)