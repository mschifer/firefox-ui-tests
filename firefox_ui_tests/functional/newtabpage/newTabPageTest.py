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
import os
from os import sys, path
import time
import platform
import pprint
import json
import urllib2
import random
from urlparse import urlparse

from firefox_ui_harness import FirefoxTestCase
from marionette_driver.keys import Keys
from marionette_driver import By, Wait, Actions
import mozversion


class NewTabPageTestCase(FirefoxTestCase):
    """ Set base state for all Remote New Tab Page tests
        * enable new tab page with enhanced tiles
        * disable intro and update tours 
        * init test data
        * open a new tab
    """

    def setUp(self):
        FirefoxTestCase.setUp(self)
        testConfigFile = '%s/%s' % (path.dirname(path.abspath(__file__)),
                                    'newtabConfig.json')
        print 'Check for file: %s' % testConfigFile
        self.configData = None
        if os.path.isfile(testConfigFile):
            f = open(testConfigFile, 'r')
            self.configData = json.load(f)
            f.close()
            for pref in self.configData['prefs']:
                print 'setting pref from config file: %s : %s' % (
                    pref, self.configData['prefs'][pref])
                self.prefs.set_pref(pref, self.configData['prefs'][pref])
                print 'Pref %s is now set to %s:' % (pref,
                                                     self.prefs.get_pref(pref))

        # Use Remote Tab if true
        self.newtabPage = 'about:newtab'
        self.remotetabDefault = self.prefs.get_pref(
            'browser.newtabpage.remote')
        if self.remotetabDefault:
            self.newtabPage = 'about:remote-newtab'

        # Ensure we start each test case witha new clean profile when run 
        # as a test suite.
        with self.marionette.using_context('content'):
            self.marionette.restart(clean=True, in_app=False)

        # Set window size so we have at least 2 rows of tiles displayed and visible
        self.start_size = self.marionette.window_size
        self.max_width = self.marionette.execute_script(
            "return window.screen.availWidth;")
        self.max_height = self.marionette.execute_script(
            "return window.screen.availHeight;")
        self.marionette.set_window_size(self.start_size['width'],
                                        self.start_size['height'] * 2)

        # Get a copy of the diretoryLinks.json file being used by the browser
        self.directoryLinksData = None
        binary = self.marionette.bin
        self.version_info = mozversion.get_version(binary=binary)
        self.directoryLinksURL = self.prefs.get_pref(
            'browser.newtabpage.directory.source').replace(
                '%LOCALE%', self.appinfo.locale).replace(
                    '%CHANNEL%', self.version_info['application_display_name'])
        self.directoryLinksData = self.get_directory_links_file(
            self.directoryLinksURL)

        self.baseline_url_list = [
            {'google.com': 'https://www.google.com'
             }, {'yahoo.com': 'https://www.yahoo.com'},
            {'duckduckgo.com': 'https://duckduckgo.com/'
                            }, {'reddit.com': 'https://www.reddit.com/'
                            }, {'github.com': 'https://github.com/'
                            }, {'facebook.com': 'https://www.facebook.com/'},
            {'sfbay.craigslist.org': 'http://sfbay.craigslist.org/'
             }, {'twitter.com': 'https://twitter.com/'}
        ]

        # Set tags used to identify controls
        self.customizeButton = {
            'id': 'newtab-customize-button',
            'expected': 'Customize your New Tab page'
        }
        self.customizeButtonElements = {
            'showTopSites': {
                'id': 'newtab-customize-classic',
                'expected': 'Show your top sites'
            },
            'includeSuggestedSites': {
                'id': 'newtab-customize-enhanced',
                'expected': 'Include suggested sites'
            },
            'showBlankPage':
            {'id': 'newtab-customize-blank',
             'expected': 'Show blank page'},
            'learnAboutNewTab': {
                'id': 'newtab-customize-learn',
                'expected': 'Learn about New Tab'
            }
        }

        self.learnAboutURL = 'https://www.mozilla.org/en-US/firefox/tiles/'
        self.defaultSearch = 'search.yahoo.com'
        self.tabbar = self.browser.tabbar

        # Save and set prefernces
        self.newtab_blocked_pref = self.prefs.get_pref(
            'browser.newtabpage.blocked')
        self.newtab_pinned_pref = self.prefs.get_pref(
            'browser.newtabpage.pinned')
        self.tabPref = self.prefs.get_pref('browser.newtabpage.enabled')
        self.enhancedPref = self.prefs.get_pref('browser.newtabpage.enhanced')
        self.newTabSourcePref = self.prefs.get_pref(
            'browser.newtabpage.directory.source')
        self.tourPref = self.prefs.get_pref('browser.newtabpage.introShown')
        self.updatedTourPref = self.prefs.get_pref(
            'browser.newtabpage.updateIntroShown')

        if self.newtab_blocked_pref <> None:
            self.prefs.set_pref('browser.newtabpage.blocked', '')
        if self.newtab_pinned_pref <> None:
            self.prefs.set_pref('browser.newtabpage.pinned', '[]')
        if self.tourPref <> None:
            self.prefs.set_pref('browser.newtabpage.introShown', True)
        if self.updatedTourPref <> None:
            self.prefs.set_pref('browser.newtabpage.updateIntroShown', True)

        # Set Default State
        self.prefs.set_pref('browser.newtabpage.enabled', True)
        self.prefs.set_pref('browser.newtabpage.enhanced', True)
        self.assertEqual(self.tabbar.window, self.browser)

        # Make sure we start off in a known state of 1 tab open
        while (len(self.tabbar.tabs) > 1):
            self.tabbar.close_tab(self.tabbar.tabs[(len(self.tabbar.tabs) - 1)
                                                   ])

        # Open a new tab
        self.tabbar.open_tab('button')

    """ Restore state to default
        * restore any prefs changed in setup to the original state
        * clear browser history 
        * close any extra open tabs
    """

    def tearDown(self):
        while (len(self.tabbar.tabs) > 1):
            self.tabbar.close_tab(self.tabbar.tabs[(len(self.tabbar.tabs) - 1)
                                                   ])

        # Restore prefs
        self.prefs.set_pref('browser.newtabpage.enabled', self.tabPref)
        self.prefs.set_pref('browser.newtabpage.enhanced', self.enhancedPref)
        if self.tourPref <> None:
            self.prefs.set_pref('browser.newtabpage.introShown', self.tourPref)
        if self.updatedTourPref <> None:
            self.prefs.set_pref('browser.newtabpage.updateIntroShown',
                                self.updatedTourPref)

        # Clear history
        self.places.remove_all_history()
        self.marionette.set_window_size(self.start_size['width'],
                                        self.start_size['height'])
        FirefoxTestCase.tearDown(self)

    """ Download the directoryLinks.json file and load it for future use """

    def get_directory_links_file(self, url):
        print 'Getting Directory Link JSON file:'
        print url
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        data = json.load(f)
        f.close()
        return data

    """ Load a URL and verify that it loaded """

    def load_pages(self, url_list, visit_count=1):
        with self.marionette.using_context('chrome'):
            self.locationbar = self.browser.navbar.locationbar
            for page_visit in range(visit_count):
                for targetSite in url_list:
                    for title in targetSite.keys():
                        tryCount = 0
                        retry = True
                        while retry:
                            url = targetSite[title]
                            print 'Trying to open: %s' % url
                            try:
                                # use sendkey to the url bar to get proper
                                # frequency score for tile display
                                self.locationbar.clear()
                                self.locationbar.urlbar.send_keys(url)
                                self.locationbar.urlbar.send_keys(
                                    self.keys.ENTER)
                                self.wait_page_loaded()
                                retry = False
                            except Exception, e:
                                tryCount += 1
                                print 'Unable to load page: %s' % url
                                if tryCount > 2:
                                    retry = False

    """ Print Page Source - For Debugging """

    def dump_page_source(self):
        print '--- PAGE SOURCE ---'
        pprint.pprint(self.marionette.page_source)
        print '--- END SOURCE ---'

    """ Open the customize button panel """

    def open_customize_panel(self, ):
        action = Actions(self.marionette)
        customize_button = self.marionette.find_element(
            By.ID, self.customizeButton['id'])

        # Move mouse out of the way first
        search_text = self.marionette.find_element(By.ID, 'newtab-search-text')
        action.move(search_text)
        action.perform()
        time.sleep(1)
        Wait(self.marionette).until(lambda mn: customize_button.is_displayed())
        customize_button.click()
        time.sleep(2)
        return self.marionette.find_element(By.ID, 'newtab-customize-panel')

    """ Click on the Show Top Sites element of the customize panel """

    def customize_show_top_sites(self):
        action = Actions(self.marionette)
        panel = self.open_customize_panel()
        topsites_button = panel.find_element(
            By.ID, self.customizeButtonElements['showTopSites']['id'])
        action.move(topsites_button)
        action.perform()
        Wait(self.marionette).until(lambda mn: topsites_button.is_displayed())
        time.sleep(1)
        topsites_button.click()
        time.sleep(1)
        panel.send_keys(Keys.ESCAPE)

    """ Click on the Include Suggested Sites element of the customize panel """

    def customize_show_enhanced_sites(self):
        action = Actions(self.marionette)
        panel = self.open_customize_panel()
        suggestedsites_button = panel.find_element(
            By.ID, self.customizeButtonElements['includeSuggestedSites']['id'])
        action.move(suggestedsites_button)
        action.perform()
        Wait(self.marionette).until(
            lambda mn: suggestedsites_button.is_displayed())
        time.sleep(1)
        suggestedsites_button.click()
        time.sleep(1)
        panel.send_keys(Keys.ESCAPE)

    """ Click on the Show Blank Page element of the customize panel """

    def customize_show_blank_page(self):
        action = Actions(self.marionette)
        panel = self.open_customize_panel()
        blank_button = panel.find_element(
            By.ID, self.customizeButtonElements['showBlankPage']['id'])
        action.move(blank_button)
        action.perform()
        Wait(self.marionette).until(lambda mn: blank_button.is_displayed())
        time.sleep(1)
        blank_button.click()
        time.sleep(1)
        panel.send_keys(Keys.ESCAPE)

    """ Click on the Learn About element of the customize panel """

    def customize_learn_about(self):
        action = Actions(self.marionette)
        panel = self.open_customize_panel()
        learn_button = panel.find_element(
            By.ID, self.customizeButtonElements['learnAboutNewTab']['id'])
        Wait(self.marionette).until(lambda mn: learn_button.is_displayed())
        action.move(learn_button)
        action.perform()
        learn_button.click()
        self.wait_page_loaded()
        panel.send_keys(Keys.ESCAPE)

    """ Set prefs to show blank page """

    def set_blank_page(self):
        if self.prefs.get_pref('browser.newtabpage.enabled'):
            self.prefs.set_pref('browser.newtabpage.enabled', False)
        if self.prefs.get_pref('browser.newtabpage.enhanced'):
            self.prefs.set_pref('browser.newtabpage.enhanced', False)

    """ Set prefs to show top sites """

    def set_top_sites_tiles(self):
        if not self.prefs.get_pref('browser.newtabpage.enabled'):
            self.prefs.set_pref('browser.newtabpage.enabled', True)
        if self.prefs.get_pref('browser.newtabpage.enhanced'):
            self.prefs.set_pref('browser.newtabpage.enhanced', False)

    """ Set prefs to suggested sites """

    def set_enhanced_tiles(self):
        if not self.prefs.get_pref('browser.newtabpage.enabled'):
            self.prefs.set_pref('browser.newtabpage.enabled', True)
        if not self.prefs.get_pref('browser.newtabpage.enhanced'):
            self.prefs.set_pref('browser.newtabpage.enhanced', True)

    """ Return a list of tiles in grid order """

    def get_tiles_grid(self):
        displayedTiles = []
        cell_list = self.marionette.find_elements(By.CLASS_NAME, "newtab-cell")
        c = 0
        for cell in cell_list:
            if (cell.find_elements(By.CLASS_NAME, "newtab-site")):
                cell_site = cell.find_element(By.CLASS_NAME, "newtab-site")
                tile = cell_site.find_element(By.CLASS_NAME, "newtab-link")
                cell_type = cell_site.get_attribute('type')
                cell_pinned = cell_site.get_attribute('pinned')
                cell_text = tile.text
                cell_title = tile.get_attribute('title')
                cell_href = tile.get_attribute('href')
                try:
                    cell_explanation = cell.find_element(
                        By.CLASS_NAME, "newtab-suggested-bounds").text
                except:
                    cell_explanation = None
                try:
                    sugg = self.marionette.find_element(
                        By.CLASS_NAME, "newtab-suggested-bounds")
                except:
                    # if element not found, not a tile
                    pass
                cell_thumb = tile.find_element(
                    By.CLASS_NAME, "newtab-thumbnail").get_attribute('style')
                cell_sugg = cell_site.find_element(
                    By.CLASS_NAME,
                    "newtab-thumbnail").get_attribute('suggested')
                cell_displayed = cell.is_displayed()
                tile_object = cell
                displayedTiles.append({
                    'url': cell_href,
                    'cell_text': cell_text,
                    'title': cell_title,
                    'thumbnail': cell_thumb,
                    'type': cell_type,
                    'displayed': cell_displayed,
                    'explanation': cell_explanation,
                    'pinned': cell_pinned,
                    'gridlocation': c,
                    'tile_object': tile_object
                })
            c += 1
        return displayedTiles

    """ Return dictionary of tiles by cell-text names """

    def get_tile_names(self):
        tileNames = {}
        cell_list = self.marionette.find_elements(By.CLASS_NAME, "newtab-cell")
        c = 0
        for cell in cell_list:
            if (cell.find_elements(By.CLASS_NAME, "newtab-site")):
                cell_site = cell.find_element(By.CLASS_NAME, "newtab-site")
                tile = cell_site.find_element(By.CLASS_NAME, "newtab-link")
                cell_type = cell_site.get_attribute('type')
                cell_text = tile.text
                tileNames[cell_text] = {'type': cell_type}
            c += 1
        return tileNames

    """ Get status of undo menu """

    def get_undo_status(self):
        menu = self.marionette.find_element(By.ID,"newtab-undo-container")
        status = menu.get_attribute("undo-disabled")
        return status



    """ Return object pointer to Restore All button """

    def get_restore_all_button(self):
        return self.marionette.find_element(By.ID,'newtab-undo-restore-button')

    """ Click on the Restore All link or throw assert if no button """

    def restore_all(self):
        restore = self.get_restore_all_button()
        restore.click()
        

    """ Return object pointer to Undo button """

    def get_undo_button(self):
        return self.marionette.find_element(By.ID, 'newtab-undo-button')

    """ Click on the Restore All link or throw assert if no button """

    def undo(self):
        undo = self.get_undo_button()
        undo.click()
        
    """ Return object pointer to tiles's remove button """

    def get_remove_all_button(self, tile_obj):
        return tile_obj.find_element(By.CLASS_NAME,
                                     'newtab-control newtab-control-block')

    """ Click on the tiles Remove This Site button """

    def remove_tile(self, tile_obj):
        action = Actions(self.marionette)
        button = self.get_remove_all_button(tile_obj)
        action.move(button)
        action.perform()
        Wait(self.marionette).until(lambda mn: button.is_displayed())
        button.click()

    """ Return object pointed to tile's Pin this site button """

    def get_pin_button(self, tile_obj):
        return tile_obj.find_element(By.CLASS_NAME,
                                     'newtab-control newtab-control-pin')

    """ Click on the tiles Pin This Site button """

    def pin_tile(self, tile_obj):
        action = Actions(self.marionette)
        button = self.get_pin_button(tile_obj)
        action.move(button)
        action.perform()
        Wait(self.marionette).until(lambda mn: button.is_displayed())
        button.click()

    """ Get the list of associated sites for a suggested tile """

    def get_sites(self, tile, maxSites=10):
        url_list = []
        siteList = tile['frecent_sites']
        numSites = len(siteList)
        for i in range(0, numSites, 1):
            siteIndex = random.randint(0, len(siteList) - 1)
            site = siteList[siteIndex]
            title = tile['title']
            url_list.append({title: 'http://%s' % site})
            del (siteList[siteIndex])
            if len(url_list) == maxSites:
                break
        return url_list

    """ Return the tile object for a suggested site tile if one exists
        return None if not found 
    """

    def get_suggested_tile(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.newtabPage)
            time.sleep(2)
            try:
                return self.marionette.find_element(By.CLASS_NAME,
                                                    "newtab-suggested-bounds")
            except Exception, e:
                return None

    """ Load a set of site urls for a given suggested tile """

    def load_suggested_sites(self,targetTile):
        tileCount = 0
        for tile in self.directoryLinksData['suggested']:
            if tileCount == targetTile:
                self.load_pages(self.get_sites(tile), 1)
                break
            tileCount += 1

    """ Load default pages as defined in self.baseline_url_list """

    def set_baseline_history(self):
        print 'Load baseline urls'
        self.load_pages(self.baseline_url_list, 1)
        return len(self.baseline_url_list)

    """ Wait until the page reload button is enabled """

    def wait_page_loaded(self):
        with self.marionette.using_context('chrome'):
            Wait(self.marionette).until(
                lambda mn: self.locationbar.stop_button.is_enabled() == False)

    """ Return directory links data for a given tile """


    def get_directorylinks_tile_data(self,targetTile,tileType):
        numTiles = len(self.directoryLinksData[tileType])
        tileCount = 0 
        for tile in self.directoryLinksData[tileType]:
            if tileCount == targetTile:
                pprint.pprint(tile)
                return tile
            tileCount += 1
        return None

    """ Load Suggested Tile """

    def load_suggested_tile(self, targetTile):
        s_tile = None
        maxAttepts = 5
        attempts = 0
        while ((s_tile is None) and (attempts < maxAttepts)):
            self.load_suggested_sites(targetTile)
            attempts += 1
            print 'Attempt %s, to trigger suggested tile' % attempts
            s_tile = self.get_suggested_tile()
        return s_tile
