from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    monthly_income = db.Column(db.Float, default=0.0)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
    total_expense = sum(expense.amount for expense in expenses)
    
    return render_template('dashboard.html', 
                         expenses=expenses, 
                         total_expense=total_expense,
                         monthly_income=user.monthly_income)

@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    
    new_expense = Expense(
        amount=amount,
        category=category,
        description=description,
        date=date,
        user_id=current_user.id
    )
    
    db.session.add(new_expense)
    db.session.commit()
    
    flash('Expense added successfully!')
    return redirect(url_for('dashboard'))

@app.route('/delete_expense/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('dashboard'))
    
    db.session.delete(expense)
    db.session.commit()
    
    flash('Expense deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/update_income', methods=['POST'])
@login_required
def update_income():
    user = current_user
    user.monthly_income = float(request.form['monthly_income'])
    db.session.commit()
    
    flash('Monthly income updated successfully!')
    return redirect(url_for('dashboard'))

@app.route('/get_expense_data')
@login_required
def get_expense_data():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    # Calculate expenses by category
    categories = {}
    for expense in expenses:
        categories[expense.category] = categories.get(expense.category, 0) + expense.amount
    
    # Calculate monthly expenses
    monthly = {}
    for expense in expenses:
        month_key = expense.date.strftime('%Y-%m')
        monthly[month_key] = monthly.get(month_key, 0) + expense.amount
    
    return jsonify({
        'categories': categories,
        'monthly': monthly
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 