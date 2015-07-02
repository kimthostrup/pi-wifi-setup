from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    user = { "nickname" : "Reach" }
    return render_template("index.html", title = "ReachSetup Home", user = user)
