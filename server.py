from flask import Flask
from threading import Thread

app = Flask('')


@app.route("/")
def hello():
    return "Discord Bot is up and running!"


def run():
    app.run(host="0.0.0.0", port=8080)


def stay_alive():
    t = Thread(target=run)
    t.start()
