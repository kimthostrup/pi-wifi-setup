#!/bin/bash -e

# Handle boot network sequence

createAdHocNetwork(){
    echo "Creating ad-hoc network"
    # get the last symbols of this boards' mac address
    mac_address=$(ifconfig -a | grep wlan0)
    mac_address='ReachNetwork'${mac_address: -7}
    ifconfig wlan0 down
    ifconfig wlan0 up
    iwconfig wlan0 mode ad-hoc
    iwconfig wlan0 key aaaaa11111 #WEP key
    iwconfig wlan0 essid $mac_address #SSID
    ifconfig wlan0 10.0.0.200 netmask 255.255.255.0 up
    /usr/sbin/dhcpd wlan0
    echo "Ad-hoc network created"
}

date --set 2015-07-29

echo "================================="
echo "====Reach Network Setup v0.0====="
echo "================================="
echo "Scanning for known WiFi networks"
ssids=( 'Igor' '456' 'Phone' 'EML33T5' )
connected=false
ifconfig wlan0 up
for ssid in "${ssids[@]}"
do
    echo "Scanning for:" $ssid
    if iwlist wlan0 scan | grep $ssid > /dev/null
    then
        echo "First WiFi in range has SSID:" $ssid
        echo "Starting supplicant for WPA/WPA2"
        wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null 2>&1
        echo "Obtaining IP from DHCP"
        if dhclient -1 wlan0
        then
            echo "Connected to WiFi"
            connected=true
            # /home/reach/ReachView/server.py &
            break
        else
            echo "DHCP server did not respond with an IP lease (DHCPOFFER)"
            echo "There was some trouble connecting to" $ssid
            echo "Please check if the key is correct"
            wpa_cli terminate
            ifconfig wlan0 down
            ifconfig wlan0 up
        fi
    else
        echo "Not in range, WiFi with SSID:" $ssid
    fi
done

if ! $connected; then
    createAdHocNetwork
    # start a web interface to add new ssid
    /home/reach/ReachSetup/run.py &
fi

exit 0
