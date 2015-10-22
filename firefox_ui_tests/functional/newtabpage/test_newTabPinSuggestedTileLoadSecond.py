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


class NewTabPagePinSuggestedLoadSecond(NewTabPageTestCase):

    """ Load a suggested tile and Pin it
        Then try and trigger a new suggested tile
    """

    def test_pin_suggested_load_second_tile(self):
        with self.marionette.using_context('content'):
            # Set baseline conditions 
            self.set_enhanced_tiles()
            self.set_baseline_history()
            self.marionette.navigate(self.newtabPage)
            time.sleep(1)
            starting_tiles = self.get_tiles_grid()
            self.assertTrue(len(starting_tiles) > 3,
                            'FAILED: Insufficent starting tiles: %s' %
                            len(starting_tiles))

            # Load first suggested tile
            numTiles = len(self.directoryLinksData['suggested'])
            print 'There are %s suggested tile options' % numTiles
            tile1 = { 'explanation':None }
            tile2 = { 'explanation':None }
            targetTile1  = 0
            targetTile2  = 0
            # Pick to suggested tiles to aim for 
            # NEED TO BE DIFFERENT Categories (explinations)
            while tile1 == tile2:
                targetTile1 = random.randint(0, numTiles - 1)
                targetTile2 = random.randint(0, numTiles - 1)
                tile1 = self.get_directorylinks_tile_data(targetTile1, 'suggested')
                tile2 = self.get_directorylinks_tile_data(targetTile2, 'suggested')
                print 'TILE 1: %s' % tile1['explanation']
                print 'TILE 2: %s' % tile2['explanation']
            s_tile = self.load_suggested_tile(targetTile1)
            self.assertFalse(s_tile is None, 'FAILED: First suggested tile was not found')
            if s_tile.text == tile1['explanation']:
                print 'Found expected suggested: %s' % s_tile.text
            else:
                self.assertEquals(s_tile.text, tile2['explanation'],'First suggested tile matches second target tile')
                print 'Found unexpected suggested: %s' % s_tile.text
            second_tile_set = self.get_tiles_grid()
            pinned_tile = second_tile_set[0]
            self.pin_tile(pinned_tile['tile_object'])
            pinned_pref = self.prefs.get_pref('browser.newtabpage.pinned')
            self.assertTrue(
                pinned_tile['cell_text'] in pinned_pref,
                'browser.newtabpage.pinned pref not set when tile pinned')
            time.sleep(5)

            third_tile_set = self.get_tiles_grid()
            pprint.pprint(third_tile_set[0])
            # Now try and trigger a second suggested tile
            s_tile = self.load_suggested_tile(targetTile2)
            self.assertFalse(s_tile is None, 'FAILED: Second suggested tile was not found')
            print 'Found Suggested: %s' % s_tile.text
            if s_tile.text == tile2['explanation']:
                print 'Found expected second suggested tile'
            else:
                self.assertEquals(s_tile.text, tile1['explanation'],'Second suggested tile matches first target tile')
                if s_tile.text <> tile2['explanation']:
                    print 'Found a differnt suggested tile than expected, but still found one so its ok'
            time.sleep(5)
            final_tile_set = self.get_tiles_grid()
            self.assertEquals(pinned_tile['cell_text'],final_tile_set[0]['cell_text'], 'FAILED: First pinned suggested tile has changed')
            pprint.pprint(final_tile_set[0])
            pprint.pprint(final_tile_set[1])

