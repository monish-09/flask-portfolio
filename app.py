from flask import Flask, render_template, request, flash, redirect, url_for, session,Response
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection
import csv
import math
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import random
import time

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    print("✅ SQLite Connected Successfully!")

    conn.close()
    return render_template("index.html")

def send_email(name, email, subject, message):

    body = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

    msg = MIMEText(body)

    msg["Subject"] = "New Portfolio Contact"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("✅ Email Sent Successfully")

    except Exception as e:

        print("❌ Email Error:", e)


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    subject = request.form["subject"].strip()
    message = request.form["message"].strip()

    # Validation
    if not name or not email or not subject or not message:
        flash("❌ Please fill all the fields!", "error")
        return render_template("index.html")

    if len(message) < 10:
        flash("❌ Message should contain at least 10 characters.", "error")
        return render_template("index.html")

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO contact_messages(name,email,subject,message)
    VALUES(?,?,?,?)
    """



    cursor.execute(sql, (name, email, subject, message))
    conn.commit()

    send_email(name, email, subject, message)

    cursor.close()
    conn.close()

    flash("✅ Thank you! Your message has been sent successfully.", "success")

    return render_template("index.html")




@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_connection()
    cursor = conn.cursor()

    # Total Messages
    cursor.execute("SELECT COUNT(*) FROM contact_messages")
    otal_messages = cursor.fetchone()[0]

    # Today's Messages
    cursor.execute("""
    SELECT COUNT(*)
    FROM contact_messages
    WHERE DATE(created_at)=DATE('now')
    """)

    today_messages = cursor.fetchone()[0]

    # Search
    if search:

        cursor.execute("""
        SELECT *
        FROM contact_messages
        WHERE name LIKE ? OR email LIKE ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """, (f"%{search}%", f"%{search}%", per_page, offset))

    else:

       cursor.execute("""
        SELECT *
        FROM contact_messages
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """, (per_page, offset))

    rows = cursor.fetchall()

    contact_messages = []

    for row in rows:
        contact_messages.append(dict(row))

    total_pages = math.ceil(total_messages / per_page)

    cursor.close()
    conn.close()

    return render_template(
    "admin.html",
    messages=contact_messages,
    total_messages=total_messages,
    today_messages=today_messages,
    username=session["username"],
    page=page,
    total_pages=total_pages,
    search=search
)


@app.route("/delete/<int:id>")
def delete_message(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contact_messages WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Message deleted successfully!", "success")

    return redirect(url_for("admin"))



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM admin WHERE username=?",
        (username,)
        )

        row = cursor.fetchone()

        admin = dict(row) if row else None

        cursor.close()
        conn.close()

        if admin and check_password_hash(admin["password"], password):

            session["admin"] = True
            session["admin_id"] = admin["id"]
            session["username"] = admin["username"]

            flash("Login Successful!", "success")

            return redirect(url_for("admin"))

        flash("Invalid Username or Password", "error")

    return render_template("login.html")



@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM admin WHERE id=%s",
        (session["admin_id"],)
    )

    admin = cursor.fetchone()

    if request.method == "POST":

        username = request.form["username"]
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not check_password_hash(admin["password"], current_password):

            flash("Current Password is incorrect.", "error")

        elif new_password != confirm_password:

            flash("New passwords do not match.", "error")

        else:

            hashed_password = generate_password_hash(new_password)

            cursor.execute("""
                UPDATE admin
                SET username=%s, password=%s
                WHERE id=%s
            """, (username, hashed_password, session["admin_id"]))

            conn.commit()

            session["username"] = username

            flash("Profile updated successfully!", "success")

            cursor.close()
            conn.close()

            return redirect(url_for("profile"))

    cursor.close()
    conn.close()

    return render_template("profile.html", admin=admin)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admin WHERE email=%s",
            (email,)
        )

        admin = cursor.fetchone()

        if not admin:

            flash("Email not found.", "error")

            cursor.close()
            conn.close()

            return render_template("forgot_password.html")

        otp = str(random.randint(100000,999999))

        session["otp"] = otp
        session["reset_email"] = email
        session["otp_time"] = time.time()
        session["otp_attempts"] = 0
        session["otp_lock_time"] = None

        body = f"""
Hello Admin,

Your Password Reset OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.
"""

        msg = MIMEText(body)

        msg["Subject"] = "Password Reset OTP"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        try:

            server = smtplib.SMTP("smtp.gmail.com",587)

            server.starttls()

            server.login(EMAIL_USER, EMAIL_PASSWORD)

            server.send_message(msg)

            server.quit()

        except Exception as e:

            flash("Unable to send OTP.", "error")

            print(e)

            cursor.close()
            conn.close()

            return render_template("forgot_password.html")

        cursor.close()
        conn.close()

        return redirect(url_for("verify_otp"))

    return render_template("forgot_password.html")

@app.route("/logout")
def logout():

    session.clear()

    flash("Logout Successful!", "success")

    return redirect(url_for("login"))


@app.route("/export")
def export_csv():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email, subject, message, created_at
        FROM contact_messages
        ORDER BY created_at DESC
    """)

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    def generate():

        data = csv.writer

        yield "ID,Name,Email,Subject,Message,Date\n"

        for msg in messages:

            yield f'{msg["id"]},"{msg["name"]}","{msg["email"]}","{msg["subject"]}","{msg["message"]}","{msg["created_at"]}"\n'

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=messages.csv"
        }
    )

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        # Check if account is temporarily locked

        lock_time = session.get("otp_lock_time")

        if lock_time:

            if time.time() - lock_time < 300:

                flash("Too many failed attempts. Please try again after 5 minutes.", "error")

                return render_template("verify_otp.html")

            else:

                session["otp_attempts"] = 0
                session["otp_lock_time"] = None

        user_otp = request.form["otp"].strip()
        # OTP Expiry Check (5 minutes)

        otp_time = session.get("otp_time")

        if otp_time is None:

            flash("OTP session expired.", "error")
            return redirect(url_for("forgot_password"))

        if time.time() - otp_time > 300:

            session.pop("otp", None)
            session.pop("otp_time", None)
            session.pop("reset_email", None)

            flash("OTP has expired. Please request a new OTP.", "error")

            return redirect(url_for("forgot_password"))        

        if user_otp == session.get("otp"):

            session["otp_attempts"] = 0
            session["otp_lock_time"] = None
            
            flash("OTP Verified Successfully!", "success")

            return redirect(url_for("reset_password"))

        else:

            attempts = session.get("otp_attempts", 0) + 1

            session["otp_attempts"] = attempts

            if attempts >= 5:

                session["otp_lock_time"] = time.time()

                flash("Too many failed attempts. Account locked for 5 minutes.", "error")

            else:

                flash(f"Invalid OTP. Attempts left: {5-attempts}", "error")

    return render_template("verify_otp.html")

@app.route("/resend-otp")
def resend_otp():

    if "reset_email" not in session:

        flash("Session expired. Please try again.", "error")
        return redirect(url_for("forgot_password"))

    email = session["reset_email"]

    otp = str(random.randint(100000,999999))

    session["otp"] = otp
    session["otp_time"] = time.time()

    body = f"""
Hello Admin,

Your new Password Reset OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.
"""

    msg = MIMEText(body)

    msg["Subject"] = "New Password Reset OTP"
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        flash("A new OTP has been sent to your email.", "success")

    except Exception as e:

        print(e)

        flash("Unable to resend OTP.", "error")

    return redirect(url_for("verify_otp"))

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "reset_email" not in session:
        flash("Session expired. Please try again.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        new_password = request.form["new_password"].strip()
        confirm_password = request.form["confirm_password"].strip()

        if new_password != confirm_password:

            flash("Passwords do not match.", "error")
            return render_template("reset_password.html")

        hashed_password = generate_password_hash(new_password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE admin
            SET password=%s
            WHERE email=%s
            """,
            (hashed_password, session["reset_email"])
        )

        conn.commit()

        cursor.close()
        conn.close()

        # OTP session remove
        session.pop("otp", None)
        session.pop("reset_email", None)

        flash("Password reset successfully. Please login.", "success")

        return redirect(url_for("login"))

    return render_template("reset_password.html")

if __name__ == "__main__":
    app.run(debug=True)