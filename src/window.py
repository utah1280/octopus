import os
from gi.repository import Adw, Gtk


@Gtk.Template(resource_path='/com/octopus/octopus/window.ui')
class OctopusWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OctopusWindow'

    home_path = os.path.expanduser("~")

    button_names = [
        "search_button",
        "home_button",
        "documents_button",
        "downloads_button",
        "music_button",
        "pictures_button",
        "videos_button",
        "trash_button",
        "go_back_button",
        "go_forward_button",
        "path_button"
    ]

    widget_names = [
        "content",
        "content_topbar",
        "content_topbar_start",
        "content_topbar_title",
        "list_view",
        "list_view_content",
        "search_widget",
        "search_widget_entry"
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
