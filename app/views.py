from flask import render_template, flash, redirect
from app import app
from forms import WifiForm
from os import system, popen

def scanAvailableNetworks():
    cmd = ["iwlist", "wlan0", "scan", "|", "grep", "ESSID"]
    cmd = " ".join(cmd)

    proc = popen(cmd)
    output = proc.read()
    print("### NETWORK SCAN OUTPUT ###")
    print(output)
    proc.close()

def addNewNetwork(ssid, key):

    # we got SSID and key validated, now we should add them
    # to our startup script

    with open("/etc/rc.local", "r") as f:
        data = f.readlines()

    # now we will be looking for the added network during startup
    data[39] = data[39][:-2] + "'" + str(form.ssid.data) + "' )\n"

    with open("/etc/rc.local", "w") as f:
        f.writelines(data)

    # we have the key, and so should the wpa_supplicant
    cmd = ["wpa_passphrase", str(form.ssid.data), str(form.key.data), ">>", "/etc/wpa_supplicant/wpa_supplicant.conf"]
    cmd = " ".join(cmd)
    system(cmd)

@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    form = WifiForm()

    form.ssid.choices = [(1, "LOL"), (2, "ROFL")]

    scanAvailableNetworks()

    if form.validate_on_submit():
        flash("New Wifi network data submitted: SSID == " + form.ssid.data + ", key == " + "*" * len(form.key.data) + ".")
        print("New Wifi network data submitted: SSID == " + str(form.ssid.data) + ", key == " + str(form.key.data) + ".")

        addNewNetwork(str(form.ssid.data), str(form.key.data))

        # to apply changes and try to connect to the new network we have to reboot
        cmd = "reboot"
        system(cmd)

        return redirect("/")

    return render_template("index.html", title = "ReachSetup Home", form = form)


