from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

messages = []

HTML = """<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qahramon Chat</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body{margin:0;background:#f0f2f5;font-family:Arial;height:100vh;display:flex;flex-direction:column}
        #messages{flex:1;overflow-y:auto;padding:20px;background:white}
        .msg{margin:10px 0;padding:12px 16px;border-radius:20px;max-width:80%;word-wrap:break-word}
        .mine{background:#0084ff;color:white;margin-left:auto;border-bottom-right-radius:4px}
        .other{background:#e5e5ea;color:black;border-bottom-left-radius:4px}
        .name{font-weight:bold;font-size:0.8em;margin-bottom:3px}
        form{padding:10px;background:white;border-top:1px solid #ddd;display:flex;gap:10px}
        input{flex:1;padding:14px;border-radius:25px;border:1px solid #ddd}
        button{padding:14px 25px;background:#0084ff;color:white;border:none;border-radius:25px;cursor:pointer}
    </style>
</head>
<body>
<div id="messages"></div>
<form onsubmit="send();return false;">
    <input id="name" placeholder="Ismingiz" value="Foydalanuvchi">
    <input id="msg" placeholder="Xabar..." required autofocus>
    <button>Yuborish</button>
</form>

<script>
    const socket = io({transports: ['websocket', 'polling']});
    const name = localStorage.getItem("name") || "Foydalanuvchi";
    document.getElementById("name").value = name;

    socket.on("msg", d => {
        let div = document.createElement("div");
        div.className = "msg " + (d.name===name ? "mine" : "other");
        div.innerHTML = `<div class="name">${d.name}</div>${d.text}`;
        document.getElementById("messages").appendChild(div);
        window.scrollTo(0, document.body.scrollHeight);
    });

    function send() {
        let text = document.getElementById("msg").value.trim();
        let nameVal = document.getElementById("name").value.trim() || "Anonim";
        if (!text) return;
        localStorage.setItem("name", nameVal);
        socket.emit("msg", {name: nameVal, text: text});
        document.getElementById("msg").value = "";
    }
    document.getElementById("msg").addEventListener("keypress", e=>{if(e.key==="Enter")send()});
</script>
</body>
</html>"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("msg")
def handle(data):
    msg = {"name": data["name"][:20], "text": data["text"][:500]}
    messages.append(msg)
    if len(messages) > 500: messages.pop(0)
    emit("msg", msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)