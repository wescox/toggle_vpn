#!/bin/python

import os, gi, requests, time, signal, subprocess, re, fcntl, sys
gi.require_version("Gtk", "3.0")
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator
except ValueError:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk, Notify as notify, GLib as glib


class Tray:
    def __init__(self):
        # initiate tray app
        self.indicator = appindicator.Indicator.new("openvpntray", "network-vpn-acquiring", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # get initial state
        self.set_state()

        # create menu based on state
        self.menu()
    
        # initiate 15 minute IP check loop
        glib.timeout_add_seconds(600, self.disconnect_check) # 600 seconds = 10 minutes
    

    def menu(self):
        menu = gtk.Menu()

        vpn_connect = gtk.MenuItem()
        if self.status == 'connected':
            vpn_connect.set_label("Disconnect VPN")
            vpn_connect.connect('activate', self.disconnect_vpn)
        elif self.status == 'disconnected':
            vpn_connect.set_label("Connect to VPN")
            vpn_connect.connect('activate',self.connect_vpn)
        menu.append(vpn_connect)
        
        if self.status == 'connected':
            validate = gtk.MenuItem(label='Validate connection')
            validate.connect('activate', self.validate)
            menu.append(validate)

        # add separator
        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        # add quit
        vpn_exit = gtk.MenuItem(label='Quit')
        vpn_exit.connect('activate', self.quit)
        menu.append(vpn_exit)

        menu.show_all()
        self.indicator.set_menu(menu)
    
        return menu
    

    def set_state(self):
        self.ip_check()
        if self.connected:
            self.indicator.set_icon_full("network-vpn", "ServiceTrade VPN")
            self.status = 'connected'
        else:
            self.indicator.set_icon_full("openvpn", "ServiceTrade VPN")
            self.status = 'disconnected'


    def ip_check(self):
        vpn_ip = '52.6.171.48'
        res = requests.get("https://icanhazip.com")
        local_ip = res.text.rstrip()
        if local_ip == vpn_ip:
            self.connected = True
        else:
            self.connected = False


    def notify(self, message):
        subprocess.Popen(["notify-send", "ServiceTrade VPN", message]) 
    

    def validate(self, _):
        self.ip_check()
        if self.connected:
            self.notify("VPN connection still active")
        else:
            self._disconnect_vpn()


    def disconnect_check(self):
        self.ip_check()
        
        # status changed to disconnected without input
        if not self.connected and self.status == 'connected':
            self._disconnect_vpn()

        return True # must return True to keep loop going


    
    # this non sensical setup is simply to get the icons to update correctly
    def connect_vpn(self,_):
        self.indicator.set_icon_full("network-vpn-acquiring", "ServiceTrade VPN")
        glib.timeout_add(100, self._connect_vpn)


    def _connect_vpn(self):

        cwd = os.path.dirname(os.path.realpath(__file__))
        # so i don't need to care about profile name as long as there's just one in cwd
        profile = [profile for profile in os.listdir(cwd) if profile.endswith('.ovpn')][0]

        # TODO: do this twice in case the first one fails
        subprocess.run(["openvpn3", "session-start", "--config", f"{cwd}/{profile}"])

        idx = 10
        time.sleep(2)
        while idx > 0:
            time.sleep(1)
            self.ip_check()
            if self.connected:
                break
            idx -= 1

        self.set_state()
        self.menu()

        if not self.connected:
            self.notify("Failed to connect")

    # this non sensical setup is simply to get the icons to update correctly
    def disconnect_vpn(self,_):
        self.indicator.set_icon_full("network-vpn-acquiring", "ServiceTrade VPN")
        glib.timeout_add(100, self._disconnect_vpn)


    def _disconnect_vpn(self):

        # get list of open sessions
        sessions_list = subprocess.getoutput("openvpn3 sessions-list")
        sessions = re.findall("(?<=Path: ).*", sessions_list)
        
        # close any open sessions or open a new one 
        errors = ""
        if sessions:
            for session in sessions:
                cmd = f"openvpn3 session-manage --session-path {session} --disconnect"
                disconnect_session = re.search("Initiated session shutdown", subprocess.getoutput(cmd))
                if not disconnect_session:
                    errors += f"{session}\n"

        self.set_state()
        self.menu()

        if self.connected: 
            self.notify("Failed to disconnect")
        elif not self.connected and len(errors):
            self.notify("Disconnected but failed to close all sessions")


    def quit(self,_):
        self._disconnect_vpn()
        gtk.main_quit()
        if os.path.exists(self.lockfile):
            os.remove(self.lockfile)
    

if __name__ == "__main__":
    
    lockfile = '/tmp/toggle-openvpn.lock'
    try:

        # create lockfile
        with open(lockfile, 'w') as lf:
            fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lf.write(str(os.getpid()))
            lf.flush()

            # simply so that CTRL+C works if running from CLI
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            app = Tray()
            app.lockfile = lockfile
            gtk.main()

    except IOError:
        print('App is already running')
        sys.exit(1)
        
