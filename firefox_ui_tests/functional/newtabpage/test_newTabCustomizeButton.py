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

sys.path.append(path.dirname(path.abspath(__file__)))
from newTabPageTest import NewTabPageTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait

#####


class NewTabPageCustomizeButton(NewTabPageTestCase):
    """ Verify default state of the customize controls """

    def test_newTab_customizeButton_exists(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.newtabPage)
            customize_button = self.marionette.find_element(
                By.ID, self.customizeButton['id'])
            customize_buttonTitle = customize_button.get_attribute('title')
            self.assertEqual(
                customize_buttonTitle, self.customizeButton['expected'],
                '"%s" does NOT match "%s"' %
                (customize_buttonTitle, self.customizeButton['expected']))
            customize_button.click()

            panel = self.marionette.find_element(By.ID,
                                                 'newtab-customize-panel')

            for customize in self.customizeButtonElements:
                print 'Verifying Customize Button Title: %s' % \
                       self.customizeButtonElements[customize][ 'expected' ]
                print 'Verifying Customize Button ID   : %s' % \
                       self.customizeButtonElements[customize][ 'id' ]
                button = panel.find_element(
                    By.ID, self.customizeButtonElements[customize]['id'])
                buttonTitle = button.text
                print 'Button Title: %s' % buttonTitle
                self.assertFalse(button.is_selected(),
                                 '%s : Is Selected, it should not be' %
                                 buttonTitle)
                self.assertTrue(button.is_enabled(),
                                '%s : Is Not Enabled, it should be ' %
                                buttonTitle)
                self.assertTrue(button.is_displayed(),
                                '%s : Is Not Displayed, it should be ' %
                                buttonTitle)
                self.assertEqual(
                    buttonTitle,
                    self.customizeButtonElements[customize]['expected'],
                    '"%s" does NOT match "%s"' % (
                        buttonTitle,
                        self.customizeButtonElements[customize]['expected']))
            panel.send_keys(Keys.ESCAPE)
            print 'All Customize values match expected defaults'
