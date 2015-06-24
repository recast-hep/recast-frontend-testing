#-*- coding: utf-8 -*-
from page_objects import PageObject, PageElement

class CatalogPanel(PageObject):
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
    
    def getAnalActList(self):
        '''get list of all action fields for all requests'''
        anaLiItems = self.w.find_elements_by_class_name('views-field-analysis-actions')
        return anaLiItems

    def getTitle(self):
        '''get the title of the page from the page header'''
        return self.w.title

    def getNewAnalysis(self):
        '''get the New Analysis panel'''
        try: pe = PageElement(link_text="New Analysis")
        except NoSuchElementException, e:
            return False
        pe.click()
        return AnalysisPanel(self.w,'/node/add/analysis?destination=analyses-catalog')
    
    def getSubscribeLinks(self):
        try: pe = PageElement(link_text="subscribe")
        except NoSuchElementException, e:
            return False
        pe.click()
        return True

    def getAddRqstLinks(self):
        try: pe = PageElement(link_text="add request")
        except NoSuchElementException, e:
            return False
        #pe.click()
        #return True 
        return pe.get("/")
    
    def getRequestsPanel(self):
        
        