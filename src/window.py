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

def classify_file_type(filename):
    extension = os.path.splitext(filename)[1].lower()
    if not extension:
        return 'directory'
    elif extension in ('.txt', '.text'):
        return 'text'
    elif extension in ('.jpg', '.jpeg', '.png', '.gif', '.svg'):
        return 'picture'
    elif extension in ('.mp3', '.wav', '.flac'):
        return 'audio'
    elif extension in ('.mp4', '.mov', '.avi'):
        return 'video'
    elif extension in ('.zip', '.tar', '.gz', '.rar'):
        return 'archive'
    else:
        return ''

def ls(directory, hidden=False):
    if directory is None:
        directory = "."

    files = os.listdir(directory)
    if not hidden:
        files = [file for file in files if not file.startswith('.')]

    files_with_types = []
    for file in files:
        files_with_types.append({'name': file, 'type': classify_file_type(file)})

    return files_with_types


@Gtk.Template(resource_path='/com/octopus/octopus/window.ui')
class OctopusWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OctopusWindow'

    # Helpers
    view_mode = "list"
    hidden = False
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
    content_ = Gtk.Template.Child()
    list_view = Gtk.Template.Child()
    list_view_content = Gtk.Template.Child()
    search_widget = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.documents_button.set_tooltip_text(self.home_path + "/Documents")
        self.downloads_button.set_tooltip_text(self.home_path + "/Documents")
        self.music_button.set_tooltip_text(self.home_path + "/Music")
        self.pictures_button.set_tooltip_text(self.home_path + "/Pictures")
        self.videos_button.set_tooltip_text(self.home_path + "/Videos")

        self.list_files()

    def list_files(self, directory=home_path):
        files = ls(directory)

        if len(files) == 0:
            status_page = Adw.StatusPage(title="Folder is empty", icon_name="folder-symbolic")

            if self.content_.get_content() != status_page:
                self.content_.set_content(status_page)
            return

        self.content_.set_content()

        list_box = Gtk.Box(orientation="vertical", margin_top=5, margin_bottom=5, margin_start=10, margin_end=10, spacing=3)
        self.list_view_content.set_child(list_box)
        self.content_.set_content(self.list_view)

        for file in files:
            button = Gtk.Button(child=Adw.ButtonContent(label=file['name'], halign=1, margin_start=5, icon_name=file['type']), has_frame=False)
            button.connect("clicked", lambda callback, file_name=file['name']: self.list_files(os.path.join(self.current_path, file_name)))
            list_box.append(button)
