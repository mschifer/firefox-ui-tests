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

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait, Actions
import mozversion


class NewTabPageLearnAbout(NewTabPageTestCase):
    """ Verify that the Customize Button - Learn About link
        opens a new tab with the learn about page loaded.
    """

    def test_learn_about(self):
        self.locationbar = self.browser.navbar.locationbar
        action1 = Actions(self.marionette)
        startingTabCount = len(self.tabbar.tabs)
        with self.marionette.using_context('content'):
            self.customize_learn_about()

        endingTabCount = len(self.tabbar.tabs)
        self.assertEqual(startingTabCount + 1, endingTabCount,
                         'Learn About did not open new tab')
        self.tabbar.switch_to(self.tabbar.selected_index)

        with self.marionette.using_context('content'):
            Wait(self.marionette,
                 timeout=30).until(
                     lambda mn: self.learnAboutURL in mn.get_url())
            self.assertEqual(self.learnAboutURL, self.marionette.get_url(
            ), 'Learn About did not load the correct URL, Expected %s, Actual: %s'
                             % (self.learnAboutURL, self.marionette.get_url()))
        self.tabbar.close_tab(self.tabbar.tabs[(len(self.tabbar.tabs) - 1)])
