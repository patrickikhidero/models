from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import User, Ticket
from app.forms import RegistrationForm, LoginForm, TicketForm

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'user':
        return render_template('user_dashboard.html', tickets=current_user.tickets)
    elif current_user.role == 'admin':
        return render_template('admin_dashboard.html', tickets=Ticket.query.all())
    return "Access Denied", 403

@bp.route('/submit_ticket', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    if current_user.role != 'user':
        return "Access Denied", 403
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been submitted!', 'success')
        return redirect(url_for('routes.dashboard'))
    return render_template('submit_ticket.html', form=form)
