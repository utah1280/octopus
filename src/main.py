import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import OctopusWindow


class OctopusApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.octopus.octopus', flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        self.window = None
        self.create_actions()

    def create_actions(self):
        """Create application actions."""
        actions = [
            ('quit', lambda *_: self.quit(), ['<primary>q']),
            ('about', self.on_about_action, ['<primary>a']),
            ('search', self.on_search, ['<primary>s']),
            ('home', self.on_home, None),
            ('documents', self.on_documents, None),
            ('downloads', self.on_downloads, None),
            ('music', self.on_music, None),
            ('pictures', self.on_pictures, None),
            ('videos', self.on_videos, None),
            ('trash', self.on_trash, None),
        ]
        for name, callback, shortcuts in actions:
            self.create_action(name, callback, shortcuts)

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action."""
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def do_activate(self):
        """Called when the application is activated."""
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

    def on_search(self, widget, _):
        """Callback for the app.search action."""
        pass

    def on_home(self, widget, _):
        """Callback for the app.home action."""
        self.window.update_file_list(self.window.home_path)

    def on_documents(self, widget, _):
        """Callback for the app.documents action"""
        self.window.update_file_list(self.window.home_path + "/Documents")

    def on_downloads(self, widget, _):
        """Callback for the app.downloads action"""
        self.window.update_file_list(self.window.home_path + "/Downloads")

    def on_music(self, widget, _):
        """Callback for the app.music action"""
        self.window.update_file_list(self.window.home_path + "/Music")

    def on_pictures(self, widget, _):
        """Callback for the app.pictures action"""
        self.window.update_file_list(self.window.home_path + "/Pictures")

    def on_videos(self, widget, _):
        """Callback for the app.videos action"""
        self.window.update_file_list(self.window.home_path + "/Videos")

    def on_trash(self, widget, _):
        """Callback for the app.trash action."""
        self.window.update_file_list(".local/share/Trash/files")

def main(version):
    """The application's entry point."""
    app = OctopusApplication()
    return app.run(sys.argv)
