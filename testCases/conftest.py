from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service
from utilities.readProperties import ReadConfig
from pytest_metadata.plugin import metadata_key

opt=webdriver.ChromeOptions()
args=ReadConfig.getChromeOptionsArguments()
opt.add_argument(args)
opt.page_load_strategy = 'normal'
s_obj=ReadConfig.getServiceObject()
print(s_obj)
serv_obj=Service(s_obj)

@pytest.fixture()
def driverinstance(browser):
    if browser == 'chrome' or browser == '':        
        driver=webdriver.Chrome(options=opt,service=serv_obj)
        driver.implicitly_wait(10)
    elif browser == 'firefox':
        driver=webdriver.Firefox()
    return driver

def pytest_addoption(parser): # This will get value from CLI/hooks
    parser.addoption("--browser",default="chrome")

@pytest.fixture()
def browser(request): # This will return the browser value to driverinstance menthod
    return request.config.getoption("--browser")

######### Pytest HTML Report #########
@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    report.title = "Amazon UI Testing"

# Hook for adding environment info in HTML Report 
@pytest.hookimpl(optionalhook=True)
def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Amazon UI"
    config.stash[metadata_key]["Tester"] = "Sanket"

@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("Plugins", None)    
