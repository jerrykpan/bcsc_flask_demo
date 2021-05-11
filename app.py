from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 

db = SQLAlchemy(app)

class Tasklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Task {}".format(self.id)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content']

        new_task = Tasklist(content=task_content)

        try:
            db.session.add(new_task)

            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task"
    else:
        tasks = Tasklist.query.order_by(Tasklist.date_created).all()

        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Tasklist.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)

        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting your task."

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    task_to_update = Tasklist.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating your task."
    else:
        return render_template('update.html', task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)