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

from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/octopus/octopus/window.ui')
class OctopusWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OctopusWindow'

    # Helpers
    search_active = False

    # Buttons
    search_button = Gtk.Template.Child()

    # Widgets
    header_bar = Gtk.Template.Child()
    status_page = Gtk.Template.Child()
    search_widget = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def status_page_on_search(self):
        if self.search_active:
            self.status_page.set_title('Empty folder')
            self.status_page.set_description(None)
            self.status_page.set_icon_name('folder-symbolic')

            self.search_button.set_icon_name('system-search-symbolic')

            self.header_bar.set_show_title(False)
            self.header_bar.set_title_widget(None)

            self.search_active = False
        else:
            self.status_page.set_title('Search Everywhere')
            self.status_page.set_description('Find files and folders in all search locations')
            self.status_page.set_icon_name('folder-saved-search-symbolic')

            self.search_button.set_has_frame(True)
            self.search_button.set_icon_name('folder-drag-accept-symbolic')

            self.header_bar.set_show_title(True)
            self.header_bar.set_title_widget(self.search_widget)

            self.search_active = True
