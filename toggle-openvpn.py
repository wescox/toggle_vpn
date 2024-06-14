#!/usr/bin/python

import os, gi, requests, time, signal, subprocess, re, shlex
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify as notify, GLib as glib
from pydbus import SystemBus as systembus, SessionBus as sessionbus


APPINDICATOR_ID = "openvpn3tray"

class Tray:
    def __init__(self):
        # initiate tray app
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, 'network-vpn-acquiring', appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.status = 'acquiring'
        self.menu()
    
        # initiate notification
        #notify.init(APPINDICATOR_ID)
    
        # connect or disconnect from VPN
        #self.vpn()
    
        # initiate 15 minute IP check loop
        glib.timeout_add_seconds(900, self.vpn) # 900 seconds = 15 minutes
    
        # initiate GTK event loop
        # gtk.main()
    
    def menu(self):
        menu = gtk.Menu()

        vpn_connect = gtk.MenuItem()
        if self.status == 'connected':
            vpn_connect.set_label("Connect to VPN")
            vpn_connect.connect('activate', self.vpn)
        elif self.status == 'disconnected':
            vpn_connect.set_label("Connect to VPN")
            vpn_connect.connect('activate', self.vpn)
        menu.append(vpn_connect)

        vpn_exit = gtk.MenuItem(label='Quit')
        vpn_exit.connect('activate', self.quit)
        menu.append(vpn_exit)

        menu.show_all()
        self.indicator.set_menu(menu)
    
        return menu
    
    def ipcheck(self):
        vpn_ip = '52.6.171.48'
        #local_ip = subprocess.getoutput("curl -s icanhazip.com")
        res = requests.get("https://icanhazip.com")
        local_ip = res.text
        if local_ip == vpn_ip:
            self.indicator.set_icon_full("network-vpn", "VPN Connected")
            self.status = 'connected'
        else:
            self.indicator.set_icon_full("network-offline", "VPN Disconnected")
            self.status = 'disconnected'
    
        #return True if local_ip == vpn_ip else False
        #return True
    
        # show notification for 3 seconds
        #notification = notify.Notification.new('Test', 'Test2')
        #notification.show()
        #time.sleep(3)
        #notification.close()
    
    def notify(self, title, message):
        subprocess.Popen(["notify-send", title, message]) 
        # show notification for 5 seconds
        #notification = notify.Notification.new(title, body)
        #notification.show()
        #time.sleep(5)
        #notification.close()
    
      
    #def shell(cmd):
    #    return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE).stdout.decode("utf-8")
    
    def connect_vpn(self):
    
        ## get list of open sessions
        #sessions = re.findall("(?<=Path: ).*", shell("openvpn3 sessions-list"))
        #
        ## close any open sessions or open a new one 
        #errors = ""
        #if sessions and not connected:
        #    for session in sessions:
        #        cmd = f"openvpn3 session-manage --session-path {session} --disconnect"
        #        stop = re.search("Initiated session shutdown", subprocess.getoutput(cmd))
        #        if stop:
        #            msg("ServiceTrade VPN", "Disconnected")
        #        else:
        #            errors += f"{session}\n"
        #else:
            cwd = os.getcwd()
            # so i don't need to care about profile name as long as there's just one in cwd
            profile = [profile for profile in os.listdir(cwd) if profile.endswith('.ovpn')][0]
            #start = re.search("Client connected", shell(cmd))
            start = subprocess.getoutput(f"openvpn3 session-start --config {profile}")
            if "Client connected" not in start:
                self.notify("ServiceTrade VPN", "Failed to connect")
                self.indicator.set_icon_full("openvpn", "VPN disconnected")
                self.notify("ServiceTrade VPN", "Failed to connect")
        
        # must return true to keep 15 minute cycle going 
        return True
    
    
    
    def quit(self,_):
        # add vpn disconnect
        #notify.uninit()
        gtk.main_quit()
    
    #def __del__():
    #    # Remove the lock file when the program exits
    #    os.close(lock_fd)
    #    os.unlink(lock_file)
    
if __name__ == "__main__":
    
    # simply so that CTRL+C works if running from CLI
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = Tray()
    gtk.main()
