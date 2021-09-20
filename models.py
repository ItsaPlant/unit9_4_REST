import json
from os import waitpid

class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileExistsError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        todo = [todo for todo in self.all() if todo['id'] == id]
        if todo:
            return todo[0]
        return []

    def create(self, data):
        self.todos.append(data)
        self.save_all()

    def save_all(self):
        with open('todos.json', "w") as f:
            json.dump(self.todos, f)

    # def update(self, id, data):
    #     data.pop('csrf_token')
    #     self.todos[id] = data
    #     self.save_all()

    def update(self, id, data):
        todo = self.get(id)
        if todo:
            index = self.todos.index(id)
            self.todos[index] = data
            self.save_all()
            return True
        return False
    
    def delete(self, id):
        todo = self.get(id)
        if todo:
            self.todos.remove(todo)
            self.save_all()
            return True
        return False

todos = Todos()