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

class userScenarioTests(unittest.TestCase):
    """Implementation of use case scenarios describe in the
    Recast-database wiki as they apply to the web interface """
    pageURL = "http://recast.perimeterinstitute.ca" # Change when final web URL exists
    pageTitleLoggedin = "testuser1 | RECAST [beta]" # Change when non-Beta
    pageTitleNoLogin = "Latest Requests | RECAST [beta]" # Change when non-Beta
    testuser = "testuser1"
    userpwd = "Pd6g%X2"
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome() # Alternate driver if desired
        self.driver.implicitly_wait(5)
        
    def tearDown(self):
        self.driver.close()
        
    def listAllRqstForAnalysis(self):
        '''Scenario: I want to be able to list all requests associated to a 
        given analysis'''
        homepanel = HomePanel( self.driver, self.pageURL)
        homepanel.get("/")
        homepanel.analysesCatalog().click()
        anacatpanel = homepanel.getAnaCatalog().get('/')
        
    def listModelParamsForRequest(self):
        '''Scenario: I want to be able to list all model parameters and their
        values for a given request'''
        homepanel = HomePanel(self.driver,self.pageURL)
        homepanel.get("/")
        loginpanel = homepanel.getLoginPanel()
        loginpanel.username = self.testuser
        loginpanel.password = self.userpwd
        loginpanel.loginsubmit.click()
        ana
        homepanel.analysesCatalog().click()
        anacatpanel = homepanel.getAnaCatalog().get('/')
        anacatpanel.get("/")
        

    def viewMyAnalyses(self):
        '''Scenario: I want to be able to view all analyses I have submitted'''
        homepanel = HomePanel(self.driver,self.pageURL)
        homepanel.get("/")
        
    def viewAllAnalyses(self):
        '''Scenario: I want to be able to view all analyses submitted by others'''
        homepanel = HomePanel(self.driver,self.pageURL)
        homepanel.get("/")
        
    def viewDescAndArticlesForAnalysis(self):
        '''Scenario: I want to be able to view a description and published
        articles associated with an analysis'''
        homepanel = HomePanel(self.driver,self.pageURL)
        homepanel.get("/")
        
    def viewModelDescription(self):
        '''Scenario: I want to be able to view a description of a given model'''
        homepanel = HomePanel(self.driver,self.pageURL)
        homepanel.get("/")
        
        
## BOILERPLATE FUNCTIONS PROVIDED BY SELENIUM IDE CAPTURES
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
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
    suite = unittest.TestLoader().loadTestsFromTestCase (userScenarioTests)
    unittest.TextTestRunner(verbosity=2).run(suite)