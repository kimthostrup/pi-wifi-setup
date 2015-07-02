from flask import render_template, flash, redirect
from app import app
from forms import WifiForm
from os import system

@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    form = WifiForm()
    user = { "nickname" : "Reach" }

    if form.validate_on_submit():
        flash("New Wifi network data submitted: SSID == " + form.ssid.data + ", key == " + "*" * len(form.key.data) + ".")

        # we got the SSID and key validated, that means we have to add 
        # them to our boot script (/etc/rc.local) and to the wpa_supplicant file 
        with open("/etc/rc.local", "w") as f:
            data = f.readlines()

#        data[39] = data[39][:-1] +  

        cmd = ["wpa_passphrase", form.ssid.data, form.key.data, ">>", "/etc/wpa_supplicant/wpa_supplicant/conf"]
        print("Running " + cmd)
        # system(" ".join(cmd))
        return redirect("/")

    return render_template("index.html", title = "ReachSetup Home", user = user, form = form)
