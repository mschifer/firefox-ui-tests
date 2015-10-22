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


class HistoryTilePlacementMultipleSite(NewTabPageTestCase):
    """ 
       User history tiles should be displayed ahead of 
       directory/sponsored tiles
       * enabled suggested tiles so all tiles displayed
       * get current tile list.
       * visit sites
       *  site 0 will be visited 3 times
       *  site 1 will be visited twice
       *  site 3 will be visited once
       * History tiles should be in order 0, 1 2 - directory
       * get tile list and verify site visited is in 1st tile slot
    """

    def test_history_tile_placement_multiple_sites(self):
        with self.marionette.using_context('content'):
            self.set_enhanced_tiles()
            time.sleep(1)
            starting_tiles = self.get_tiles_grid()
            site_list = []
            site_list.append(self.baseline_url_list[0])
            self.load_pages(site_list, 1)
            site_list.append(self.baseline_url_list[1])
            self.load_pages(site_list, 1)
            site_list.append(self.baseline_url_list[2])
            self.load_pages(site_list, 1)
            self.marionette.navigate(self.newtabPage)
            ending_tiles = self.get_tiles_grid()
            print '-- First 6 Starting Tiles --'
            for i in range(0, 6, 1):
                print 'Starting Tile: %s' % starting_tiles[i]['cell_text']
            print '-- First 6  Ending Tiles --'
            for i in range(0, 6, 1):
                print 'Ending Tile  : %s' % ending_tiles[i]['cell_text']
            print ' -- Expected Tiles --'
            for i in range(0, len(site_list), 1):
                print 'Expected Tile: %s' % site_list[i].keys()
            for i in range(0, len(site_list), 1):
                self.assertFalse(
                    starting_tiles[i]['cell_text'] ==
                    ending_tiles[i]['cell_text'],
                    'FAILED: First tile is still the same from start')
                self.assertTrue(
                    ending_tiles[i]['cell_text'] in site_list[i].keys(),
                    'Expected first tile to match expected site')
