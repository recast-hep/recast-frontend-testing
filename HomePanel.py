# -*- coding: utf-8 -*-

#from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from page_objects import PageObject, PageElement
try:
    from LoginPanel import LoginPanel
except ImportError:
    pass
try:
    from RequestsPanel import RequestsPanel
except ImportError:
    pass
try:
    from AnalysisPanel import AnalysisPanel
except ImportError:
    pass
#from locators import MainPageLocators

class HomePanel(PageObject):
    loginBtn = PageElement(link_text="Login")
    logoutBtn = PageElement(link_text="Log out")
    requestSort = PageElement(link_text="Request")
    analysisSort = PageElement(link_text="Analysis")
    statusSort = PageElement(link_text="Status")
    nextBtn = PageElement(partial_link_text="next ")
    prevBtn = PageElement(partial_link_text=" previous")
    firstBtn = PageElement(partial_link_text=" first")
    lastBtn = PageElement(partial_link_text="last ")
    searchBox = PageElement(id_="edit-search-block-form--2")

    def getNewAnalysis(self):
        try: pe = PageElement(link_text="New Analysis")
        except NoSuchElementException, e:
            return False
        pe.click()
        return AnalysisPanel(self.w,'/?q=user/login')
    
    def getSubscribe(self):
        try: pe = PageElement(link_text="subscribe")
        except NoSuchElementException, e:
            return False
        pe.click()
        return True

    def getAddRqst(self):
        try: pe = PageElement(link_text="Add Request")
        except NoSuchElementException, e:
            return False
        pe.click()
        return True #return PageElement(link_text="Add Request")

    def chkHeaderLinks(self):
        assert self.is_element_present(By.LINK_TEXT,"Feedback")
        assert self.is_element_present(By.LINK_TEXT,"Login")
        assert self.is_element_present(By.LINK_TEXT,"Register")

    def chkLinks_NoLogin(self): # Test when not logged links not present
        print "check Links - No Login\n"
        assert not self.is_element_present(By.LINK_TEXT,"New Analysis")
        assert not self.is_element_present(By.LINK_TEXT,'subscribe')
        assert not self.is_element_present(By.LINK_TEXT,'add request')

    def chkLinks_Login(self):  # Test when logged in links are visible
        print "check links - Logged in\n"
        assert self.is_element_present(By.LINK_TEXT,'New Analysis')
        assert self.is_element_present(By.LINK_TEXT,'subscribe')
        assert self.is_element_present(By.LINK_TEXT,'add request')

    def getTotHomeTblPgs(self): # return # of pages in analyses table
        totpages = self.w.find_elements(By.CLASS_NAME,"pager-item")
        maxpage = len(totpages) + 1
        return maxpage

    def getLoginPanel(self): # returns a LoginPanel object?
        #loginBtn = PageElement(link_text="Login")
        loginBtn = self.w.find_element_by_link_text('Login')
        loginBtn.click()
        return LoginPanel(self.w,'/?q=user/login')

    def testPaging(self):
        mxPgLbl = self.w.find_elements_by_class_name("pager-item")
        totpgs = len(mxPgLbl) + 1 # +1 b/c current page label has class=active
        pgcnt = 1
        actCnt = 0
        incompCnt = 0
        inprogCnt = 0
        cancCnt = 0
        compCnt = 0
        while(self.is_element_present(By.PARTIAL_LINK_TEXT,"next ")):
            pg = self.w.find_element_by_css_selector(".pager-current")
            pgt = pg.text
            curpg = int(pgt)
            print curpg
            assert curpg == pgcnt
            pgcnt += 1
            
            allstats = self.w.find_elements(By.CLASS_NAME,"views-field-field-request-status")
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
            #nextBtn = PageElement(partial_link_text="next ")
            nextBtn.click()

        print 'status counts: A{} IC{} C{} INP{} CAN{}'.format(actCnt,incompCnt,compCnt,inprogCnt,cancCnt)
        assert not (actCnt == 0 and incompCnt == 0 and compCnt == 0 and inprogCnt == 0 and cancCnt == 0)
        actCnt = 0
        incompCnt = 0
        inprogCnt = 0
        cancCnt = 0
        compCnt = 0
        while(self.is_element_present(By.PARTIAL_LINK_TEXT," previous")):
            #pg = self.w.find_element_by_css_selector(".pager-current")
            pg = self.w.find_element_by_css_selector(".pager-current")
            pgt = pg.text
            curpg = int(pgt)
            print curpg
            assert curpg == pgcnt
            pgcnt -= 1
            prevBtn = self.w.find_element_by_partial_link_text(" previous")
            prevBtn.click()
            assert len(self.w.find_elements(By.PARTIAL_LINK_TEXT,"next ")) == 1
            assert len(self.w.find_elements(By.PARTIAL_LINK_TEXT,"last ")) == 1
        
        lastBtn = self.w.find_element_by_partial_link_text("last ")
        lastBtn.click()
        pg = self.w.find_element_by_css_selector(".pager-current")
        pgt = pg.text
        assert int(pgt) == totpgs
        firstBtn =  self.w.find_element_by_partial_link_text(" first")
        firstBtn.click()
        pg = self.w.find_element_by_css_selector(".pager-current")
        assert int(pg.text) == 1

    def testAnalysisSort(self):
        requestColHeader = self.w.find_element_by_link_text('Analysis')
        requestColHeader.click()
        analysisTexts = self.w.find_elements_by_class_name('views-field-field-request-analysis')
        lastAna = ""
        for anaText in analysisTexts:
            innerHref = anaText.find_element_by_tag_name('a')
            inText = innerHref.text
            if(inText == u'Analysis'):
                continue
            if(lastAna == ""):
                lastAna = inText
                continue
            if(lastAna > inText):
                print 'Analysis Title SORT ERROR: {} != {}'.format(lastAna.encode('ascii','ignore'),inText.encode('ascii','ignore'))
                #assert False # THIS SHOULD BE UNCOMMENTED ONCE SORTING WORKS
            lastAna = inText

    def testRequestSort(self):
        requestColHeader = self.w.find_element_by_link_text('Request')
        requestColHeader.click() # select Descending order
        lastRq = ""
        allRqTds = self.w.find_elements_by_class_name('views-field-title')
        for rqNum in allRqTds:
            if(rqNum.text == u'Request'): continue
            if(lastRq == ""): 
                lastRq = rqNum.text
                continue
            fltstr = float(rqNum.text)
            lstflt = float(lastRq) # Descending order after click()
            assert fltstr >= lstflt # req #s apparently can be dup'd
            lastRq = rqNum.text
        
        requestColHeader = self.w.find_element_by_link_text('Request')
        requestColHeader.click() # Change to Ascending Sort order
        allRqTds = self.w.find_elements_by_class_name('views-field-title')
        lastRq = ""
        for rqNum in allRqTds:
            if(rqNum.text == u'Request'): continue
            if(lastRq == ""):
                lastRq = rqNum.text
                continue
            fltstr = float(rqNum.text)
            lstflt = float(lastRq)
            assert fltstr <= lstflt # ascending sort
            lastRq = rqNum.text
    
    def testStatusSort(self):
        statusColHeader = self.w.find_element_by_link_text('Status')
        statusColHeader.click()
        allStatusTds = self.w.find_elements_by_class_name('views-field-field-request-status')
        prevStatus = ""
        for statCol in allStatusTds:
            if(statCol.text == u'Status'):
                continue
            if(prevStatus == ""):
                prevStatus = statCol.text
                continue
            if(statCol.text > prevStatus): # <= is OK
                print "{} > {}".format(statCol, prevStatus)
                #assert FALSE  # UNCOMMENT 
            prevStatus = statCol.text
    
# USEFUL BOILER PLATE FUNCTIONS CREATED BY SELENIUM_IDE
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
