# ToggleVPN
A Linux Applet to quickly toggle OpenVPN on and off using your desktop environment app launcher

## Screenshots

[Launcher]()
[Notification]()

## Installation

There are scripts included which support either [OpenVPN 3](https://community.openvpn.net/openvpn/wiki/OpenVPN3Linux) or [Network Manager](https://wiki.archlinux.org/title/NetworkManager).  Visit the links for more information and installation instructions.  The ServiceTrade VPN profile is not compatible with the kernel implementation of OpenVPN or Network Manager as is.  You must edit the profile and remove the lines that start with "route".  Or you can use OpenVPN 3. 

Clone the repo.

If you using Network Manager, the script assumes a profile has been imported with the name of 'ServiceTrade'.  You can use the GUI applet or nmcli with the commands below.  If you use a different name the script will need to be updated.

```bash
mv /path/to/profile.ovpn /path/to/ServiceTrade.ovpn
nmcli connection import type openvpn file /path/to/ServiceTrade.ovpn
```
The above is not necessary for OpenVPN 3.  Just edit file path in the script to point to your VPN profile location.

Make appropriate shell script executable
```bash
chmod u+x /path/to/toggle-vpn.sh
```

Symlink, move or copy the shell script.  I prefer symlinks.
```bash
ln -sf /path/to/toggle-vpn.sh $HOME/bin
```
You will need to make $HOME/bin if it does not exist and make sure $HOME/bin is in your PATH.  Bash does this by default (IIRC) whereas you will need to add to your ZSH config.  IIRC, it's already there but commented out.  You can really put this anywhere you want but this is the "Linuxy" location and you'll need to update the desktop file if you choose a different location.

Symlink, move, or copy the appropriate desktop file and icon.  I prefer symlinks.
```bash
ln -sf /path/to/toggle-vpn.desktop $HOME/.local/share/applications
ln -sf /path/to/openvpn.png $HOME/.local/share/icons
```

Finally, update your MIME type database
```bash
update-desktop-database $HOME/.local/share/applications
```
This doesn't work sometimes and you'll need to log out and back in to see changes take effect. 
