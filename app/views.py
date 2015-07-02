from flask import render_template
from app import app
from forms import WifiForm

@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    form = WifiForm()
    user = { "nickname" : "Reach" }
    return render_template("index.html", title = "ReachSetup Home", user = user, form = form)
