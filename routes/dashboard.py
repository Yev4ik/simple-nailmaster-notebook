import os
import random
from datetime import date, timedelta, datetime, time
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Appointment, Client, mark_past_appointments_done

dashboard_bp = Blueprint('dashboard', __name__)


# Load motivational phrases from file
def get_random_phrase():
    phrases_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'references', 'motivational_phrases.md')
    try:
        with open(phrases_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        phrases = [line.strip('- \n') for line in lines if line.startswith('- ')]
        return random.choice(phrases) if phrases else "Have a great day!"
    except FileNotFoundError:
        return "Have a great day!"


# Get clients with birthdays in next 7 days
def get_upcoming_birthdays(user_id):
    clients = Client.query.filter_by(user_id=user_id).filter(Client.birthday.isnot(None)).all()
    today = date.today()
    upcoming = []
    for client in clients:
        bday_this_year = client.birthday.replace(year=today.year)
        if bday_this_year < today:
            bday_this_year = client.birthday.replace(year=today.year + 1)
        days_until = (bday_this_year - today).days
        if 0 <= days_until <= 7:
            upcoming.append({'name': client.name, 'date': bday_this_year, 'days_until': days_until})
    return sorted(upcoming, key=lambda x: x['days_until'])


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    first_day_of_month = today.replace(day=1)

    # Today's appointments
    todays_appointments = Appointment.query.filter_by(
        user_id=current_user.id,
        date=today
    ).order_by(Appointment.time).all()

    visits_today = len(todays_appointments)

    # Monthly earnings (done appointments)
    monthly_appointments = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.date >= first_day_of_month,
        Appointment.date <= today,
        Appointment.status == 'done'
    ).all()
    monthly_earnings = sum(a.price for a in monthly_appointments)

    # Mark past appointments as done if status is still 'on plan'
    mark_past_appointments_done(todays_appointments)

    # Notifications
    birthdays = get_upcoming_birthdays(current_user.id)
    phrase = get_random_phrase()

    return render_template('dashboard.html',
                           visits_today=visits_today,
                           monthly_earnings=monthly_earnings,
                           todays_appointments=todays_appointments,
                           birthdays=birthdays,
                           phrase=phrase,
                           today=today,
                           user_name=current_user.name)
