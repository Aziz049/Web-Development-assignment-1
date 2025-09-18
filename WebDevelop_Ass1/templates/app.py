
# app.py
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
# Use environment variable in production. Default below for dev convenience.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-please-change")

@app.route("/")
def home():
    """Home page (welcome)."""
    return render_template("home.html")

@app.route("/sign", methods=["GET", "POST"])
def sign():
    """
    GET: show form
    POST: accept 'name' from form, add entry to session['guestbook'], redirect to /guestbook
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            # store timestamp as string so session JSON-serializable
            entry = {
                "name": name,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            guestbook = session.get("guestbook", [])
            # Make latest entries appear first:
            guestbook.insert(0, entry)
            session["guestbook"] = guestbook
        return redirect(url_for("guestbook"))
    return render_template("sign.html")

@app.route("/guestbook")
def guestbook():
    """Display all signed names (latest first)."""
    entries = session.get("guestbook", [])
    return render_template("guestbook.html", entries=entries)

@app.route("/clear")
def clear():
    """Clear all entries from the guestbook (reset)."""
    session.pop("guestbook", None)
    return redirect(url_for("guestbook"))

if __name__ == "__main__":
    # For development only. In production use a proper WSGI server.
    app.run(debug=True)
