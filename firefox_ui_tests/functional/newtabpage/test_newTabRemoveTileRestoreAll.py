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


class NewTabPageRemoveSuggestedRestoreAll(NewTabPageTestCase):
    """ Verify that the Restore All button restores removed tile """

    def test_remove_suggested_restore_all(self):
        with self.marionette.using_context('content'):
            starting_blocked_pref = self.prefs.get_pref(
                'browser.newtabpage.blocked')
            self.set_enhanced_tiles()
            time.sleep(1)
            starting_tiles = self.get_tiles_grid()
            self.assertTrue(len(starting_tiles) > 3,
                            'FAILED: Insufficent starting tiles: %s' %
                            len(starting_tiles))
            removed_tile = starting_tiles[2]
            print 'Removing tile %s' % removed_tile['cell_text']
            self.remove_tile(removed_tile['tile_object'])
            # need to give time for the page to update
            time.sleep(1)
            blocked_pref = self.prefs.get_pref('browser.newtabpage.blocked')
            self.assertFalse(
                blocked_pref == starting_blocked_pref,
                'browser.newtabpage.blocked was not modified when tile blocked')
            removed_tiles = self.get_tiles_grid()
            for tile in removed_tiles:
                self.assertFalse(
                    tile['cell_text'] == removed_tile['cell_text'],
                    'Removed Tile found in tile list after it was blocked')
            # Restore All should bring removed tile back to starting slot

            undo_status = self.get_undo_status()
            self.assertTrue(undo_status is None,
                            'FAILED: Undo Menu is disabled')
            restore_button = self.get_restore_all_button()
            self.assertTrue(
                restore_button is not None,
                'FAILED: Restore All Button not present after a tile removed')
            self.restore_all()
            time.sleep(1)
            ending_tiles = self.get_tiles_grid()
            print 'starting tile:%s' % starting_tiles[2]['cell_text']
            print 'ending tile  :%s' % ending_tiles[2]['cell_text']
            self.assertEqual(ending_tiles[2]['cell_text'],
                             starting_tiles[2]['cell_text'],
                             'FAILED: Tile not restore to original location')
