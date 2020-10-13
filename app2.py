from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
# path os, glob(regex) / pathlib path
basedir = os.path.abspath(os.path.dirname(__file__))

# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db init
db = SQLAlchemy(app)

# marshmallow init serialization -> JSON
ma = Marshmallow(app)

# db model


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100), nullable=False)

    def __init__(self, desc):
        self.desc = desc
# product schema


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'desc')


# schema init
todo_schema = TodoSchema()  # 1:1
todos_schema = TodoSchema(many=True)  # 1: many (multiple lows)

# restfull api


@app.route('/todo', methods=['POST'])
def add_todo():
    desc = request.json['desc']
    new_todo = Todos(desc)

    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)


@app.route('/todo', methods=['GET'])
def get_todos():
    all_todos = Todos.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

# get one todo
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    todo = Todos.query.get(id)
    return todo_schema.jsonify(todo)


# update
@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo=Todos.query.get(id)
    desc=request.json['desc']
    todo.desc = desc
    db.session.commit()
    return todo_schema.jsonify(todo)

# delete
@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo=Todos.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)

# run server

if __name__ == '__main__':
    app.run(debug=True)
