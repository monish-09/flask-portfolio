from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import get_connection

app = Flask(__name__)
app.secret_key = "portfolio_secret"


@app.route("/")
def home():

    conn = get_connection()

    if conn.is_connected():
        print("✅ Database Connected Successfully!")

    conn.close()

    return render_template("index.html")


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
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(sql, (name, email, subject, message))
    conn.commit()

    cursor.close()
    conn.close()

    flash("✅ Thank you! Your message has been sent successfully.", "success")

    return render_template("index.html")




@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM contact_messages
        ORDER BY created_at DESC
    """)

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin.html", messages=messages)


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

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect(url_for("admin"))

        flash("Invalid Username or Password", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("login"))




if __name__ == "__main__":
    app.run(debug=True)