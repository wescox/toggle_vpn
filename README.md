# ToggleVPN
A Linux tray applet to quickly manage OpenVPN3 connections.  It can be launched using your DE's application launcher. The app icon changes based on connection state so that you have a visual indication of current status.  The app also checks whether you're still connected every 10 minutes and will automatically close all sessions if not.    

![Launcher](https://github.com/wescox/toggle_vpn/blob/master/screenshots/launcher.png)

## Installation

### Prequisites
 - If you are using GNOME you must have some sort of [extension](https://extensions.gnome.org/) installed to support tray apps.  I use [AppIndicator/KStatusNotifierItem Support](https://github.com/ubuntu/gnome-shell-extension-appindicator).  Visit links for more information and installation instructions. 
 - Install [OpenVPN 3](https://community.openvpn.net/openvpn/wiki/OpenVPN3Linux). Visit the link for more information and installation instructions.
 - Install [GTK](https://www.gtk.org/) libraries.  There's a good chance you already have these since many Linux apps rely on them.  You definitely do if you use GNOME DE. Visit link for more information
 - Install Python 3, pip, and the below packages:
    - [PyGObject](https://pypi.org/project/PyGObject/):
        pip:
        ```
        pip install PyGObject
        ```
        Fedora:
        ```
        sudo dnf install python3-gobject
        ```
        Ubuntu/Debian variants:
        ```
        sudo apt install python3-gi
        ```
    - [requests](https://pypi.org/project/requests/):
        ```
        pip install requests
        ```

### Steps
Clone the repo.

Either move your VPN profile to the repo or edit the file path in the script to point to your VPN profile location.

Make the script executable
```bash
chmod u+x /path/to/toggle-openvpn.py
```

Symlink, move or copy the script.  I prefer symlinks.
```bash
ln -sf /path/to/toggle-openvpn.py $HOME/.local/bin
```
You will need to make $HOME/.local/bin if it does not exist and make sure it is in your PATH.  You could also use /usr/local/bin if you want the app to be available for all users.

Symlink, move, or copy the appropriate desktop file and icon.  I prefer symlinks.
```bash
ln -sf /path/to/toggle-vpn.desktop $HOME/.local/share/applications
ln -sf /path/to/openvpn.png $HOME/.local/share/icons
```
Again, you could use the /usr/local versions of the above as well.

Finally, update your MIME type database
```bash
update-desktop-database $HOME/.local/share/applications
```
This doesn't work sometimes and you'll need to log out and back in to see changes take effect. I also have no idea if this command works in any DE other than GNOME.

## Issues

- The icons don't update quite as reliably as I'd like.  The GTK loop is asynchronous and I don't care enough to figure out how to manage that in Python.  
- It won't automatically start at boot.  I think this is more of a GNOME or me problem.  YMMV.  It could always be setup as a systemd service rather than being launched as an application.
