# Simple Nailmaster Notebook

A web application for nail technicians to manage clients, appointments, finances, and daily tasks. Built with a powder pink, elegant design.

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite + SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript (vanilla)

## Features

- **Dashboard** — daily overview with visit count, monthly earnings, today's schedule, client birthday reminders, and motivational quotes
- **Clients** — full CRUD, search by name or status (new / regular / VIP), tracks visit history
- **Appointments** — weekly schedule view, automatic pricing from procedure catalog, 5-minute break enforcement, working hours 10:00–19:00, status tracking
- **Finance** — earnings from completed appointments, manual expense tracking by category (materials, rent, instruments, other), spending breakdown
- **Checklists** — daily task lists with persistent storage

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd simple-nailmaster-notebook

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at `http://localhost:5000`.

## Project Structure

```
├── app.py                  # Flask app entry point
├── models.py               # SQLAlchemy database models
├── routes/                 # Route blueprints
│   ├── auth.py             # Login & registration
│   ├── dashboard.py        # Dashboard
│   ├── clients.py          # Client management
│   ├── appointments.py     # Appointment scheduling
│   ├── finance.py          # Finance tracking
│   └── checklists.py       # Daily checklists
├── templates/              # Jinja2 HTML templates
├── static/
│   ├── css/                # Stylesheets
│   ├── js/                 # Frontend scripts
│   └── images/             # Static images
└── references/
    ├── procedures.md       # Nail services catalog (prices & durations)
    └── motivational_phrases.md
```

## Notes

- Prices are in Ukrainian hryvnia (UAH)
- Time is displayed in 24-hour format
- Each user's data is fully isolated — users only see their own clients, appointments, and finances
