# This Source Code Form is subject to the terms of the Mozilla Public
# v. 2.0. If a copy of the MPL was not distributed with this
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

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait
import mozversion


class NewTabPageShowSuggestedSitesClearHistory(NewTabPageTestCase):

    """ Verify that clearing history will remove
        suggested tile from display
    """

    def test_suggested_tiles_clear_history(self):
        with self.marionette.using_context('content'):
            self.set_baseline_history()
            self.set_enhanced_tiles()
            numTiles = len(self.directoryLinksData['suggested'])
            print 'There are %s suggested tile options' % numTiles
            targetTile = random.randint(0, numTiles - 1)
            tileCount = 0
            url_list = []
            for tile in self.directoryLinksData['suggested']:
                if tileCount == targetTile:
                    print 'Select This tile: %s : %s' % (tile['title'],
                                                         tile['explanation'])
                    explanation = tile['explanation']
                    url_list = self.get_sites(tile)
                    maxAttepts = 5
                    attempts = 0
                    while ((self.get_suggested_tile() is None) and
                           (attempts < maxAttepts)):
                        print 'Attempt: %s' % attempts
                        self.load_pages(url_list, 1)
                        attempts += 1
                    s_tile = self.get_suggested_tile()
                    time.sleep(1)
                    self.assertFalse(s_tile is None,
                                     'Failed to find a suggested tile')
                    print 'Found Suggested Tile:%s' % s_tile.text
                    break
                tileCount += 1
            print 'Clear History'
            with self.marionette.using_context('chrome'):
                self.places.remove_all_history()
            time.sleep(2)
            s_tile = self.get_suggested_tile()
            if s_tile is not None:
                print 'Found a suggested tile after clear history'
                print s_tile.text
            self.assertTrue(
                self.get_suggested_tile() is None,
                'FAILED: Suggested Tile still found after clear history')
            print 'PASS: No suggested site found after clear history'
