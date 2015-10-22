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
from marionette_driver import By, Wait
import mozversion


class NewTabPageSearch(NewTabPageTestCase):
    def test_newtab_search(self):
        self.locationbar = self.browser.navbar.locationbar

        with self.marionette.using_context('content'):
            self.set_enhanced_tiles()
            search_text = self.marionette.find_element(By.ID,
                                                       'newtab-search-text')
            search_button = self.marionette.find_element(
                By.ID, 'newtab-search-submit')
            search_text.send_keys('happy cows')
            time.sleep(1)
            search_button.click()
            print 'Verify that %s was loaded on search' % self.defaultSearch
            Wait(self.marionette).until(
                lambda mn: self.defaultSearch in mn.get_url())
            self.wait_page_loaded()

            # Verify we have a search page now
            print 'Loaded URL: %s' % self.marionette.get_url()
            self.assertTrue((self.defaultSearch in self.marionette.get_url()),
                            'Wrong Search Provider URL found: %s' %
                            self.marionette.get_url())
