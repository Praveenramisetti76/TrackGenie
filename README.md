# Personal Expense Tracker

A modern web application for tracking personal expenses with beautiful visualizations and user-friendly features.

## Features

- User authentication and secure login
- Expense tracking with categories
- Monthly income tracking
- Interactive charts and analytics
- Dark mode support
- Responsive design
- Monthly comparison views

## Deployment Instructions

### Deploying to Render.com

1. Create a Render account at https://render.com

2. Create a new Web Service:
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Choose a name for your service
   - Select "Python" as the runtime
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn app:app`
   - Add the following environment variables:
     - `FLASK_APP=app.py`
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-secret-key-here`
     - `DATABASE_URL=sqlite:///expenses.db`

3. Click "Create Web Service"

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`
5. Run the application:
   ```bash
   flask run
   ```

## Technologies Used

- Flask
- SQLAlchemy
- Bootstrap 5
- Chart.js
- SQLite
- Flask-Login
- Flask-WTF

run locally:

$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
## License

MIT License 