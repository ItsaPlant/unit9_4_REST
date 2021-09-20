from flask import Flask, jsonify, abort, make_response, request
from flask.wrappers import Request

from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "ni"

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(todos.all())

@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201

@app.route("/api/v1/todos/<int:todo_id>/", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('title', todo['title']),
        'description': data.get('description', todo['description']),
        'done': data.get('done', todo['done'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})

@app.route("/api/v1/todos/<int:todo_id>", methods = ["DELETE"])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

#ERRORHANDLERs

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)