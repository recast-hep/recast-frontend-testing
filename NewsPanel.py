#-*- coding: utf-8 -*-
from page_objects import PageObject, PageElement

class NewsPanel(PageObject):
    loginBtn = PageElement(link_text="Login")
    logoutBtn = PageElement(link_text="Log out")
    homeLink = PageElement(link_text='Home')
    catalogLink = PageElement(link_text='Analyses Catalog')
    requestsLink = PageElement(link_text='Requests')
    aboutLink = PageElement(link_text='About')
    devsLink =PageElement(link_text='Developers')
    newsLink = PageElement(link_text='News')
    helpLink = PageElement(link_text='Help')