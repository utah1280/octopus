# main.py
#
# Copyright 2024 Ravshan Zaripov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import OctopusWindow


class OctopusApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.octopus.octopus',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action, ['<primary>a'])
        self.create_action('search', self.on_search, ['<primary>s'])
        self.create_action('home', self.on_home)
        self.create_action('documents', self.on_documents)
        self.create_action('downloads', self.on_downloads)
        self.create_action('music', self.on_music)
        self.create_action('pictures', self.on_pictures)
        self.create_action('videos', self.on_videos)
        self.create_action('trash', self.on_trash)

        self.window = None

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        if not self.window:
            self.window = OctopusWindow(application=self)
        self.window.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.window,
                                application_name='octopus',
                                application_icon='com.octopus.octopus',
                                developer_name='System Programming Project',
                                version='0.1.0',
                                developers=['Ravshan Zaripov', 'Bobir Ibragimov', 'Akbar Aminov'],
                                copyright='© 2024 Ravshan Zaripov')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def on_search(self, widget, _):
        if self.window:
            self.window.status_page_on_search()

    def on_home(self, widget, _):
        pass

    def on_documents(self, widget, _):
        pass

    def on_downloads(self, widget, _):
        pass

    def on_music(self, widget, _):
        pass

    def on_pictures(self, widget, _):
        pass

    def on_videos(self, widget, _):
        pass

    def on_trash(self, widget, _):
        pass

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = OctopusApplication()
    return app.run(sys.argv)
