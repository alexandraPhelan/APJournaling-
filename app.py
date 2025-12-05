# AP x20245823
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET_KEY", "fallback-key-change-me")
app.config["DEBUG"] = False   

DB_PATH = "apjournaling.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_pw),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        # Check hashed password
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            return render_template(
                "login.html", error="Invalid username or password"
            )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def require_login():
    return "user_id" in session


@app.route("/dashboard")
def dashboard():
    if not require_login():
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, created_at FROM entries WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],),
    )
    entries = cur.fetchall()
    conn.close()

    return render_template("dashboard.html", entries=entries)


@app.route("/entries/new", methods=["GET", "POST"])
def create_entry():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO entries (user_id, title, body) VALUES (?, ?, ?)",
            (session["user_id"], title, body),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("create_entry.html")


@app.route("/entries/<int:entry_id>")
def view_entry(entry_id):
    if not require_login():
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM entries WHERE id = ? AND user_id = ?",
        (entry_id, session["user_id"]),
    )
    entry = cur.fetchone()
    conn.close()

    if not entry:
        return "Entry not found", 404

    return render_template("view_entry.html", entry=entry)


@app.route("/entries/<int:entry_id>/edit", methods=["GET", "POST"])
def edit_entry(entry_id):
    if not require_login():
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM entries WHERE id = ? AND user_id = ?", 
        (entry_id, session["user_id"])
    )
    entry = cur.fetchone()

    if not entry:
        conn.close()
        return "Entry not found", 404

    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        cur.execute(
            "UPDATE entries SET title = ?, body = ? WHERE id = ?",
            (title, body, entry_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("view_entry", entry_id=entry_id))

    conn.close()
    return render_template("edit_entry.html", entry=entry)


@app.route("/entries/<int:entry_id>/delete", methods=["POST"])
def delete_entry(entry_id):
    if not require_login():
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM entries WHERE id = ? AND user_id = ?", 
        (entry_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/search")
def search():
    if not require_login():
        return redirect(url_for("login"))

    q = request.args.get("q", "")

    conn = get_db()
    cur = conn.cursor()
    like_term = f"%{q}%"
    cur.execute(
        "SELECT id, title, created_at FROM entries "
        "WHERE user_id = ? AND (title LIKE ? OR body LIKE ?) "
        "ORDER BY created_at DESC",
        (session["user_id"], like_term, like_term),
    )
    results = cur.fetchall()
    conn.close()

    return render_template("search.html", query=q, results=results)


if __name__ == "__main__":
    app.run()
