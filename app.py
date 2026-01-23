from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import secrets, os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

# CHANGE THESE
USERS = {
    "itx_ankelet25": "Hydrogen",
    "jatin25": "Zinc"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        if USERS.get(u) == p:
            session["user"] = u
            return redirect("/chat")
        return "Invalid login"
    return render_template("index.html")

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template("chat.html", username=session["user"])

@socketio.on("send_message")
def handle_message(data):
    user = session.get("user")
    if user:
        emit("receive_message", {
            "user": user,
            "type": data["type"],
            "content": data["content"]
        }, broadcast=True)

@app.route("/inbox")
def inbox():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("inbox.html", username=session["username"])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0",
                 port=int(os.environ.get("PORT", 5000)))






