# window.py
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

import os
import subprocess

from gi.repository import Adw
from gi.repository import Gtk


def get_home_directory():
    return os.path.expanduser("~")

def ls(path_):
    if path_ is None:
        path_ = "."

    result = subprocess.run(["ls", path_], stdout=subprocess.PIPE, text=True)

    if result.returncode == 0:
        filenames = result.stdout.split('\n')

        filenames = [filename for filename in filenames if filename]

        filenames.sort()

        return filenames
    else:
        print("Error executing ls command.")
        return []

def create_list_view_box():
    list_view_box = Gtk.Box()

    list_view_box.set_margin_top(10)
    list_view_box.set_margin_bottom(10)
    list_view_box.set_margin_start(10)
    list_view_box.set_margin_end(10)
    list_view_box.set_spacing(5)
    list_view_box.set_orientation(Gtk.Orientation.VERTICAL)

    return list_view_box

def modify_status_page(widget_, title_, icon_, description_=None):
    widget_.set_title("")
    widget_.set_icon_name(None)
    widget_.set_description(None)

    widget_.set_title(title_)
    widget_.set_icon_name(icon_)
    widget_.set_description(description_)

@Gtk.Template(resource_path='/com/octopus/octopus/window.ui')
class OctopusWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OctopusWindow'

    # Helpers
    view_mode = "list"
    search_active = False
    home_path = get_home_directory()
    current_path = home_path

    # Buttons
    search_button = Gtk.Template.Child()
    home_button = Gtk.Template.Child()
    documents_button = Gtk.Template.Child()
    downloads_button = Gtk.Template.Child()
    music_button = Gtk.Template.Child()
    pictures_button = Gtk.Template.Child()
    videos_button = Gtk.Template.Child()
    trash_button = Gtk.Template.Child()

    # Widgets
    header_bar = Gtk.Template.Child()
    status_page = Gtk.Template.Child()
    search_widget = Gtk.Template.Child()
    toolbar_view = Gtk.Template.Child()
    scrolled_window = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.documents_button.set_tooltip_text(self.home_path + "/Documents")
        self.downloads_button.set_tooltip_text(self.home_path + "/Documents")
        self.music_button.set_tooltip_text(self.home_path + "/Music")
        self.pictures_button.set_tooltip_text(self.home_path + "/Pictures")
        self.videos_button.set_tooltip_text(self.home_path + "/Videos")

        self.list_()

    def open_search(self):
        self.search_button.set_icon_name('folder-drag-accept-symbolic')
        self.search_button.set_tooltip_text('Files')

        self.header_bar.set_show_title(True)
        self.header_bar.set_title_widget(self.search_widget)

        modify_status_page(self.status_page, title_="Search Everywhere", icon_="folder-saved-search-symbolic", description_="Find files and folders in all search locations")

        self.scrolled_window.set_child(self.status_page)

        self.search_active = True

    def close_search(self):
        self.search_button.set_icon_name('system-search-symbolic')
        self.search_button.set_tooltip_text('Search Everywhere')

        self.header_bar.set_show_title(False)
        self.header_bar.set_title_widget(None)

        self.search_active = False

        self.list_()

    def status_page_on_search(self):
        if self.search_active:
            self.close_search()
        else:
            self.open_search()

    def list_(self, path_=None):
        if self.search_active:
            self.close_search()

        files = ls(path_)

        # If the folder is empty insert corresponding status page widget
        if len(files) == 0:
            modify_status_page(self.status_page, title_="Folder is empty", icon_="folder-symbolic")

            if self.scrolled_window.get_child() != self.status_page:
                self.scrolled_window.set_child(self.status_page)

            return

        list_view_box = create_list_view_box()

        for file in files:
            button = Gtk.Button(child=Adw.ButtonContent(label=file, halign=1, margin_start=10))
            list_view_box.append(button)

        self.scrolled_window.set_child(list_view_box)
