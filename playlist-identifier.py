"""
  playlist-identifier plugin for rhythmbox application.
  Copyright (C) 2012  Taylor Raack <taylor@raack.info>
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from gi.repository import RB, Peas
from gi.repository import GObject


class PlaylistIdentifierPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(PlaylistIdentifierPlugin, self).__init__()

    def do_activate(self):
        print "Hello World"
        
    def do_deactivate(self):
        del self.string
