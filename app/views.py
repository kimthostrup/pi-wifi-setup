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
        print("New Wifi network data submitted: SSID == " + str(form.ssid.data) + ", key == " + str(form.key.data) + ".")

        # we got the SSID and key validated, that means we have to add 
        # them to our boot script (/etc/rc.local) and to the wpa_supplicant file 
        with open("/etc/rc.local", "r") as f:
            data = f.readlines()

        print(str(data[39]))

        data[39] = data[39][:-2] + "'" + str(form.ssid.data) + "' )\n"

        print("Hello! this is the new /etc/rc.local file")
        print(str(data[39]))

        with open("/etc/rc.local", "w") as f:
             f.writelines(data)

        cmd = ["wpa_passphrase", str(form.ssid.data), str(form.key.data), ">>", "/etc/wpa_supplicant/wpa_supplicant.conf"]
        cmd = " ".join(cmd)
        print("Running " + cmd)
        system(cmd)

        return redirect("/")

    return render_template("index.html", title = "ReachSetup Home", user = user, form = form)
