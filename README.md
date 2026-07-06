# 🚀 Flask Portfolio Website

A modern **Flask Portfolio Website** built with **Flask, MySQL, HTML, CSS, and JavaScript**. The project includes a secure **Admin Dashboard** for managing contact messages with OTP-based password reset and a responsive user interface.

---

# ✨ Features

## 🌐 Portfolio Website
- Responsive Design
- Dark / Light Mode
- About Section
- Skills Section
- Projects Section
- Contact Form

## 🔐 Admin Authentication
- Secure Admin Login
- Password Hashing
- Show / Hide Password
- Forgot Password via Email OTP
- OTP Verification
- OTP Expiry (5 Minutes)
- Reset Password
- Change Username
- Change Password
- Logout

## 📩 Contact Management
- Store Contact Messages
- View Full Message
- Delete Messages
- Search by Name or Email
- Pagination
- Export Messages as CSV

## 🎨 UI Features
- Premium Authentication UI
- Modern Admin Dashboard
- Responsive Layout
- Flash Messages
- Password Visibility Toggle

---

# 🛠 Tech Stack

### Backend
- Python
- Flask

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- MySQL

### Email Service
- Gmail SMTP

---

# 📂 Project Structure

```text
portfolio/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
└── database/
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/monish-09/portfolio.git
```

Move into the project folder

```bash
cd portfolio
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
python app.py
```

---

# 🔑 Environment Variables

Create a `.env` file and add:

```env
SECRET_KEY=your_secret_key

EMAIL_USER=your_email@gmail.com

EMAIL_PASSWORD=your_app_password

DB_HOST=localhost

DB_USER=root

DB_PASSWORD=your_password

DB_NAME=portfolio
```

---

# 📌 Future Improvements

- Activity Logs
- Multi Admin Support
- Dashboard Analytics
- Docker Support

---

# 👨‍💻 Author

**Monish**

GitHub:
https://github.com/monish-09

---

# ⭐ Support

If you like this project, consider giving it a **Star ⭐** on GitHub.