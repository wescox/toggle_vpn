#!/bin/bash

# Store profile name in a variable
profile="ServiceTrade"

# Store VPN session in a variable
session=($(nmcli con show --active | grep -oP "(?<=$profile ).*"))

# Check if there are any open sessions 
if [ -z $session ]; then
	#if no open sessions create one
	start=$(nmcli con up $profile | grep "successfully activated")
	if [ -z "$start" ]; then
		notify-send "ServiceTrade VPN" "Failed to connect"
	else
		ip=$(curl -s "https://icanhazip.com")
		notify-send "ServiceTrade VPN" "Connected with IP: $ip"
	fi
else
	#attempt to close open session
	stop=$(nmcli con down $profile | grep "successfully deactivated")
	if [ -z "$stop" ]; then
		notify-send "ServiceTrade VPN" "Failed to disconnect from session: $session"
	else
		ip=$(curl -s "https://icanhazip.com")
		notify-send "ServiceTrade VPN" "Disconnected with IP: $ip"
	fi
fi

