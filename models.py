from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta

db = SQLAlchemy()


# Mark past 'on plan' appointments as 'done' when their end time has passed
def mark_past_appointments_done(appointments):
    now = datetime.now()
    for appt in appointments:
        end_time = datetime.combine(appt.date, appt.time) + timedelta(minutes=appt.duration)
        if end_time <= now and appt.status == 'on plan':
            appt.status = 'done'
    db.session.commit()


# Registered nailmaster account with authentication fields
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    clients = db.relationship('Client', backref='user', lazy=True)
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    spendings = db.relationship('Spending', backref='user', lazy=True)
    checklists = db.relationship('Checklist', backref='user', lazy=True)


# Client profile with preferences, allergies and visit history
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    favourite_colours = db.Column(db.String(200), nullable=True)
    nail_shape = db.Column(db.String(20), nullable=True)  # square/oval/almond
    status = db.Column(db.String(20), default='new')  # new/regular/vip
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    appointments = db.relationship('Appointment', backref='client', lazy=True, cascade='all, delete-orphan')

    # Count completed visits from appointments table (not stored directly)
    @property
    def visit_count(self):
        return Appointment.query.filter_by(
            client_id=self.id,
            status='done'
        ).count()


# Scheduled visit with procedure, price and status tracking
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    procedure = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # minutes
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='on plan')  # on plan/cancelled/did not come/done
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# Business expense entry categorized for financial tracking
class Spending(db.Model):
    __tablename__ = 'spendings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # materials/rent/instruments/else
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# Daily task item with completion toggle
class Checklist(db.Model):
    __tablename__ = 'checklists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task = db.Column(db.String(300), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
