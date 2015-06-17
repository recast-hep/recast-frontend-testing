from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from page_objects import PageObject, PageElement

try:
    from HomePanel import HomePanel
except ImportError:
    pass
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

#from locators import MainPageLocators

class RequestsPanel(PageObject):
    pass