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

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait
import mozversion


class NewTabPageShowTopSitesNoHistory(NewTabPageTestCase):

    """ 
        Verify that no tiles are displayed when only 
        Show Top Sites in enabled and there is no history
    """

    def test_show_top_sites_no_history(self):
        with self.marionette.using_context('content'):
            self.set_blank_page()
            self.marionette.navigate(self.newtabPage)
            self.customize_show_top_sites()
            # Verify settings
            self.assertTrue(self.prefs.get_pref('browser.newtabpage.enabled'),
                            'newtabpage.enabled was not set to True')
            self.assertFalse(
                self.prefs.get_pref('browser.newtabpage.enhanced'),
                'newtabpage.enhanced was set to True')
            # Verify no tiles present
            tile_list = self.get_tiles_grid()
            for tile in tile_list:
                print 'FAILED: Tiles Found!'
                pprint.pprint(tile)
            self.assertEqual(len(tile_list), 0, 'Expected No Tiles found')
