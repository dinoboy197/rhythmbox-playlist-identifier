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
from gi.repository import GObject, Gtk

ui_str = """
<ui>
  <popup name="BrowserSourceViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="ShowPlaylistsForTrackPopup" action="ShowPlaylistsForTrack"/>
    </placeholder>
  </popup>

  <popup name="PlaylistViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="ShowPlaylistsForTrackPopup" action="ShowPlaylistsForTrack"/>
    </placeholder>
  </popup>

  <popup name="QueuePlaylistViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="ShowPlaylistsForTrackPopup" action="ShowPlaylistsForTrack"/>
    </placeholder>
  </popup>

  <popup name="PodcastViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="ShowPlaylistsForTrackPopup" action="ShowPlaylistsForTrack"/>
    </placeholder>
  </popup>
</ui>
"""


class PlaylistIdentifierPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(PlaylistIdentifierPlugin, self).__init__()
        GObject.Object.__init__(self)

    def do_activate(self):
        data = dict()
        shell = self.object
        manager = shell.props.ui_manager

        data['action_group'] = Gtk.ActionGroup(name='ShowPlaylistsForTrackActions')

        action = Gtk.Action(name='ShowPlaylistsForTrack', label=_("_Show Playlists For Track"),
                            tooltip=_("Show the containing playlists for the selected track"),
                            stock_id='gnome-mime-text-x-python')
        action.connect('activate', self._show_playlists_for_track, shell)
        data['action_group'].add_action(action)

        manager.insert_action_group(data['action_group'], 0)
        data['ui_id'] = manager.add_ui_from_string(ui_str)
        manager.ensure_update()

        shell.set_data('ShowPlaylistsForTrackInfo', data)

    def do_deactivate(self):
        shell = self.object
        data = shell.get_data('ShowPlaylistsForTrackInfo')

        manager = shell.props.ui_manager
        manager.remove_ui(data['ui_id'])
        manager.remove_action_group(data['action_group'])
        manager.ensure_update()

        shell.set_data('ShowPlaylistsForTrackInfo', None)
        
    def _show_playlists_for_track(self, action, shell):
        playlists = self._get_playlists_for_selected_track(shell)

        dialog = Gtk.Dialog("Playlists", None, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.YES,
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
                           
        # add labels for all playlists
        for playlist in playlists:
            playlist_label = Gtk.Label(playlist)
            dialog.vbox.pack_start(playlist_label, True, True, 0)
            playlist_label.show()
        
        # build and show dialog
        box1 = Gtk.HBox(False, 0)
        dialog.vbox.pack_start(box1, True, True, 0)
        box1.show()
        response = dialog.run()
        
        # cleanup
        dialog.destroy()
        while Gtk.events_pending():
            Gtk.main_iteration()
            
    def _get_playlists_for_selected_track(self, shell):
        page = shell.props.selected_page
        if not hasattr(page, "get_entry_view"):
            return
        selected = page.get_entry_view().get_selected_entries()
        if selected != []:
            uri = selected[0].get_playback_uri()
            return self._get_playlists_for_uri(shell, uri)
            
    def _get_playlists_for_uri(self, shell, uri):
        playlist_model_entries = shell.props.playlist_manager.get_playlists()
        if playlist_model_entries:
            playlists = []
            for playlist in playlist_model_entries:
                playlist_rows = playlist.get_query_model()
                for row in playlist_rows:
                    if row[0].get_string(RB.RhythmDBPropType.LOCATION) == uri:
                        playlists.append(playlist.props.name)
                        break
            return playlists
        else:
            return []
