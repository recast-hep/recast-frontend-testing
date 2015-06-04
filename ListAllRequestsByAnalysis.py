# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ListAllRequestsByAnalysis(unittest.TestCase):
    def setUp(self):
#        self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.base_url = "http://recast.perimeterinstitute.ca/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_list_all_requests_by_analysis(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Requests").click()
        pgcnt=1

        while(self.is_element_present(By.PARTIAL_LINK_TEXT,"next ")):
            curpg = int(driver.find_element_by_css_selector(".pager-current").text)
            assert curpg == pgcnt 
            pgcnt += 1
            driver.find_element_by_partial_link_text("next ").click()
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," previous")) == 1
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," first")) == 1

        #Verify next & last links are now gone on last page
        assert len(driver.find_elements(By.PARTIAL_LINK_TEXT,"next ")) < 1
        assert len(driver.find_elements(By.PARTIAL_LINK_TEXT,"last ")) < 1
        curpg = int(driver.find_element_by_css_selector(".pager-current").text)
        assert curpg == 5 

        #step back to first page
        while(self.is_element_present(By.PARTIAL_LINK_TEXT," previous")):
            curpg = int(driver.find_element_by_css_selector(".pager-current").text)
            assert curpg == pgcnt
            pgcnt -= 1
            driver.find_element_by_partial_link_text(" previous").click()
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT,"next ")) == 1
            assert len(driver.find_elements(By.PARTIAL_LINK_TEXT,"last ")) == 1

        #Verify links missing again on first page
        assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," previous")) < 1
        assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," first")) < 1

        #jump to last page via href last
        driver.find_element_by_partial_link_text("last ").click()
        #Verify last page
        curpg = int(driver.find_element_by_css_selector(".pager-current").text)
        assert curpg == 5 

        # Select the first page
        driver.find_element_by_partial_link_text(" first").click()
        #Verify return to first page again
        curpg = int(driver.find_element_by_css_selector(".pager-current").text)
        assert curpg == 1
        # Select the Incomplete status and verify only those display
        reqselect = Select(driver.find_element_by_class_name('form-select'))
        reqselect.select_by_visible_text("Incomplete")
        allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
        for statcol in allstats:
            if (statcol.text == u'Status'): # column header, ignore
                continue
            #print statcol.text
            self.assertEqual(statcol.text,u'Incomplete')

        # Now check the rest of the status options, Active, In Progress, Completed, Cancelled
        # select option Active from Status selector
        reqselect = Select(driver.find_element_by_class_name('form-select'))
        reqselect.select_by_visible_text("Active")
        allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
        for statcol in allstats:
            if (statcol.text == u'Status'): # column header, ignore
                continue
            self.assertEqual(statcol.text,u'Active')

        reqselect = Select(driver.find_element_by_class_name('form-select'))
        reqselect.select_by_visible_text("In Progress")
        allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
        for statcol in allstats:
            if (statcol.text == u'Status'): # column header, ignore
                continue
            self.assertEqual(statcol.text,u'In Progress')

        reqselect = Select(driver.find_element_by_class_name('form-select'))
        reqselect.select_by_visible_text("Completed")
        allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
        for statcol in allstats:
            if (statcol.text == u'Status'): # column header, ignore
                continue
            #print statcol.text
            self.assertEqual(statcol.text,u'Completed')

        reqselect = Select(driver.find_element_by_class_name('form-select'))
        reqselect.select_by_visible_text("Cancelled")
        allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
        for statcol in allstats:
            if (statcol.text == u'Status'): # column header, ignore
                continue
            #print statcol.text
            self.assertEqual(statcol.text,u'Cancelled')

        # Return to the All Status display
        reqselect = Select(driver.find_element_by_class_name('form-select'))
        reqselect.select_by_visible_text("- Any -")

        # Now login to reveal Showing: filter field of Requests
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("edit-name").clear()
        driver.find_element_by_id("edit-name").send_keys("testuser1")
        driver.find_element_by_id("edit-pass").clear()
        driver.find_element_by_id("edit-pass").send_keys("Pd6g%X2")
        driver.find_element_by_id("edit-submit").click()

        # These next tests requires the user be logged in, not visible w/o login
        # so if the Log out link is visible, they are logged in
        #assert len(driver.find_elements(By.PARTIAL_LINK_TEXT," previous")) < 1

        lcnt = driver.find_elements(By.ID,'page-title')
        #print lcnt[0].get_attribute('innerHTML')
        # Verify that testuser1 logged in
        self.assertEqual(lcnt[0].get_attribute('innerHTML'),u'\n          testuser1        ')
        if(len(lcnt) >= 1):
            driver.find_element_by_link_text("Requests").click()
            reqselect = Select(driver.find_element_by_class_name('form-select'))
            reqselect.select_by_visible_text("Incomplete")
            #driver.find_elements_by_link_text("Log out").click()
            if (len(driver.find_elements_by_link_text("Log out")) == 1):
                Select(driver.find_element_by_css_selector("select")).select_by_visible_text("My Requests")
                emptyview = driver.find_elements(By.CLASS_NAME,"views-empty")
                if(len(emptyview) < 1):
                    allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
                    for statcol in allstats:
                        if (statcol.text == u'Status'): # column header, ignore
                            continue
                        self.assertEqual(statcol.text,u'Incomplete')
                else:
                    print "emptyview >= 1 (1)"
            else:
                print "no logout seen (1)"

            if (len(driver.find_elements_by_link_text("Log out")) == 1):
                Select(driver.find_element_by_css_selector("select")).select_by_visible_text("Requests for analyses I'm subscribed to")
                emptyview = driver.find_elements(By.CLASS_NAME,"views-empty")
                if(len(emptyview) < 1):
                    allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
                    for statcol in allstats:
                        if (statcol.text == u'Status'): # column header, ignore
                            continue
                        self.assertEqual(statcol.text,u'Incomplete')
                else:
                    print "emptyview >= 1 (2)"
            else:
                print "no logout (subscribed rqsts 2)"

            if (len(driver.find_elements_by_link_text("Log out")) == 1):
                Select(driver.find_element_by_css_selector("select")).select_by_visible_text("Requests for analyses I responded to")
                emptyview = driver.find_elements(By.CLASS_NAME,"views-empty")
                if(len(emptyview) < 1):
                    allstats = driver.find_elements(By.CLASS_NAME,"views-field-field-request-status")
                    for statcol in allstats:
                        if (statcol.text == u'Status'): # column header, ignore
                            continue
                        self.assertEqual(statcol.text,u'Incomplete')
                else:
                    print "emptyview >= 1 (3)"
            else:
                print "no logout (responded rqsts 3)"

            #Terminate test by logging out
            driver.find_element_by_link_text("Log out").click()
## END OF TEST ##
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
### END OF MAIN ###

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
