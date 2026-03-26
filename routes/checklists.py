from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Checklist

checklists_bp = Blueprint('checklists', __name__)


@checklists_bp.route('/checklists')
@login_required
def checklists():
    today = date.today()
    date_filter = request.args.get('date', str(today))

    try:
        filter_date = date.fromisoformat(date_filter)
    except ValueError:
        filter_date = today

    tasks = Checklist.query.filter_by(
        user_id=current_user.id,
        date=filter_date
    ).order_by(Checklist.is_done, Checklist.created_at).all()

    total_tasks = len(tasks)
    done_tasks = sum(1 for t in tasks if t.is_done)

    return render_template('checklists.html', tasks=tasks, filter_date=filter_date, today=today,
                           total_tasks=total_tasks, done_tasks=done_tasks)


# Add a task
@checklists_bp.route('/checklists/add', methods=['POST'])
@login_required
def add_task():
    task_text = request.form.get('task', '').strip()
    date_str = request.form.get('date', '').strip()

    if not task_text:
        flash('Task text is required.', 'error')
        return redirect(url_for('checklists.checklists'))

    try:
        task_date = date.fromisoformat(date_str) if date_str else date.today()
    except ValueError:
        task_date = date.today()

    task = Checklist(
        user_id=current_user.id,
        task=task_text,
        date=task_date
    )
    db.session.add(task)
    db.session.commit()
    flash('Task has been added.', 'success')
    return redirect(url_for('checklists.checklists', date=str(task_date)))


# Toggle task completion
@checklists_bp.route('/checklists/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Checklist.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('checklists.checklists', date=str(task.date)))


# Edit a task
@checklists_bp.route('/checklists/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Checklist.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    new_text = request.form.get('task', '').strip()
    if not new_text:
        flash('Task text cannot be empty.', 'error')
    else:
        task.task = new_text
        db.session.commit()
        flash('Task has been updated.', 'success')
    return redirect(url_for('checklists.checklists', date=str(task.date)))


# Delete a task
@checklists_bp.route('/checklists/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Checklist.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task_date = task.date
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted.', 'success')
    return redirect(url_for('checklists.checklists', date=str(task_date)))
