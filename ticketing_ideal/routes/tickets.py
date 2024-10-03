from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Ticket

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/dashboard')
@login_required
def user_dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', tickets=tickets)

@tickets_bp.route('/submit-ticket', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_ticket = Ticket(title=title, description=description, user_id=current_user.id)
        db.session.add(new_ticket)
        db.session.commit()

        flash('Ticket submitted successfully!', 'success')
        return redirect(url_for('tickets.user_dashboard'))

    return render_template('ticket_form.html')
