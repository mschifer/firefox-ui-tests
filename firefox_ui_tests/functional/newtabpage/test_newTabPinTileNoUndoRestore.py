# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
###########################################################
# Test opening a new tab in current window.
# Create a new Tab By:
#   Menu
#   Shortcut
#   newTabButton
#   tabStrip
# Verify
#   Tab Index incrased by 1
#   New Tab index is Selected
#   Original Tab Index is Not Selected
#   Tab has title New Tab
#   Tab URL matches perf.

from os import sys, path
import time
import platform
import urllib2
import random
from urlparse import urlparse
import pprint
#import unicodedata

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase

from marionette_driver.keys import Keys
from marionette_driver import By, Wait, Actions
import mozversion


class NewTabPagePinNoUndoRestoreAll(NewTabPageTestCase):
    """ Verify that pinning a tile does not display the 
        Undo/Restore All menu links """

    def test_pin_tile_does_not_invoke_undo_restore_all(self):
        with self.marionette.using_context('content'):
            self.set_enhanced_tiles()
            self.marionette.navigate(self.newtabPage)
            time.sleep(1)
            starting_tiles = self.get_tiles_grid()
            self.assertTrue(len(starting_tiles) > 3,
                            'FAILED: Insufficent starting tiles: %s' %
                            len(starting_tiles))
            pinned_tile = starting_tiles[2]
            self.pin_tile(pinned_tile['tile_object'])

            pinned_pref = self.prefs.get_pref('browser.newtabpage.pinned')
            self.assertTrue(
                pinned_tile['cell_text'] in pinned_pref,
                'browser.newtabpage.pinned pref not set when tile pinned')
            undo_status = self.get_undo_status()
            self.assertTrue(undo_status, 'FAILED: Undo Menu is not disabled')
            print 'Undo Menu Disabled is %s' % undo_status
            # Unpin the tile
            end_tiles = self.get_tiles_grid()
            self.pin_tile(end_tiles[2]['tile_object'])

        time.sleep(1)
