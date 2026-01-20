from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

USERS = {
    "user1": "password1",
    "user2": "password2"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if USERS.get(username) == password:
            session["user"] = username
            return redirect("/chat")
        return "Invalid credentials"

    return render_template("index.html")

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template("chat.html")

@socketio.on("message")
def handle_message(msg):
    user = session.get("user")
    if user:
        send(f"{user}: {msg}", broadcast=True)


if __name__ == "__main__":
    import os
socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


@socketio.on("disconnect")
def handle_disconnect():
    pass
