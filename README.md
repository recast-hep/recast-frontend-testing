The scripts presented in this project represent a test suite
for exercising the capabilities of the Recast web site pages
https://github.com/recast-hep

The python scripts found within this project use the Selenium
WebDriver for python as the execution vehicle.  To execute
these tests, first download the python Selenium WebDriver module
from https://pypi.python.org/pypi/selenium and use
one of the methods described there to install the module
into your python installation.  This installation can also
be done within a python 'venv' container/environment if desired.

These scripts utilize the Chrome web browser driver which
requires that the Chrome browser be installed in your
development system also.  If you wish to change this look
at each script's setUp block and select the desired
self.driver setting for the browser you want to use.
See the Selenium website (seleniumhq.org) for more information
on browsers supported by Selenium.

There also is a dependency upon the Python page-objects
package.  If you are using Anaconda Python (http://continuum.io/downloads)
you can use the pip tool to install this:
pip install page-objects


