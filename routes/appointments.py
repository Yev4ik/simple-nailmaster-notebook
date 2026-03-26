import os
from datetime import date, time, datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Appointment, Client, mark_past_appointments_done

appointments_bp = Blueprint('appointments', __name__)

PROCEDURES = {}


# Load procedures from references file
def load_procedures():
    global PROCEDURES
    if PROCEDURES:
        return PROCEDURES
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'references', 'procedures.md')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('|') and 'Procedure' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) == 3:
                    name, price, duration = parts
                    PROCEDURES[name] = {'price': int(price), 'duration': int(duration)}
    except FileNotFoundError:
        pass
    return PROCEDURES


@appointments_bp.route('/appointments')
@login_required
def appointments():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    week_offset = request.args.get('week', 0, type=int)
    start_of_week += timedelta(weeks=week_offset)
    end_of_week += timedelta(weeks=week_offset)

    week_appointments = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.date >= start_of_week,
        Appointment.date <= end_of_week
    ).order_by(Appointment.date, Appointment.time).all()

    # Group by day
    days = {}
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        days[day] = []
    for appt in week_appointments:
        if appt.date in days:
            days[appt.date].append(appt)

    procedures = load_procedures()
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.name).all()

    # Auto-mark past appointments as done
    mark_past_appointments_done(week_appointments)

    return render_template('appointments.html',
                           days=days,
                           procedures=procedures,
                           clients=clients,
                           week_offset=week_offset,
                           start_of_week=start_of_week,
                           end_of_week=end_of_week,
                           today=today)


# Add a new appointment
@appointments_bp.route('/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    client_id = request.form.get('client_id', type=int)
    procedure = request.form.get('procedure', '').strip()
    date_str = request.form.get('date', '').strip()
    time_str = request.form.get('time', '').strip()

    if not all([client_id, procedure, date_str, time_str]):
        flash('All fields are required.', 'error')
        return redirect(url_for('appointments.appointments'))

    # Validate client belongs to this user
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first()
    if not client:
        flash('Client not found. Please add the client first.', 'error')
        return redirect(url_for('appointments.appointments'))

    procedures = load_procedures()
    if procedure not in procedures:
        flash('Invalid procedure.', 'error')
        return redirect(url_for('appointments.appointments'))

    try:
        appt_date = date.fromisoformat(date_str)
        appt_time = time.fromisoformat(time_str)
    except ValueError:
        flash('Invalid date or time format.', 'error')
        return redirect(url_for('appointments.appointments'))

    # Cannot book in the past
    appt_datetime = datetime.combine(appt_date, appt_time)
    if appt_datetime < datetime.now():
        flash('Cannot add an appointment in the past.', 'error')
        return redirect(url_for('appointments.appointments'))

    # Working hours: 10:00–19:00
    appt_end_time = (appt_datetime + timedelta(minutes=procedures[procedure]['duration'])).time()
    if appt_time < time(10, 0) or appt_end_time > time(19, 0):
        flash('Appointments are only available between 10:00 and 19:00.', 'error')
        return redirect(url_for('appointments.appointments'))

    price = procedures[procedure]['price']
    duration = procedures[procedure]['duration']

    # Check: same client, same procedure, same day
    duplicate = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.client_id == client_id,
        Appointment.procedure == procedure,
        Appointment.date == appt_date,
        Appointment.status != 'cancelled'
    ).first()
    if duplicate:
        flash(f'{client.name} already has "{procedure}" on this day.', 'error')
        return redirect(url_for('appointments.appointments'))

    # Check time conflicts (5 min break between appointments)
    new_start = appt_datetime
    new_end = new_start + timedelta(minutes=duration)

    existing = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.date == appt_date,
        Appointment.status != 'cancelled'
    ).all()

    for ex in existing:
        ex_start = datetime.combine(ex.date, ex.time)
        ex_end = ex_start + timedelta(minutes=ex.duration)
        # Add 5 minute buffer
        ex_end_with_break = ex_end + timedelta(minutes=5)
        new_end_with_break = new_end + timedelta(minutes=5)

        if new_start < ex_end_with_break and ex_start < new_end_with_break:
            flash(f'Time conflict! There must be at least 5 minutes between appointments. Conflict with {ex.client.name} at {ex.time.strftime("%H:%M")}.', 'error')
            return redirect(url_for('appointments.appointments'))

    appointment = Appointment(
        user_id=current_user.id,
        client_id=client_id,
        procedure=procedure,
        price=price,
        duration=duration,
        date=appt_date,
        time=appt_time,
        status='on plan'
    )
    db.session.add(appointment)
    db.session.commit()
    flash(f'Appointment for {client.name} has been added.', 'success')
    return redirect(url_for('appointments.appointments'))


# Update appointment status
@appointments_bp.route('/appointments/status/<int:appt_id>', methods=['POST'])
@login_required
def update_status(appt_id):
    appt = Appointment.query.filter_by(id=appt_id, user_id=current_user.id).first_or_404()
    new_status = request.form.get('status', '').strip()
    if new_status in ['on plan', 'cancelled', 'did not come']:
        appt.status = new_status
        db.session.commit()
        flash(f'Appointment status updated to "{new_status}".', 'success')
    else:
        flash('Invalid status.', 'error')
    return redirect(url_for('appointments.appointments'))


# Get procedure info as JSON for frontend
@appointments_bp.route('/appointments/procedure-info/<procedure>')
@login_required
def procedure_info(procedure):
    procedures = load_procedures()
    if procedure in procedures:
        return jsonify(procedures[procedure])
    return jsonify({'error': 'Not found'}), 404
