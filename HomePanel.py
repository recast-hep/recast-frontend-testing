# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from page_objects import PageObject, PageElement
from LoginPanel import LoginPanel
#from locators import MainPageLocators

class HomePanel(PageObject):
    loginBtn = PageElement(link_text="Login")
    logoutBtn = PageElement(link_text="Log out")
    requestSort = PageElement(link_text="Request")
    analysisSort = PageElement(link_text="Analysis")
    statusSort = PageElement(link_text="Status")
    nextBtn = PageElement(partial_link_text="next ")
    prevBtn = PageElement(partial_link_text=" prev")
    firstBtn = PageElement(partial_link_text=" first")
    lastBtn = PageElement(partial_link_text="last ")
    searchBox = PageElement(id_="edit-search-block-form--2")

    def getNewAnalysis(self):
        #try: pe = PageElement(link_text,"New Analysis")
        #except NoSuchElementException, e: return False
	#return pe
	if(self.is_element_present(By.LINK_TEXT,"New Analysis")):
	    return PageElement(link_text,"New Analysis")
	else: return False

    def getSubscribe(self):
        return PageElement(link_text,"subscribe")

    def getAddRqst(self):
        return PageElement(link_text,"Add Request")

    def chkHeaderLinks(self):
	assert self.is_element_present(By.LINK_TEXT,"Feedback")
	assert self.is_element_present(By.LINK_TEXT,"Login")
	assert self.is_element_present(By.LINK_TEXT,"Register")

    def chkLinks_NoLogin(self): # Test when not logged links not present
        print "chkLinksNL\n"
        assert not self.is_element_present(By.LINK_TEXT,"New Analysis")
        assert not self.is_element_present(By.LINK_TEXT,'subscribe')
        assert not self.is_element_present(By.LINK_TEXT,'add request')
	print "done\n"

    def chkLinks_Login(self):  # Test when logged in links are visible
        assert self.is_element_present(By.LINK_TEXT,'New Analysis')
        assert self.is_element_present(By.LINK_TEXT,'subscribe')
        assert self.is_element_present(By.LINK_TEXT,'add request')

    def getTotHomeTblPgs(self): # return # of pages in analyses table
        totpages = self.w.find_elements(By.CLASS_NAME,"pager-item")
        maxpage = len(totpages) + 1
        return maxpage

    def getLoginPanel(self): # returns a LoginPanel object?
        loginBtn.click()
        return LoginPanel(self)

    def testPaging(self):
        pgcnt = 1
        while(self.is_element_present(By.PARTIAL_LINK_TEXT,"next ")):
	    pg = self.w.find_element_by_css_selector(".pager-current")
	    print "obj: {}\n".format(pg)
	    pgt = pg.text
	    print "text: {}\n".format(pgt)
            #curpg = int(self.w.find_element_by_css_selector(".pager-current").text)
	    curpg = int(pgt)
            print curpg
            assert curpg == pgcnt
            pgcnt += 1
            actCnt = 0
            incompCnt = 0
            inprogCnt = 0
            cancCnt = 0
            compCnt = 0
            allstats = self.w.find_elements(By.CLASS_NAME,"views-field-field-request-status")
            #allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
            for statcol in allstats:
                if (statcol.text == u'Status'): # column header, ignore
                    continue
                if(statcol.text == u'Active'):
                    actCnt += 1
                if(statcol.text == u'Incomplete'):
                    incompCnt += 1
                if(statcol.text == u'Complete'):
                    compCnt += 1
                if(statcol.text == u'InProgress'):
                    inprogCnt += 1
                if(statcol.text == u'Cancelled'):
                    cancCnt += 1
	    nextBtn = self.w.find_element_by_partial_link_text("next ")
	    nextBtn.click()

	print 'status counts: A{} IC{} C{} INP{} CAN{}'.format(actCnt,incompCnt,compCnt,inprogCnt,cancCnt)
	assert not (actCnt == 0 and incompCnt == 0 and compCnt == 0 and inprogCnt == 0 and cancCnt == 0)


# USEFUL BOILER PLATE FUNCTIONS CREATED BY SELENIUM_IDE
    def is_element_present(self, how, what):
        #try: self.webdriver.find_element(by=how, value=what)
        try: self.w.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        #try: self.webdriver.switch_to_alert()
        try: self.w.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            #alert = self.webdriver.switch_to_alert()
            alert = self.w.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
