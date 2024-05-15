import os
import gi
import sys
import time
import logging
import subprocess

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

def open_file(filepath):
    """Open the file with the default application."""
    try:
        subprocess.run(['xdg-open', filepath], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error opening file {filepath}: {e}")

# Application class
class OctopusApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.octopus.octopus', flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.window = None
        self.home_path = os.path.expanduser("~")
        self.current_path = self.home_path
        self.search_active = False
        self.last_click_time = 0
        self.selected_button = None
        self.history = []
        self.history_index = -1
        self.create_actions()

    # Callbacks
    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(transient_for=self.window,
                                application_name='octopus',
                                application_icon='com.octopus.octopus',
                                developer_name='System Programming Project',
                                version='0.1.0',
                                developers=['Ravshan Zaripov', 'Bobir Ibragimov', 'Akbar Aminov'],
                                copyright='© 2024 Ravshan Zaripov')
        about.present()

    def on_search(self, widget, _):
        self.search_active = not self.search_active
        if self.search_active:
            self.window.search_button.set_icon_name("folder-open-symbolic")
            self.window.search_button.set_tooltip_text("Go to Files")
            self.window.content_topbar.set_title_widget(self.window.search_widget)
            self.window.content_topbar.remove(self.window.content_topbar_start)
            self.window.content.set_content(Adw.StatusPage(icon_name="system-search-symbolic", title="Search Everywhere", description="Find files and folders in all search locations."))
        else:
            self.window.search_button.set_icon_name("system-search-symbolic")
            self.window.search_button.set_tooltip_text("Search Everywhere")
            self.window.content_topbar.set_title_widget(self.window.content_topbar_title)
            self.window.content_topbar.pack_start(self.window.content_topbar_start)
            self.update_file_list(self.current_path)

    def on_navigate(self, widget, target_path):
        """Callback for navigation actions."""
        self.update_file_list(target_path)

    def on_back(self, widget, _):
        if self.history_index > 0:
            self.history_index -= 1
            self.update_file_list(self.history[self.history_index], add_to_history=False)

    def on_forward(self, widget, _):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.update_file_list(self.history[self.history_index], add_to_history=False)

    def on_button_clicked(self, button, filename):
        current_time = time.time()
        full_path = os.path.join(self.current_path, filename)
        if button == self.selected_button and current_time - self.last_click_time < 0.5:
            if os.path.isdir(full_path):
                self.update_file_list(full_path)
            else:
                open_file(full_path)
            self.selected_button = None
        else:
            if self.selected_button:
                self.selected_button.get_style_context().remove_class("selected")
            self.selected_button = button
            self.last_click_time = current_time
            button.get_style_context().add_class("selected")

    # Update UI
    def update_file_list(self, directory=None, add_to_history=True):
        """Updates the file list in the UI for the given directory."""
        directory = directory or self.home_path
        files = list_directory_files(directory)
        self.window.path_button.set_label(directory)

        if add_to_history:
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(directory)
            self.history_index += 1

        if not files:
            status_page = Adw.StatusPage(title="Folder is empty", icon_name="folder-symbolic")
            self.window.content.set_content(status_page)
            logger.info(f"No files found in directory: {directory}")
            self.current_path = directory
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

    # Create actions
    def create_actions(self):
        """Create application actions."""
        actions = [
            ('quit', lambda *_: self.quit(), ['<primary>q']),
            ('about', self.on_about_action, ['<primary>a']),
            ('search', self.on_search, ['<primary>s']),
            ('home', lambda widget, _: self.on_navigate(widget, self.home_path), None),
            ('documents', lambda widget, _: self.on_navigate(widget, os.path.join(self.home_path, "Documents")), None),
            ('downloads', lambda widget, _: self.on_navigate(widget, os.path.join(self.home_path, "Downloads")), None),
            ('music', lambda widget, _: self.on_navigate(widget, os.path.join(self.home_path, "Music")), None),
            ('pictures', lambda widget, _: self.on_navigate(widget, os.path.join(self.home_path, "Pictures")), None),
            ('videos', lambda widget, _: self.on_navigate(widget, os.path.join(self.home_path, "Videos")), None),
            ('trash', lambda widget, _: self.on_navigate(widget, os.path.expanduser("~/.local/share/Trash/files")), None),
            ('back', self.on_back, ['<primary>Left']),
            ('forward', self.on_forward, ['<primary>Right']),
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

