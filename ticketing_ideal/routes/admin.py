from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Ticket

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('tickets.user_dashboard'))
    
    tickets = Ticket.query.all()
    return render_template('admin_dashboard.html', tickets=tickets)

@admin_bp.route('/admin/manage/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def manage_ticket(ticket_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('tickets.user_dashboard'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == 'POST':
        ticket.status = request.form['status']
        db.session.commit()
        flash('Ticket status updated!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('manage_tickets.html', ticket=ticket)
