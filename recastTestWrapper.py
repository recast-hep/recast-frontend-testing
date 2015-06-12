from selenium import webdriver
from selenium.webdriver.common.by import By
from HomePanel import HomePanel
from LoginPanel import LoginPanel
import unittest, time, re

class recastTestWrapper(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome() # self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(5) # seconds


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

    #def __new__(cls, *args, **kwargs):
    #    if not cls._instance:
    #    cls._instance = super(recastTestWrapper, cls).__new__(cls, *args, **kwargs)
    #    return cls._instance

    #def connect(self, host="http://recast.perimeterinstitute.ca/"):
    #    #self.driver = webdriver.Firefox()
    #    self.driver = webdriver.Chrome() # Loads faster than FF, but not preferred
    #    self.base_url = host
    #    return self.driver

    def tearDown(self):
        self.driver.close()
        #self.webdriver.close()

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
