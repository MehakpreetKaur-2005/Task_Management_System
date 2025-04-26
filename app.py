from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    desc = db.Column(db.String(600), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):  
        return f"{self.sno} - {self.title}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

def create_db():
    with app.app_context():
        db.create_all()

create_db()

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc, user_id=session['user_id'])
        db.session.add(todo)
        db.session.commit()
    
    user = User.query.get(session['user_id'])
    if not user:
        # If user doesn't exist, clear session and redirect to login
        session.clear()
        flash('Session expired. Please login again.', 'warning')
        return redirect(url_for('login'))
        
    allTodo = Todo.query.filter_by(user_id=session['user_id']).all()
    
    # Calculate task statistics
    total_tasks = len(allTodo)
    completed_tasks = len([todo for todo in allTodo if todo.completed])
    pending_tasks = total_tasks - completed_tasks
    
    task_stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks
    }
    
    return render_template('index.html', allTodo=allTodo, username=user.username, task_stats=task_stats)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to index
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to index
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/delete/<int:sno>")
def delete(sno):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    todo = Todo.query.filter_by(sno=sno, user_id=session['user_id']).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    
    return redirect('/')

@app.route("/toggle_complete/<int:sno>")
def toggle_complete(sno):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    todo = Todo.query.filter_by(sno=sno, user_id=session['user_id']).first()
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    
    return redirect('/')

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    todo = Todo.query.filter_by(sno=sno, user_id=session['user_id']).first()
    
    if not todo:
        return redirect('/')
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect("/")
    
    return render_template('update.html', todo=todo)

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
