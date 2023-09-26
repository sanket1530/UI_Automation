from pageObjects.GoogleHomePage import Google_Home_Page
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.action_chains import ActionChains
from pageObjects.AmazonPage import AmazonSite
from utilities.customLogger import LogGen
import pytest

class Test_002_Amazon:
    base_URL=ReadConfig.getbaseURL()
    search_text_Google=ReadConfig.getSearchTextGoogle()
    email=ReadConfig.getemailorMobileNumber()
    password=ReadConfig.getpassword()
    product_category=ReadConfig.getproduct_category()
    productsearch=ReadConfig.getproductsearch()
    minprice=ReadConfig.getminprice()
    maxprice=ReadConfig.maxprice()

    logger=LogGen.loggen()

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_Amazon_HomePage(self,driverinstance):
        self.logger.info("************* Start : Test_03_test_Amazon_HomePage *************")
        self.logger.info("************* Verifying Amazon Home Page *************")
        driver=driverinstance        
        driver.get(self.base_URL)
        act=ActionChains(driver)
        ghp=Google_Home_Page(driver,act)
        ghp.search_Google_Home_Page(self.search_text_Google)
        ghp.enter_button()
        links=ghp.links_for_search_text_Google()        
        for link in links:
            link_url=link.get_attribute("href")
            if link_url =="https://www.amazon.in/":
                link.click()
                break
        act_title=driver.title
        if "Amazon.in" in act_title:
            self.logger.info("************* Amazon Home Page is displayed *************")
            self.logger.info("************* End : Passed : Test_03_test_Amazon_HomePage *************")
            assert True
        else:
            self.logger.error("************* Amazon Home Page is not displayed *************")
            self.logger.error("************* End : Failed : Test_03_test_Amazon_HomePage *************")
            driver.save_screenshot(".\\Screenshots\\"+"Error_test_Amazon_HomePage.png")
            assert False    
        driver.quit()

    @pytest.mark.regression
    def test_Amazon_Product_Price_Search(self,driverinstance):
        self.logger.info("************* Start : Test_04_test_Amazon_Product_Price_Search *************")
        self.logger.info("************* Verifying Product Price Range *************")
        driver=driverinstance        
        driver.get(self.base_URL)
        act=ActionChains(driver)
        ghp=Google_Home_Page(driver,act)
        ghp.search_Google_Home_Page(self.search_text_Google)
        ghp.enter_button()
        links=ghp.links_for_search_text_Google()        
        for link in links:
            link_url=link.get_attribute("href")
            if link_url =="https://www.amazon.in/":
                link.click()
                break
        asp=AmazonSite(driver,act)
        asp.amazon_home_signin_window()
        asp.enter_email(self.email)
        asp.continue_button()
        asp.enter_password(self.password)
        asp.amazon_account_signin()
        allcat_dropdown=asp.allcategories_dropdown()
        allcat_dropdown.select_by_visible_text(self.product_category)
        asp.productsearch(self.productsearch)
        asp.enter_button()
        asp.minprice_product(self.minprice)
        asp.maxprice_product(self.maxprice)
        asp.fetchpriceresults()
        product_prices_list_page1=asp.product_prices()
        asp.gotopage(2)
        product_prices_list_page2=asp.product_prices()
        for prod_price in product_prices_list_page1:
            if int(prod_price) < int(self.minprice) or int(prod_price) > int(self.maxprice):
                driver.save_screenshot(".\\Screenshots\\"+"Error_test_Amazon_Product_Price_Search.png")
                flag1= False
            else:
                flag1= True
        for prod_price in product_prices_list_page2:
            print(int(prod_price),"in")
            if int(prod_price) < int(self.minprice) or int(prod_price) > int(self.maxprice):
                driver.save_screenshot(".\\Screenshots\\"+"Error_test_Amazon_Product_Price_Search.png")
                flag2= False
            else:
                flag2= True
        if (flag1 and flag2):
            self.logger.info("************* Product Price Range is Verified *************")
            self.logger.info("************* End : Passed : Test_04_test_Amazon_Product_Price_Search *************")
            assert True
        else:
            self.logger.error("************* Product Price Range is not correct *************")
            self.logger.error("************* End : Failed : Test_04_test_Amazon_Product_Price_Search *************")
            assert False
        asp.logoutAmazon()    
        driver.quit()
    
    @pytest.mark.regression
    def test_products_fivestar_rated(self,driverinstance):
        self.logger.info("************* Start : Test_05_test_products_fivestar_rated *************")
        self.logger.info("************* Verifying Five Star Rated Products *************")
        driver=driverinstance
        driver.get(self.base_URL)
        act=ActionChains(driver)
        ghp=Google_Home_Page(driver,act)
        ghp.search_Google_Home_Page(self.search_text_Google)
        ghp.enter_button()
        links=ghp.links_for_search_text_Google()        
        for link in links:
            link_url=link.get_attribute("href")
            if link_url =="https://www.amazon.in/":
                link.click()
                break
        asp=AmazonSite(driver,act)
        asp.amazon_home_signin_window()
        asp.enter_email(self.email)
        asp.continue_button()
        asp.enter_password(self.password)
        asp.amazon_account_signin()
        allcat_dropdown=asp.allcategories_dropdown()
        allcat_dropdown.select_by_visible_text(self.product_category)
        asp.productsearch(self.productsearch)
        asp.enter_button()
        asp.minprice_product(self.minprice)
        asp.maxprice_product(self.maxprice)
        asp.fetchpriceresults()
        productnameplusrating_1=asp.productnamewithstarrating()
        print(len(productnameplusrating_1))
        asp.gotopage(2)
        productnameplusrating_2=asp.productnamewithstarrating()
        print(len(productnameplusrating_2))
        productnameplusrating_1.update(productnameplusrating_2)     
        if len(productnameplusrating_1) > 0:
            print("********************** Start : All the products on the first 2 pages whose rating is 5 out of 5 **********************")
            prodfound = False
            for productname,rating in productnameplusrating_1.items():
                if rating == 5.0:
                    print(productname)
                    prodfound=True
                    assert True
            print("**********************   End : All the products on the first 2 pages whose rating is 5 out of 5 **********************")
            self.logger.info("************* Five Star Rated Products are present *************")
            self.logger.info("************* End : Passed : Test_05_test_products_fivestar_rated *************")
            if prodfound == False:
                    print("********************** No Product is rated 5 out of 5 **********************")
                    self.logger.info("************* Five Star Rated Products are not present *************")
                    self.logger.info("************* End : Passed : Test_05_test_products_fivestar_rated *************")
        else:
            driver.save_screenshot(".\\Screenshots\\"+"Error_test_products_fivestar_rated.png")
            self.logger.info("************* Error occured while fetching five star rated product *************")
            self.logger.info("************* End : Failed : Test_05_test_products_fivestar_rated *************")
            assert False
        asp.logoutAmazon()
        driver.quit()

    @pytest.mark.regression
    def test_wishlist_first_fivestar_rated_product(self,driverinstance):
        self.logger.info("************* Start : Test_06_test_wishlist_first_fivestar_rated_product *************")
        self.logger.info("************* Verifying First Five Star Rated Product Added to Wishlist *************")
        driver=driverinstance
        driver.get(self.base_URL)
        act=ActionChains(driver)
        ghp=Google_Home_Page(driver,act)
        ghp.search_Google_Home_Page(self.search_text_Google)
        ghp.enter_button()
        links=ghp.links_for_search_text_Google()        
        for link in links:
            link_url=link.get_attribute("href")
            if link_url =="https://www.amazon.in/":
                link.click()
                break
        asp=AmazonSite(driver,act)
        asp.amazon_home_signin_window()
        asp.enter_email(self.email)
        asp.continue_button()
        asp.enter_password(self.password)
        asp.amazon_account_signin()
        allcat_dropdown=asp.allcategories_dropdown()
        allcat_dropdown.select_by_visible_text(self.product_category)
        asp.productsearch(self.productsearch)
        asp.enter_button()
        asp.minprice_product(self.minprice)
        asp.maxprice_product(self.maxprice)
        asp.fetchpriceresults()
        product_name,productFoundFlag,wishListAddedProduct_Name = asp.wishlistfirstproductwith5starrating()
        if productFoundFlag == False:
            asp.gotopage(2)
            product_name,productFoundFlag,wishListAddedProduct_Name = asp.wishlistfirstproductwith5starrating()        
        if product_name == wishListAddedProduct_Name:
            assert True
            self.logger.info("************* First Five Star Rated Product is added to Wishlist *************")
            self.logger.info("************* End : Passed : Test_06_test_wishlist_first_fivestar_rated_product *************")
        else:
            self.logger.info("************* First Five Star Rated Product is not added to Wishlist *************")
            self.logger.info("************* End : Failed : Test_06_test_wishlist_first_fivestar_rated_product *************")
            assert False
        asp.logoutAmazon()
        driver.quit()