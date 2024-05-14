import os
import gi
import sys
import time
import logging

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import OctopusWindow


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Helper functions
FILE_TYPE_MAP = {
    'text': ['.txt', '.text'],
    'picture': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    'audio': ['.mp3', '.wav', '.flac'],
    'video': ['.mp4', '.mov', '.avi'],
    'archive': ['.zip', '.tar', '.gz', '.rar'],
}

def get_file_type(filename):
    """Returns the type of the file based on its extension."""
    extension = os.path.splitext(filename)[1].lower()
    if not extension:
        return 'directory'
    for file_type, extensions in FILE_TYPE_MAP.items():
        if extension in extensions:
            return file_type
    return 'unknown'

def list_directory_files(directory, show_hidden=False):
    """Returns a list of files in the given directory with their types."""
    files = os.listdir(directory)
    if not show_hidden:
        files = [file for file in files if not file.startswith('.')]
    return [{'name': file, 'type': get_file_type(file)} for file in files]




class OctopusApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.octopus.octopus', flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        self.window = None
        self.home_path = os.path.expanduser("~")
        self.current_path = self.home_path

        self.last_click_time = 0
        self.selected_button = None

        self.create_actions()


    # Callbacks
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

    def on_home(self, widget, _):
        """Callback for the app.home action."""
        self.update_file_list()

    def on_documents(self, widget, _):
        """Callback for the app.documents action"""
        self.update_file_list(self.window.home_path + "/Documents")

    def on_downloads(self, widget, _):
        """Callback for the app.downloads action"""
        self.update_file_list(self.window.home_path + "/Downloads")

    def on_music(self, widget, _):
        """Callback for the app.music action"""
        self.update_file_list(self.window.home_path + "/Music")

    def on_pictures(self, widget, _):
        """Callback for the app.pictures action"""
        self.update_file_list(self.window.home_path + "/Pictures")

    def on_videos(self, widget, _):
        """Callback for the app.videos action"""
        self.update_file_list(self.window.home_path + "/Videos")

    def on_trash(self, widget, _):
        """Callback for the app.trash action."""
        self.update_file_list(os.path.expanduser("~/.local/share/Trash/files"))

    def on_back(self, widget, _):
        """Callback for the app.back action."""
        pass

    # TODO!.
    def on_forward(self, widget, _):
        """Callback for the app.forward action."""
        pass

    def on_search(self, widget, _):
        """Callback for the app.search action."""
        pass


    #
    def on_button_clicked(self, button, filename):
        current_time = time.time()
        if button == self.selected_button and current_time - self.last_click_time < 0.5:
            self.update_file_list(os.path.join(self.current_path, filename))
            self.selected_button = None
            self.last_click_time = 0
        else:
            if self.selected_button:
                self.selected_button.get_style_context().remove_class("selected")
            self.selected_button = button
            self.last_click_time = current_time

            button.get_style_context().add_class("selected")

    def update_file_list(self, directory=None):
        """Updates the file list in the UI for the given directory."""
        directory = directory or self.home_path
        files = list_directory_files(directory)

        if not files:
            status_page = Adw.StatusPage(title="Folder is empty", icon_name="folder-symbolic")
            if self.window.content.get_content() != status_page:
                self.window.content.set_content(status_page)
            logger.info(f"No files found in directory: {directory}")
            return

        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_top=5, margin_bottom=5, margin_start=10, margin_end=10, spacing=3)

        self.window.list_view_content.set_child(list_box)
        self.window.content.set_content()
        self.window.content.set_content(self.window.list_view)

        for file in files:
            button = Gtk.Button(
                child=Adw.ButtonContent(label=file['name'], halign=Gtk.Align.START, margin_start=5, icon_name=file['type']),
                has_frame=False
            )
            button.connect("clicked", self.on_button_clicked, file['name'])
            list_box.append(button)

        self.current_path = directory
        logger.info(f"Updated file list for directory: {directory}")


    #
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
            ('back', self.on_back, ['<primary>Left']),
            ('forward', self.on_forward, ['<primary>Right'])
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
        self.update_file_list()




def main(version):
    """The application's entry point."""
    app = OctopusApplication()
    return app.run(sys.argv)
