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


class NewTabPageShowTopSitesShortHistory(NewTabPageTestCase):

    """ Verify that only history tiles are displayed
        when only Show Top Sites is selected.
        * Select Show top Sites
        * Set base history 
        * Verify history tiles are displayed for sites visited
    """

    def test_show_top_sites_short_history(self):
        with self.marionette.using_context('content'):
            siteCount = self.set_baseline_history()
            self.set_blank_page()
            self.marionette.navigate(self.newtabPage)
            self.customize_show_top_sites()

            # Find total number of tiles we have on the page
            time.sleep(20)
            tile_list = self.get_tile_names()
            # Verify we have a history tile for each site visited
            for site in self.baseline_url_list:
                for title in site.keys():
                    self.assertTrue(title in tile_list.keys(),
                                    'History Site %s not found in tile list' %
                                    title)
                    print 'Verified History Tile: %s - %s' % (
                        title, tile_list[title]['type'])
            # Verify we don't have any tiles except history tiles
            for tile in tile_list.keys():
                self.assertTrue(tile_list[tile]['type'] == 'history',
                                'FAILED: Unexpected Type: %s -  %s' %
                                (tile, tile_list[tile]['type']))
            print 'No unexpected tile types found'
