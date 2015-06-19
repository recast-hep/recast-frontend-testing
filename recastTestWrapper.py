from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from HomePanel import HomePanel
from LoginPanel import LoginPanel
from CatalogPanel import CatalogPanel
from AboutPanel import AboutPanel
from NewsPanel import NewsPanel
from DevelopersPanel import DevelopersPanel

import unittest, time, re

class recastTestWrapper(unittest.TestCase):
    pageURL = "http://recast.perimeterinstitute.ca" # Change when final web URL exists
    pageTitleLoggedin = "testuser1 | RECAST [beta]" # Change when non-Beta
    pageTitleNoLogin = "Latest Requests | RECAST [beta]" # Change when non-Beta
    testuser = "testuser1"
    userpwd = "Pd6g%X2"
    whitePaperLink = "http://arxiv.org/abs/1010.2506"

    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)


    def testRecastHomeBasic(self):
        "Test recast web Home Panel without login"
        homepanel = HomePanel( self.driver, self.pageURL)
        homepanel.get("/")  # Launch the default page
        homepanel.chkHeaderLinks() #
        self.driver.implicitly_wait(1) # Speed up search for non-valid links
        homepanel.chkLinks_NoLogin() # non-extant links test
        self.driver.implicitly_wait(5) # reset wait to normal
        homeTitle = homepanel.getTitle()
        titleStr = str(homeTitle) # unicode -> str conversion
        if titleStr != self.pageTitleNoLogin:
            print "page title mismatch {} != {}".format(titleStr, self.pageTitleNoLogin)
            assert False
        numpgs = homepanel.getTotHomeTblPgs()
        print "numpgs: {}".format(numpgs)
        assert numpgs > 1
        homepanel.testPaging()
        homepanel.pageSiteName.click() # Reset to initial page view
        homepanel.testRequestSort()
        homepanel.pageSiteName.click()
        homepanel.testAnalysisSort()
        homepanel.pageSiteName.click()
        homepanel.testStatusSort()
        homepanel.pageSiteName.click()
        wpUrl = homepanel.getPdfUrl()
        if str(wpUrl) != self.whitePaperLink:
            print "Unexpected white paper PDF link value"
            assert False

    def testRecastHomeLogin(self):
        homepanel = HomePanel( self.driver, "http://recast.perimeterinstitute.ca")
        homepanel.get("/")  # Launch the default page
        loginpanel = homepanel.getLoginPanel()
        loginpanel.username = self.testuser
        loginpanel.password = self.userpwd
        loginpanel.loginsubmit.click()
        loginpanel.waitForView()
        h1title = loginpanel.getPageTitle()
        h1str = str(h1title)
        if h1str != self.testuser:
            print '"{}" != '.format(h1title)
            print '"{}"'.format(self.testuser)
            assert False
        pgtitle = loginpanel.getTitle()
        if str(pgtitle) != self.pageTitleLoggedin:
            print '"{}" != '.format(pgtitle)
            print '"{}"/n'.format(self.pageTitleLoggedin)
            assert False

    def tearDown(self):
        self.driver.close()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        #try: self.webdriver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            #alert = self.webdriver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

#---START OF SCRIPT
if __name__=="__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase (recastTestWrapper)
    unittest.TextTestRunner(verbosity=2).run(suite)
