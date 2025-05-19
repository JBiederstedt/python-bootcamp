from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
todo_app = Flask(__name__)

database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'todo.db')
todo_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_file}'
todo_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(todo_app)

# Database model for a task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id} {self.title!r}>'

# Create the database (if not exists)
with todo_app.app_context():
    db.create_all()

@todo_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Add a new task
        task_title = request.form.get('title')
        if task_title:
            new_task = Task(title=task_title)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('index'))

    # Show all tasks
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@todo_app.route('/complete/<int:task_id>')
def complete(task_id):
    # Toggle task completion
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@todo_app.route('/delete/<int:task_id>')
def delete(task_id):
    # Delete a task
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    todo_app.run(debug=True)
