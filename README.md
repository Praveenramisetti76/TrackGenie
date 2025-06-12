# Personal Expense Tracker

A modern and interactive web-based personal expense tracker application built with Flask, designed to help you manage your finances effectively with a user-friendly interface and insightful data visualizations.

## Features

### 🔐 User Authentication
- **Registration**: Allows new users to create accounts securely.
- **Login**: Existing users can log in to access their personalized dashboard.
- **Secure Password Hashing**: Passwords are securely stored using `werkzeug.security`.
- **Session Management**: Maintains user sessions for a seamless experience.

### 🖥️ Modern User Interface (UI)
- **Responsive Design**: Built with Bootstrap 5 for a clean, modern, and mobile-friendly layout.
- **Dark Mode**: Toggle between light and dark themes for improved readability and user preference.
- **Interactive Charts**: Utilizes Chart.js for dynamic and visually appealing data visualizations.
- **Font Awesome Icons**: Enhances the UI with a wide range of recognizable icons.
- **Animated Elements**: Smooth fade-in, slide animations, and hover effects for a dynamic user experience.
- **Comprehensive Layout**: Includes a header, footer with social media links, and a card-based design for clear content organization.

### 📊 Dashboard Functionality
- **Add Expenses**: Easily record new expenses with fields for amount, category, description, and date.
- **View Total Expenses**: Displays a real-time sum of all recorded expenses.
- **Monthly Income Tracking**: Input and update your monthly income to compare against your spending.
- **Expense Suggestions**: Provides smart, data-driven suggestions based on spending patterns, monthly trends, and income-to-expense ratio to help manage finances.
- **Recent Expenses Table**: A well-formatted table listing recent expenses with options to delete individual entries.

### 📈 Data Visualization
- **Expenses by Category (Pie Chart)**: Visualizes the distribution of your spending across different categories.
- **Monthly Comparison (Bar Chart)**: Compares your expenses month-to-month, helping to identify spending trends.
- **Income vs Expenses (Line Chart)**: Tracks your monthly income against your expenses over time, providing insights into your financial health.

## Tech Stack

- **Backend**: Flask (Python framework), SQLAlchemy (ORM for database)
- **Frontend**: HTML5, CSS3 (with Bootstrap 5), JavaScript (with Chart.js)
- **Database**: SQLite
- **Other**: Jinja2 (templating engine), Font Awesome (icons)

## Installation

1. Make sure you have Python 3.6 or higher installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`.
3. Register a new account or log in if you already have one.
4. Start tracking your expenses and explore your financial data on the dashboard.

## Database

The application uses a SQLite database (`expenses.db`) to store user and expense data. This file is automatically created when the application is run for the first time.

## Predefined Categories

- Food
- Transport
- Entertainment
- Shopping
- Bills
- Healthcare
- Education
- Travel
- Housing
- Personal Care
- Gifts
- Other

## Export Format

When exporting expenses to CSV, the following information is included:
- Date and time
- Amount
- Category
- Description

The exported file is named with the current timestamp for easy identification. 