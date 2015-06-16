from selenium import webdriver
#from selenium.support.ui import 
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

    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)


    def testRecastHomeBasic(self):
        "Test recast web Home Panel without login"
        homepanel = HomePanel( self.driver, "http://recast.perimeterinstitute.ca")
        homepanel.get("/")  # Launch the default page
        homepanel.chkHeaderLinks()
        homepanel.chkLinks_NoLogin()
        numpgs = homepanel.getTotHomeTblPgs()
        print "\nnumpgs: {}".format(numpgs)
        assert numpgs > 1
        homepanel.testPaging()
        homepanel.testRequestSort()
        homepanel.testAnalysisSort()
        homepanel.testStatusSort()
        
    def testRecastHomeLogin(self):
        homepanel = HomePanel( self.driver, "http://recast.perimeterinstitute.ca")
        homepanel.get("/")  # Launch the default page
        loginpanel = homepanel.getLoginPanel()
        loginpanel.username = "testuser1"
        loginpanel.password = "Pd6g%X2"
        loginpanel.loginsubmit.click()
        loginpanel.waitForView()
        h1title = loginpanel.getPageTitle()
        pattstr1 = 'testuser1'
        h1patt = re.compile(pattstr1)
        h1out = h1patt.match(h1title)
        if h1out:
            h1len = len(h1out.group())
            assert h1len == len(pattstr1)
        else:
            print '"{}" != '.format(h1title)
            print '"{}"/n'.format(pattstr1)
            assert False
        pgtitle = loginpanel.getTitle()
        pattstr2 = "testuser1 | RECAST [beta]"
        patt = re.compile(pattstr2)
        mout = patt.match(pgtitle)
        if mout:
            #titlelen = mout.endpos - mout.pos
            pglen = len(pgtitle)
            patlen = len(pattstr2)
            if patlen != pglen:
                print 'patlen {} pglen {}'.format(patlen,pglen)
                print '"{}"'.format(pgtitle)
                print ' != "{}"'.format(pattstr2)
                assert False
        else:
            print '"{}" != '.format(pgtitle)
            print '"{}"/n'.format(pattstr2)
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
        #try: self.webdriver.switch_to_alert()
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
