import os
import logging
from gi.repository import Adw, Gtk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_TYPE_MAP = {
    'text': ['.txt', '.text'],
    'picture': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    'audio': ['.mp3', '.wav', '.flac'],
    'video': ['.mp4', '.mov', '.avi'],
    'archive': ['.zip', '.tar', '.gz', '.rar'],
}

def get_home_directory():
    """Returns the home directory of the current user."""
    return os.path.expanduser("~")

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


@Gtk.Template(resource_path='/com/octopus/octopus/window.ui')
class OctopusWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OctopusWindow'

    home_path = get_home_directory()
    current_path = home_path

    button_names = [
        "search_button",
        "home_button",
        "documents_button",
        "downloads_button",
        "music_button",
        "pictures_button",
        "videos_button",
        "trash_button"
    ]

    widget_names = [
        "content",
        "list_view",
        "list_view_content",
        "search_widget"
    ]

    for name in button_names + widget_names:
        locals()[name] = Gtk.Template.Child()

    def __init__(self, **kwargs):
        """Initializes the OctopusWindow."""
        super().__init__(**kwargs)

        # Set tooltips for specific buttons
        tooltip_paths = {
            self.documents_button: "/Documents",
            self.downloads_button: "/Downloads",
            self.music_button: "/Music",
            self.pictures_button: "/Pictures",
            self.videos_button: "/Videos"
        }

        for button, path in tooltip_paths.items():
            button.set_tooltip_text(f"{self.home_path}{path}")

        self.update_file_list(self.home_path)

    def update_file_list(self, directory=None):
        """Updates the file list in the UI for the given directory."""
        directory = directory or self.home_path
        files = list_directory_files(directory)

        if not files:
            status_page = Adw.StatusPage(title="Folder is empty", icon_name="folder-symbolic")
            if self.content.get_content() != status_page:
                self.content.set_content(status_page)
            logger.info(f"No files found in directory: {directory}")
            return

        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_top=5, margin_bottom=5, margin_start=10, margin_end=10, spacing=3)

        self.list_view_content.set_child(list_box)
        self.content.set_content()
        self.content.set_content(self.list_view)

        for file in files:
            button = Gtk.Button(
                child=Adw.ButtonContent(label=file['name'], halign=Gtk.Align.START, margin_start=5, icon_name=file['type']),
                has_frame=False
            )
            button.connect("clicked", lambda btn, fname=file['name']: self.update_file_list(os.path.join(directory, fname)))
            list_box.append(button)

        self.current_path = directory
        logger.info(f"Updated file list for directory: {directory}")
