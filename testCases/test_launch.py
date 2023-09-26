from pageObjects.GoogleHomePage import Google_Home_Page
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.action_chains import ActionChains
from utilities.customLogger import LogGen
import pytest

class Test_001_Launch_Browser:
    base_URL=ReadConfig.getbaseURL()
    search_text_Google=ReadConfig.getSearchTextGoogle()
    logger=LogGen.loggen()

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_Google_Home_Page_Title(self,driverinstance):
        self.logger.info("************* Start : Test_01_test_Google_Home_Page_Title *************")
        self.logger.info("************* Verifying Google Home Page i.e. Browser Launch *************")
        driver=driverinstance        
        driver.get(self.base_URL)
        act_title=driver.title
        if act_title=="Google":
            assert True
            self.logger.info("************* Google Home Page is displayed *************")
            self.logger.info("************* End : Passed : Test_01_test_Google_Home_Page_Title *************")
        else:
            driver.save_screenshot(".\\Screenshots\\"+"test_Google_Home_Page_Title.png")
            self.logger.error("************* Google Home Page is not displayed *************")
            self.logger.error("************* End : Failed : Test_01_test_Google_Home_Page_Title *************")
            assert False
        driver.quit()

    @pytest.mark.regression
    def test_Google_Home_Page_Search(self,driverinstance):
        self.logger.info("************* Start : Test_02_test_Google_Home_Page_Search *************")
        self.logger.info("************* Verifying Google Home Page Search Functionality *************")
        driver=driverinstance        
        driver.get(self.base_URL)
        act=ActionChains(driver)
        ghp=Google_Home_Page(driver,act)
        ghp.search_Google_Home_Page(self.search_text_Google)
        ghp.enter_button()
        act_title=driver.title
        if self.search_text_Google+" - Google Search" in act_title:
            assert True
            self.logger.info("************* Search Results are displayed successfully *************")
            self.logger.info("************* End : Passed : Test_02_test_Google_Home_Page_Search *************")
        else:
            driver.save_screenshot(".\\Screenshots\\"+"test_Google_Home_Page_Search.png")
            self.logger.error("************* Search Results are not displayed *************")
            self.logger.error("************* End : Failed : Test_02_test_Google_Home_Page_Search *************")
            assert False
        driver.quit()