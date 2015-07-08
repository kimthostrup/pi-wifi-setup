from flask import render_template, flash, redirect
from app import app
from forms import WifiForm
from os import system, popen
from subprocess import check_output, Popen, PIPE

def scanAvailableNetworks():
    networks = []

    cmd = ["iwlist", "wlan0", "scan", "|", "grep", "ESSID"]
    # cmd = ["echo", "Hello!!!!"]
    cmd = " ".join(cmd)

    proc = Popen(cmd, stdout = PIPE, shell = True, bufsize = 2048)
    out = proc.communicate() 

    out = out[0].split("\n")

    # view results
    for val in out:
        if val:
            first = val.find('"')
            last = val.rfind('"')
            networks.append(val[first + 1:last])
        
    print("### NETWORK SCAN OUTPUT ###")
    print(out)
    print("\n### EXTRACTED NETWORKS ###")
    print(networks)

    return networks

def addNewNetwork(ssid, key):

    # we got SSID and key validated, now we should add them
    # to our startup script

    with open("/etc/rc.local", "r") as f:
        data = f.readlines()

    # now we will be looking for the added network during startup
    data[39] = data[39][:-2] + "'" + ssid + "' )\n"

    with open("/etc/rc.local", "w") as f:
        f.writelines(data)

    # we have the key, and so should the wpa_supplicant
    cmd = ["wpa_passphrase", ssid, key, ">>", "/etc/wpa_supplicant/wpa_supplicant.conf"]
    cmd = " ".join(cmd)
    system(cmd)

@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    form = WifiForm()

    choices = scanAvailableNetworks()
    choices = [(i + 1, j) for i, j in enumerate(choices)]

    form.ssid.choices = choices 

    if form.validate_on_submit():
        # get network name and key
        ssid = [item for item in choices if item[0] == form.ssid.data]
        ssid = str(ssid[0][1])
        key = str(form.key.data)
        
        flash("New Wifi network data submitted: SSID == " + ssid + ", key == " + "*" * len(key) + ".")
        print("New Wifi network data submitted: SSID == " + ssid + ", key == " + key + ".")

        addNewNetwork(str(ssid), str(key))

        # to apply changes and try to connect to the new network we have to reboot
        cmd = "reboot"
        system(cmd)

        return redirect("/")

    return render_template("index.html", title = "ReachSetup Home", form = form)


