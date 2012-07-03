# -*- coding: utf-8 -*-
"""
This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
import gi
gi.require_version('WebKit', '3.0')
from gi.repository import GObject, Gtk, Gdk, WebKit, LightDM
import os, sys
from time import sleep

class Greeter(object):

    window = None
    greeter = None
    view = None
    username = None
    password = None

    def __init__(self):
        self.greeter = LightDM.Greeter()
        # connect to greeter
        self.greeter.connect_sync()

        main_loop = GObject.MainLoop()

        # connect signal handlers to LightDM
        self.greeter.connect('show-prompt', self.show_prompt_cb)
        self.greeter.connect('show-message', self.show_message_cb)
        self.greeter.connect('authentication-complete', self.authentication_complete_cb)
        #self.greeter.connect('autologin-timer-expired', self.timed_login_cb)

        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        self.window = Gtk.Window()
        self.window.connect("destroy", Gtk.main_quit)
        self.window.app_paintable = True
        self.window.set_default_size(screen_width, screen_height)
        #self.window.set_size_request(400,300)
        #self.window.fullscreen()
        self.window.realize()

        self.view = WebKit.WebView()

        root_web_dir = "/usr/share/lightdm_pywebkit_greeter"
        #root_web_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../assets"

        f = open(root_web_dir + "/index.html", 'r')
        self.view.load_html_string(
            f.read(), "file://%s/" % root_web_dir)
        f.close()

        self.view.connect("navigation-requested", self.login_cb)

        self.window.add(self.view)
        self.window.show_all()
        main_loop.run()

    def login_cb(self, view, frame, req, data=None):
        """Callback to WebKit login action.

        This is slightly hackish, as the login credentials
        are being passed in the anchor hash url fragment.
        There are no clean, well-maintained solutions to bind
        native Python objects into JavaScript run-time, but
        this will do.
        """
        try:
            #self.log(req.get_uri())
            credentials = req.get_uri().split("#", 1)[1]
            if not credentials:
                # document.location.hash was cleared, no action
                return False
            (self.username, self.password) = credentials.split(":")
            self.log("Login request - user %s" % self.username)
            # give username to LightDM
            self.do_login()
            # give password to LightDM after a short timeout
            sleep(1)
            self.do_login()

        except Exception, e:
            print str(e)
            # fail without bothering LightDM
            self.fail(str(e))
        return False

    def do_login(self):
        """Login through LightDM after receiving credentials from WebKit UI.

        This Gtk signal is called when the user has entered both username
        and password. We have 3 possible cases to handle here.
        1) the user is already authenticated, if for example, they don't have
           a password set.
        2) The username has been passed into LightDM and now we need to pass
           the password
        3) The username has been entered, but not passed in.  We pass it in
           and start the authentication process.
        """
        try:
            if self.greeter.get_is_authenticated():
                self.log("user is already authenticated, starting session")
                start_session()
            elif self.greeter.get_in_authentication():
                self.log("username was passed in already, send password to LightDM")
                if not self.greeter.respond(self.password):
                    self.fail()
            else:
                self.log("Initial entry of username, send it to LightDM")
                if not self.greeter.authenticate(self.username):
                    self.fail()
        except Exception, e:
            self.log(e)

    def show_message(self, message):
        self.view.execute_script("ui.showMessage('%s');" % message)

    def fail(self, message="Authentication failed"):
        self.view.execute_script("ui.fail('%s');" % message)

    def reset(self):
        self.view.execute_script("ui.reset();")

    # The show_prompt callback is oddly named, but when you get this
    # callback you are supposed to send the password to LightDM next.
    def show_prompt_cb(self, greeter, text, promptType):
        self.log("show_prompt_cb")
        self.log("prompt type: %s" % promptType)
        # if this is a password orompt, we want to hide the characters
        if promptType == LightDM.PromptType.SECRET:
            pass
        else:
            pass

    def show_message_cb(self, greeter, text, type):
        """Show LightDM message in the greeter."""
        self.log("show_message_cb")
        self.show_message(text)

    def authentication_complete_cb(self, greeter):
        """LightDM has completed its duties.

        Successful login starts the session,
        failed login notifies the user.
        """
        self.log("authentication_complete_cb")
        if self.greeter.get_is_authenticated():
            session = self.read_configured_session()
            if self.greeter.start_session_sync(session):
                self.reset()
            else:
                self.fail("Failed to start session")
        else:
            self.fail("Authentication failed")

    # HACK
    def read_configured_session(self):
        try:
            f = open("/etc/lightdm/lightdm.conf", 'r')
            lightdm_conf = f.read()
            f.close()
            import re
            match = re.search(r'greeter-session=(.*)', lightdm_conf)
            return match.group(1)

        except Exception, e:
            self.log(e)
            return "gnome-session"

    def log(self, text):
        print >> sys.stderr, text


if __name__ == '__main__':
    Greeter()
    Gtk.main()
