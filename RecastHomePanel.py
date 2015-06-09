# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class RecastHomePanel(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.base_url = "http://recast.perimeterinstitute.ca/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_recast_home_panel(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        #driver.find_element_by_link_partial_text(u"next ").click()
        #driver.find_element_by_link_partial_text(u"last ").click()
        #driver.find_element_by_link_partial_text(u" previous").click()
        #driver.find_element_by_link_partial_text(u" first").click()
        pgcnt = 1
        while(self.is_element_present(By.PARTIAL_LINK_TEXT,"next ")):
            curpg = int(driver.find_element_by_css_selector(".pager-current").text)
            print curpg
            assert curpg == pgcnt
            pgcnt += 1
            actCnt = 0
            incompCnt = 0
            inprogCnt = 0
            cancCnt = 0
            compCnt = 0
            allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
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

                #self.assertEqual(statcol.text,u'Active')
            print 'status counts: A{} IC{} C{} INP{} CAN{}'.format(actCnt,incompCnt,compCnt,inprogCnt,cancCnt)
            assert not (actCnt == 0 and incompCnt == 0 and compCnt == 0 and inprogCnt == 0 and cancCnt == 0)
            driver.find_element_by_partial_link_text(u"next ").click()
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," previous")) == 1
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," first")) == 1

        while(self.is_element_present(By.PARTIAL_LINK_TEXT," previous")):
            curpg = int(driver.find_element_by_css_selector(".pager-current").text)
            print curpg
            assert curpg == pgcnt
            pgcnt -= 1
            driver.find_element_by_partial_link_text(" previous").click()
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT,"next ")) == 1
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT,"last ")) == 1

        # exercise first & last page links
        driver.find_element_by_partial_link_text("last ").click()
        #Verify last page
        curpg = int(driver.find_element_by_css_selector(".pager-current").text)
        assert curpg == 5

        # Select the first page
        driver.find_element_by_partial_link_text(" first").click()
        #Verify return to first page again
        curpg = int(driver.find_element_by_css_selector(".pager-current").text)
        assert curpg == 1

        # Alternate objects to click on that cause sort of requests on Home Panel
        #driver.find_element_by_css_selector("img[alt=\"sort ascending\"]").click()
        #driver.find_element_by_css_selector("img[alt=\"sort descending\"]").click()
        # Test request sorting ascending/descending
        driver.find_element_by_link_text("Request").click()
        rqstNames = driver.find_elements(By.CLASS_NAME,"views-field-title")
        lastName = ""
        for namecol in rqstNames:
            if (namecol.text == u'Request'): # column header, ignore
                continue
            if(lastName == ""):
                lastName = namecol.text
                continue
            fltstr = float(namecol.text)
            lstflt = float(lastName)
            print 'cmp: {} >= {}'.format(fltstr, lstflt)
            assert(fltstr >= lstflt)
            lastName = namecol.text
        # Verify descending
        driver.find_element_by_link_text("Request").click()
        rqstNames = driver.find_elements(By.CLASS_NAME,"views-field-title")
        lastName = ""
        for namecol in rqstNames:
            if (namecol.text == u'Request'): # column header, ignore
                continue
            if(lastName == ""):
                lastName = namecol.text
                continue
            fltstr = float(namecol.text)
            lstflt = float(lastName)
            print 'cmp: {} <= {}'.format(fltstr, lstflt)
            assert(fltstr <= lstflt)

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
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
