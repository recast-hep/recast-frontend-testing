# -*- coding: utf-8 -*-
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from page_objects import PageObject, PageElement
import re

try:
    from HomePanel import HomePanel
except ImportError:
    pass # Assumes the error is due to multiple imports of HomePanel
try:
    from CatalogPanel import CatalogPanel
except ImportError:
    pass
try:
    from NewsPanel import NewsPanel
except ImportError:
    pass
try:
    from DevelopersPanel import DevelopersPanel
except ImportError:
    pass
try:
    from HelpPanel import HelpPanel
except ImportError:
    pass
try:
    from RequestsPanel import RequestsPanel
except ImportError:
    pass
try:
    from AboutPanel import AboutPanel
except ImportError:
    pass

#from locators import MainPageLocators

class LoginPanel(PageObject):
    username = PageElement(id_="edit-name")
    password = PageElement(id_="edit-pass")
    loginsubmit = PageElement(id_='edit-submit')
    login = PageElement(link_text='Login')
    form = PageElement(id_='user-login')
    homeLink = PageElement(link_text='Home')
    catalogLink = PageElement(link_text='Analyses Catalog')
    requestsLink = PageElement(link_text='Requests')
    aboutLink = PageElement(link_text='About')
    devsLink =PageElement(link_text='Developers')
    newsLink = PageElement(link_text='News')
    helpLink = PageElement(link_text='Help')

    def getTitle(self):
        return self.w.title
    
    def getPageTitle(self):
        ptitle = self.w.find_element_by_id('page-title')
        return ptitle.text
    
    def getHome(self):
        self.homeLink.click()
        return HomePanel(self.w,'/')
        
    def getCatalog(self):
        self.catalogLink.click()
        return CatalogPanel(self.w,'/?q=analyses-catalog')

    def getRequests(self):
        return RequestsPanel(self.w,'/?q=requests')

    def getAbout(self):
        return AboutPanel(self.w,'/?q=about-us')

    def getDevelopers(self):
        return DevelopersPanel(self.w,'/?q=developers')

    def getNews(self):
        return NewsPanel(self.w,'/?q=news')

    def getHelp(self):
        return HelpPanel(self.w,'/?q=support')

    def waitForView(self):
        self.w.find_element_by_partial_link_text('View')

    def getRealName(self):
        allUserDatum = self.w.find_elements_by_class_name('field-item')
        return allUserDatum[0].text

    def auditUserData(self):
        nameOK = False
        instOK = False
        allUserDatum = self.w.find_elements_by_class_name('field-item')
        for datum in allUserDatum:
            pattStrName = 'Wayne Motycka'
            nameLen = len(pattStrName)
            pattStrInstitution = 'University of Nebraska at Lincoln'
            instLen = len(pattStrInstitution)
            pattName = re.compile(pattStrName)
            pattInst = re.compile(pattStrInstitution)
            nameMatch = pattName.match(datum.text)
            if nameMatch.start() == 0 & nameMatch.end() == (nameLen -1):
                nameOK = True
            instMatch = pattInst.match(datum.text)
            if instMatch.start() == 0 & instMatch.end() == (instLen -1):
                instOK = True
        assert (nameOK & instOK)
        
            

    ## BOILER PLATE FUNCTIONS FROM Selenium IDE BELOW
    def is_element_present(self, how, what):
        try: self.w.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.w.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.w.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

