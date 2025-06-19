# Expense Tracker Web Application



A full-featured web application for tracking personal expenses built with Python Flask and SQLite.

## Features

- 🧑‍💻 User authentication (Login/Register)
- 💰 Add, edit, and delete expenses
- 📊 Categorize expenses with custom categories
- 📅 Filter expenses by date ranges
- 📈 Budget tracking with visual indicators
- 🔍 Search and filter functionality
- 📱 Responsive design (works on mobile devices)

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite (with Flask-SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript (with Jinja2 templating)
- **Authentication**: Flask-Login with password hashing
- **Other Libraries**: 
  - WTForms for form validation

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Rikan-M/ExTrack.git
2. Install Requirments
  ```bash
   pip install -r requirments.txt
3. Move insede the folder
  ```bash
  cd ExpanseTracker
4. Run our project:
    ```bash
    python run.py
5. Run on web:
    copy the local host port on your web browser

## Project Structure
ExTrack
├──ExpanseTracker/
│  ├── app/                      # Application package
│  │   ├── __init__.py           # Application factory
│  │   ├── auth/                 # Authentication blueprints
│  │   ├── models.py             # Database models
│  │   ├── routes.py             # Main application routes
│  │   ├── static/               # Static files (CSS, JS, images)
│  │   ├── static/               # Static files (CSS, JS, images)
│  │   └── templates/            # Jinja2 templates
│  ├── instance/                 # Instance folder (database)
│  ├── run.py                    # Run file
├── requirements.txt             # Dependencies list
└── README.md                    # This is README.md

## Usage
1. Register a new account or login if you already have one

2. Add categories for your expenses (e.g., Food, Transportation)

3. Create budgets for each category if desired

4. Add expenses with amount, category, date, and optional notes

5. View your expense history and budget status on the dashboard

