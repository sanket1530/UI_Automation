from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Google_Home_Page:
    textbox_search_xpath="//*[@title='Search']"
    links_xpath="//a[contains(@href,'https:')]"
    
    def __init__(self,driver,act):
        self.driver=driver
        self.act=act

    def search_Google_Home_Page(self,search_text_Google):
        self.driver.find_element(By.XPATH,self.textbox_search_xpath).send_keys(search_text_Google)

    def enter_button(self):
        self.act.key_down(Keys.ENTER).perform()
        self.act.key_up(Keys.ENTER).perform()
    
    def links_for_search_text_Google(self):
        links=self.driver.find_elements(By.XPATH,self.links_xpath)
        return links