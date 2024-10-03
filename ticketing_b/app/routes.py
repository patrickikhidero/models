from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Ticket
from .forms import RegistrationForm, LoginForm, TicketForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/submit_ticket', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    if current_user.is_admin:
        return redirect(url_for('main.index')), 403
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been submitted!')
        return redirect(url_for('main.index'))
    return render_template('submit_ticket.html', form=form)

@main.route('/manage_tickets')
@login_required
def manage_tickets():
    if not current_user.is_admin:
        return redirect(url_for('main.index')), 403
    tickets = Ticket.query.all()
    return render_template('manage_tickets.html', tickets=tickets)