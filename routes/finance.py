from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Appointment, Spending

finance_bp = Blueprint('finance', __name__)


@finance_bp.route('/finance')
@login_required
def finance():
    today = date.today()
    first_day = today.replace(day=1)

    # Earnings from done appointments this month
    done_appointments = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.date >= first_day,
        Appointment.date <= today,
        Appointment.status == 'done'
    ).order_by(Appointment.date).all()

    total_earnings = sum(a.price for a in done_appointments)

    # Spendings this month
    spendings = Spending.query.filter(
        Spending.user_id == current_user.id,
        Spending.date >= first_day,
        Spending.date <= today
    ).order_by(Spending.date.desc()).all()

    total_spendings = sum(s.amount for s in spendings)

    # Spendings by category, sorted from highest to lowest
    category_totals = {}
    for s in spendings:
        category_totals[s.category] = category_totals.get(s.category, 0) + s.amount
    by_category = dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))

    net_profit = total_earnings - total_spendings

    return render_template('finance.html',
                           done_appointments=done_appointments,
                           spendings=spendings,
                           total_earnings=total_earnings,
                           total_spendings=total_spendings,
                           net_profit=net_profit,
                           by_category=by_category,
                           today=today)


# Add a spending
@finance_bp.route('/finance/add', methods=['POST'])
@login_required
def add_spending():
    amount = request.form.get('amount', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    date_str = request.form.get('date', '').strip()

    if not amount or not category or not date_str:
        flash('Amount, category and date are required.', 'error')
        return redirect(url_for('finance.finance'))

    if category not in ['materials', 'rent', 'instruments', 'else']:
        flash('Invalid category.', 'error')
        return redirect(url_for('finance.finance'))

    try:
        amount_val = int(amount)
        if amount_val <= 0:
            raise ValueError
    except ValueError:
        flash('Amount must be a positive number.', 'error')
        return redirect(url_for('finance.finance'))

    try:
        spending_date = date.fromisoformat(date_str)
    except ValueError:
        flash('Invalid date format.', 'error')
        return redirect(url_for('finance.finance'))

    spending = Spending(
        user_id=current_user.id,
        amount=amount_val,
        category=category,
        description=description,
        date=spending_date
    )
    db.session.add(spending)
    db.session.commit()
    flash('Spending has been added.', 'success')
    return redirect(url_for('finance.finance'))


# Delete a spending
@finance_bp.route('/finance/delete/<int:spending_id>', methods=['POST'])
@login_required
def delete_spending(spending_id):
    spending = Spending.query.filter_by(id=spending_id, user_id=current_user.id).first_or_404()
    db.session.delete(spending)
    db.session.commit()
    flash('Spending has been deleted.', 'success')
    return redirect(url_for('finance.finance'))
