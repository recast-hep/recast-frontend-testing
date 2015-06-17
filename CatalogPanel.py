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
        anaLiItems = self.w.find_elements_by_class_name('views-field-analysis-actions')
        return anaLiItems
    