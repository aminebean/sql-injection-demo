import sqlite3
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    current_app,
)
from werkzeug.security import check_password_hash
from .auth import login_required

bp = Blueprint("routes", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.route("/login_vuln", methods=["GET", "POST"])
def login_vuln():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        conn = sqlite3.connect(current_app.config["DB_PATH"])
        cur = conn.cursor()

        query = (
            "SELECT id, username, role FROM users "
            f"WHERE username = '{username}' AND password_plain = '{password}';"
        )
        
        cur.execute(query)
        row = cur.fetchone()
        conn.close()

        if row:
            session["user_id"] = row[0]
            session["username"] = row[1]
            session["role"] = row[2]
            return redirect(url_for("routes.dashboard"))

        return render_template("login_vuln.html", error="Invalid credentials")

    return render_template("login_vuln.html")


@bp.route("/login_safe", methods=["GET", "POST"])
def login_safe():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        conn = sqlite3.connect(current_app.config["DB_PATH"])
        cur = conn.cursor()

        query = "SELECT id, username, password_hash, role FROM users WHERE username = ?"
        cur.execute(query, (username,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row[2], password):
            session["user_id"] = row[0]
            session["username"] = row[1]
            session["role"] = row[3]
            return redirect(url_for("routes.dashboard"))

        return render_template("login_safe.html", error="Invalid credentials")

    return render_template("login_safe.html")


@bp.get("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        role=session.get("role"),
    )


@bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("routes.index"))


@bp.get("/about")
def about():
    return render_template("about.html")
