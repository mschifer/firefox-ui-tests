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
import pprint
from urlparse import urlparse

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait, Actions
import mozversion


class NewTabPageEnhancedSitesNoHistory(NewTabPageTestCase):
    """ Verify customize include suggested sites
        shows the suggested tiles when no history 
        present
    """

    def test_show_enhanced_sites_no_history(self):
        self.places.remove_all_history()
        with self.marionette.using_context('content'):
            self.set_blank_page()
            self.marionette.navigate(self.newtabPage)
            self.customize_show_enhanced_sites()

            # Find total number of tiles we have on the page
            tile_list = self.get_tiles_grid()
            # Verify we don't have any history or suggested tiles
            for tile in tile_list:
                print 'Found Default Tile: %s - %s' % (tile['cell_text'],
                                                       tile['type'])
                self.assertTrue(tile['type'] in ['affiliate', 'sponsored'],
                                'FAILED: Unexpected Type: %s -  %s' %
                                (tile['cell_text'], tile['type']))
