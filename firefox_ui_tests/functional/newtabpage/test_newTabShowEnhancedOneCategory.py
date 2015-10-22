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
import pprint

from urlparse import urlparse

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait
import mozversion


class NewTabPageShowSuggestedSitesOneCategory(NewTabPageTestCase):
    """ Verify a suggested tile will be displayed
        when miniumum criteria is met
        Actual suggested tile may vary from orginal
        target.
    """

    def test_suggested_tiles_one_category(self):
        with self.marionette.using_context('content'):
            self.set_baseline_history()
            self.set_enhanced_tiles()
            numTiles = len(self.directoryLinksData['suggested'])
            print 'There are %s suggested tile options' % numTiles
            targetTile = random.randint(0, numTiles - 1)
            s_tile = self.load_suggested_tile(targetTile)
            self.assertFalse(s_tile is None,
                                     'FAILED to find a suggested tile')
            print 'Found Suggested Tile:%s' % s_tile.text
