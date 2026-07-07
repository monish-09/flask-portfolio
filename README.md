# Flask Portfolio Website

A modern and responsive portfolio website built with **Flask**. This project includes a secure admin panel to manage contact messages, email notifications, OTP-based password reset, and SQLite database integration.

---

## Features

- Responsive Portfolio Website
- Contact Form
- Email Notification on New Contact Submission
- Secure Admin Login
- Admin Dashboard
- Search Contact Messages
- Delete Messages
- Export Messages to CSV
- Admin Profile Update
- Forgot Password with Email OTP Verification
- Password Reset
- SQLite Database
- Flash Messages
- Responsive UI

---

## Tech Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Jinja2

---

## Project Structure

```
flask-portfolio/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── app.py
├── database.py
├── create_db.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/monish-09/flask-portfolio.git

cd flask-portfolio
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python create_db.py
```

Create an admin account before running the application.

Start the application:

```bash
python app.py
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SECRET_KEY=your_secret_key
```

> **Note:** Never upload your `.env` file to GitHub.

---

## Database

This project uses **SQLite** as the database.

Tables:

- admin
- contact_messages

---

## Security Features

- Password Hashing
- Session Authentication
- OTP Verification
- Password Reset
- Protected Admin Routes

---

## Future Improvements

- Dark Mode
- Admin Activity Logs
- Message Reply System
- Image Upload Support
- Multiple Admin Accounts

---

## Author

**Monish**

GitHub:
https://github.com/monish-09

---

## License

This project is created for learning and portfolio purposes.