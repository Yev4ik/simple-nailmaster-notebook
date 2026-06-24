import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)


# Validate password: min 8 chars, one special char, one number
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]', password):
        return False, "Password must contain at least one special character."
    return True, ""


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        form_data = {'name': name, 'email': email, 'phone': phone}

        if not all([name, email, phone, password]):
            flash('All fields are required.', 'error')
            return render_template('register.html', **form_data)

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('This email is already registered.', 'error')
            return render_template('register.html', **form_data)

        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'error')
            return render_template('register.html', **form_data)

        user = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Welcome! Your account has been created.', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not all([email, password]):
            flash('All fields are required.', 'error')
            return render_template('login.html', email=email)

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("You haven't registered yet!", 'error')
            return render_template('login.html', email=email)

        if not check_password_hash(user.password_hash, password):
            flash('Wrong email or password.', 'error')
            return render_template('login.html', email=email)

        login_user(user)
        return redirect(url_for('dashboard.dashboard'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
