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


class NewTabPagePinSuggested(NewTabPageTestCase):

    """ Load a suggested tile and Pin it
        Verify state changes
    """

    def test_pin_suggested_second_tile(self):
        with self.marionette.using_context('content'):
            # Set baseline conditions 
            self.set_enhanced_tiles()
            self.set_baseline_history()
            self.marionette.navigate(self.newtabPage)
            time.sleep(1)
            # Load suggested tile
            numTiles = len(self.directoryLinksData['suggested'])
            print 'There are %s suggested tile options' % numTiles
            # Pick to suggested tiles to aim for 
            targetTile = random.randint(0, numTiles - 1)
            s_tile = self.load_suggested_tile(targetTile)
            self.assertFalse(s_tile is None, 'FAILED: Suggested tile was not found')
            tile_set = self.get_tiles_grid()
            suggested_tile = tile_set[0]
            self.pin_tile(suggested_tile['tile_object'])
            pinned_pref = self.prefs.get_pref('browser.newtabpage.pinned')
            self.assertTrue(
                suggested_tile['cell_text'] in pinned_pref,
                'browser.newtabpage.pinned pref not set when tile pinned')
            tile_set = self.get_tiles_grid()
            pinned_tile = tile_set[0]
            pprint.pprint(pinned_tile)
            self.assertEquals(suggested_tile['cell_text'],pinned_tile['cell_text'],'FAILED: Cell text has changed after pin')
            self.assertNotEqual(suggested_tile['type'],pinned_tile['type'],'FAILED: Cell Type has not changed after pin')
            self.assertEquals(pinned_tile['type'],'history','FAILED: Cell Type should be history after pin')
            self.assertTrue(pinned_tile['pinned'],'FAILED: Pinned attribute not set')
            time.sleep(5)

