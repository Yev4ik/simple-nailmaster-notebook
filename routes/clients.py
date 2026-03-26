from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Client
from datetime import date

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/clients')
@login_required
def clients():
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()

    query = Client.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(Client.name.ilike(f'%{search}%'))
    if status_filter:
        query = query.filter_by(status=status_filter)

    clients_list = query.order_by(Client.name).all()
    return render_template('clients.html', clients=clients_list, search=search, status_filter=status_filter)


# Add a new client
@clients_bp.route('/clients/add', methods=['POST'])
@login_required
def add_client():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    birthday_str = request.form.get('birthday', '').strip()
    notes = request.form.get('notes', '').strip()
    allergies = request.form.get('allergies', '').strip()
    favourite_colours = request.form.get('favourite_colours', '').strip()
    nail_shape = request.form.get('nail_shape', '').strip()
    status = request.form.get('status', 'new').strip()

    if not name or not phone:
        flash('Name and phone are required.', 'error')
        return redirect(url_for('clients.clients'))

    birthday = None
    if birthday_str:
        try:
            birthday = date.fromisoformat(birthday_str)
        except ValueError:
            flash('Invalid birthday format.', 'error')
            return redirect(url_for('clients.clients'))

    client = Client(
        user_id=current_user.id,
        name=name,
        phone=phone,
        birthday=birthday,
        notes=notes,
        allergies=allergies,
        favourite_colours=favourite_colours,
        nail_shape=nail_shape,
        status=status
    )
    db.session.add(client)
    db.session.commit()
    flash(f'Client "{name}" has been added.', 'success')
    return redirect(url_for('clients.clients'))


# Edit a client
@clients_bp.route('/clients/edit/<int:client_id>', methods=['POST'])
@login_required
def edit_client(client_id):
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()

    client.name = request.form.get('name', client.name).strip()
    client.phone = request.form.get('phone', client.phone).strip()
    birthday_str = request.form.get('birthday', '').strip()
    client.notes = request.form.get('notes', '').strip()
    client.allergies = request.form.get('allergies', '').strip()
    client.favourite_colours = request.form.get('favourite_colours', '').strip()
    client.nail_shape = request.form.get('nail_shape', '').strip()
    client.status = request.form.get('status', client.status).strip()

    if birthday_str:
        try:
            client.birthday = date.fromisoformat(birthday_str)
        except ValueError:
            flash('Invalid birthday format.', 'error')
            return redirect(url_for('clients.clients'))
    else:
        client.birthday = None

    db.session.commit()
    flash(f'Client "{client.name}" has been updated.', 'success')
    return redirect(url_for('clients.clients'))


# Delete a client
@clients_bp.route('/clients/delete/<int:client_id>', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()
    name = client.name
    db.session.delete(client)
    db.session.commit()
    flash(f'Client "{name}" has been deleted.', 'success')
    return redirect(url_for('clients.clients'))
