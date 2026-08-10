from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ==========================================
# 👤 CITIZEN LOGIN ROUTE
# ==========================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If an Admin tries to access the citizen login, log them out first.
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            logout_user()
            flash('Admin session securely closed. Please log in as a Citizen.', 'info')
        else:
            return redirect(url_for('citizen.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password combination. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        if user.role == 'admin':
            flash('This portal is for Citizens only. Please use the Admin Command Center login.', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=False)
        flash(f'Welcome back, {user.name}!', 'success')

        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('citizen.dashboard'))

    return render_template('auth/login.html')

# ==========================================
# 🏢 ADMIN COMMAND CENTER LOGIN ROUTE
# ==========================================
@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    # If a Citizen tries to access the admin login, log them out first.
    if current_user.is_authenticated:
        if current_user.role == 'citizen':
            logout_user()
            flash('Citizen session securely closed. Please log in with Administrator credentials.', 'info')
        else:
            return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid Admin email or password. Access Denied.', 'danger')
            return redirect(url_for('auth.admin_login'))

        if user.role != 'admin':
            flash('Access Denied: You do not have Administrator privileges.', 'danger')
            return redirect(url_for('auth.admin_login'))

        login_user(user, remember=False)
        flash(f'Command Center Access Granted. Welcome, {user.name}.', 'success')

        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))

    return render_template('auth/admin_login.html')

# ==========================================
# 👤 CITIZEN REGISTRATION ROUTE
# ==========================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logout_user()  # Force logout to allow fresh registration

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('An account with this email address already exists. Please sign in.', 'warning')
            return redirect(url_for('auth.login'))

        hashed_pwd = generate_password_hash(password, method='scrypt')
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_pwd,
            role='citizen'
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Registration successful! Welcome to CityPulse AI.', 'success')
        return redirect(url_for('citizen.dashboard'))

    return render_template('auth/register.html')

# ==========================================
# 🚪 LOGOUT ROUTE
# ==========================================
@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been signed out successfully.', 'info')
    return redirect(url_for('main.index'))