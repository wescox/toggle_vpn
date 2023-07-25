#!/bin/bash

# Store config file name in a variable
profile="/home/wally/ServiceTrade/code/toggle_vpn"
config=$(echo "$profile/$(ls $profile | grep ".ovpn")") # this is so I don't have to care about the file name

# Store VPN sessions in an array 
sessions=($(openvpn3 sessions-list | grep -oP "(?<=Path: ).*"))

# Check if there are any open sessions 
if [ ${#sessions[@]} -eq 0 ]; then
	#if no open sessions create one
	start=$(openvpn3 session-start --config $config | grep "Connected")
	if [ -z $start ]; then
		notify-send "ServiceTrade VPN" "Failed to connect"
	else
		ip=$(curl -s "https://icanhazip.com")
		notify-send "ServiceTrade VPN" "Connected with IP: $ip"
	fi
else
	#if open sessions attempt to close each and store any errors
	errors=""
	for session in ${sessions[@]}; do
		stop=$(openvpn3 session-manage --session-path $session --disconnect | grep "Initiated session shutdown")
		if [ -z "$stop" ]; then
			errors+="$session\n"
		fi
	done
	
	#if no errors get new IP to confirm everything worked
	if [ -n "$errors" ]; then
		notify-send "ServiceTrade VPN" "Failed to disconnect from sessions:\n$errors\nStop OpenVPN in the terminal with: sudo pkill -9 openvpn3"
	else
		ip=$(curl -s "https://icanhazip.com")
		notify-send "ServiceTrade VPN" "Disconnected with IP: $ip"
	fi
fi

