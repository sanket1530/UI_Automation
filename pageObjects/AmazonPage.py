import time,string,random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementClickInterceptedException


class AmazonSite:
    homesignin_button_xpath="//span[normalize-space()='Account & Lists']"
    email_textbox_xpath="//input[@id='ap_email']"
    continue_button_xpath="//input[@id='continue']"
    password_textbox_xpath="//input[@id='ap_password']"
    actualsignin_button_xpath="//input[@id='signInSubmit']"
    allcategories_dropdown_xpath="//select[@id='searchDropdownBox']"
    productsearch_textbox_xpath="//input[@id='twotabsearchtextbox']"
    minprice_textbox_xpath="//input[@id='low-price']"
    maxprice_textbox_xpath="//input[@id='high-price']"
    goprice_button_xpath="//input[@class='a-button-input']"
    productprices_value_xpath="//*[@class='a-section a-spacing-none a-spacing-top-micro puis-price-instructions-style']/descendant::span[@class='a-price-whole']"
    nextpage_button_xpath="//a[contains(@aria-label,'Go to next page')]"
    productstarrating_shape_xpath="//div[@class='a-row a-size-small']//span[@class='a-icon-alt']"
    productname_text_xpath="//div[@class='a-row a-size-small']//span[@class='a-icon-alt']/ancestor::div[@class='a-section a-spacing-none a-spacing-top-micro']/preceding-sibling::div//span[@class='a-size-medium a-color-base a-text-normal']"
    addtowishlist_button_xpath="//input[@id='add-to-wishlist-button']"
    wishListName_textbox_name="//input[@id='list-name']"
    createWishList_button_xpath="//*[@id='wl-redesigned-create-list']//input[@class='a-button-input a-declarative']"
    wishListAddedProduct_text_xpath="//*[@id='wl-huc-title-holder']"
    closeWishList_button_xpath="//button[@class=' a-button-close a-declarative']"
    amazonsignout_link_xpath="//span[normalize-space()='Sign Out']"

    def __init__(self,driver,act):
        self.driver=driver
        self.act=act

    def amazon_home_signin_window(self):
        self.driver.find_element(By.XPATH,self.homesignin_button_xpath).click()

    def enter_email(self,email):
        self.driver.find_element(By.XPATH,self.email_textbox_xpath).clear()
        self.driver.find_element(By.XPATH,self.email_textbox_xpath).send_keys(email)
    
    def continue_button(self):
        self.driver.find_element(By.XPATH,self.continue_button_xpath).click()

    def enter_password(self,password):
        self.driver.find_element(By.XPATH,self.password_textbox_xpath).clear()
        self.driver.find_element(By.XPATH,self.password_textbox_xpath).send_keys(password)

    def amazon_account_signin(self):
        self.driver.find_element(By.XPATH,self.actualsignin_button_xpath).click()

    def allcategories_dropdown(self):
        allcat_dropdown=Select(self.driver.find_element(By.XPATH,self.allcategories_dropdown_xpath))
        return allcat_dropdown
    
    def productsearch(self,productsearch):
        self.driver.find_element(By.XPATH,self.productsearch_textbox_xpath).clear()
        self.driver.find_element(By.XPATH,self.productsearch_textbox_xpath).send_keys(productsearch)

    def minprice_product(self,minprice):
        self.driver.find_element(By.XPATH,self.minprice_textbox_xpath).clear()
        self.driver.find_element(By.XPATH,self.minprice_textbox_xpath).send_keys(minprice)
        
    def maxprice_product(self,maxprice):
        self.driver.find_element(By.XPATH,self.maxprice_textbox_xpath).clear()
        self.driver.find_element(By.XPATH,self.maxprice_textbox_xpath).send_keys(maxprice)

    def fetchpriceresults(self):
        self.driver.find_element(By.XPATH,self.goprice_button_xpath).click()

    def enter_button(self):
        self.act.key_down(Keys.ENTER).perform()
        self.act.key_up(Keys.ENTER).perform()
    
    def links_for_search_text_Google(self):
        self.driver.find_elements(By.XPATH,self.links_xpath)

    def product_prices(self):
        nextpage_button=self.driver.find_element(By.XPATH,self.nextpage_button_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView(true);",nextpage_button)
        product_prices_element_list=self.driver.find_elements(By.XPATH,self.productprices_value_xpath)
        product_prices_list=[]
        for product in product_prices_element_list:
            i_product_price=product.text
            i_product_price=i_product_price.replace(",","")
            product_prices_list.append(i_product_price)        
        time.sleep(5) 
        return product_prices_list
    
    def gotopage(self,PageNumber):
        try:
            if PageNumber>1:
                totalPagestotraverse=PageNumber-1
                for i in range(0,totalPagestotraverse):
                    self.driver.find_element(By.XPATH,self.nextpage_button_xpath).click()
                    time.sleep(7)
            else:
                self.driver.find_element(By.XPATH,self.nextpage_button_xpath).click()          
        except Exception as e:
            print("Exception occured : "+str(e))
    
    def productnamewithstarrating(self):
        prod_name_element_list=self.driver.find_elements(By.XPATH,self.productname_text_xpath)        
        productnamerating={}              
        for index in range(1,len(prod_name_element_list)+1):
            prod_name_element=self.driver.find_element(By.XPATH,"("+self.productname_text_xpath+")["+str(index)+"]")
            product_name=prod_name_element.text
            prod_star_rating_element=self.driver.find_element(By.XPATH,"("+self.productstarrating_shape_xpath+")["+str(index)+"]")
            product_star_rating_text=prod_star_rating_element.get_attribute('textContent')
            product_star_rating_value=float(product_star_rating_text.split()[0])            
            if product_star_rating_value == 5.0 :
                self.driver.execute_script("arguments[0].scrollIntoView(true);",prod_name_element)
                time.sleep(5)
                characters = string.ascii_letters + string.digits
                random_string = ''.join(random.choice(characters) for _ in range(4))                      
                self.driver.save_screenshot(".\\Screenshots\\"+"products_fivestar_rated_"+random_string+".png")             
            productnamerating[product_name]=product_star_rating_value
        return productnamerating
    
    def wishlistfirstproductwith5starrating(self):        
        productFoundFlag = False
        product_name = "a"
        wishListAddedProduct_Name = "b"
        try:
            prod_name_element_list=self.driver.find_elements(By.XPATH,self.productname_text_xpath)              
            for index in range(1,len(prod_name_element_list)+1):
                prod_name_element=self.driver.find_element(By.XPATH,"("+self.productname_text_xpath+")["+str(index)+"]")            
                product_name=prod_name_element.text
                prod_star_rating_element=self.driver.find_element(By.XPATH,"("+self.productstarrating_shape_xpath+")["+str(index)+"]")
                product_star_rating_text=prod_star_rating_element.get_attribute('textContent')
                product_star_rating_value=float(product_star_rating_text.split()[0])            
                if product_star_rating_value == 5.0 :
                    if index>1:
                        prod_name_element_prev=self.driver.find_element(By.XPATH,"("+self.productname_text_xpath+")["+str(index-1)+"]")
                        self.driver.execute_script("arguments[0].scrollIntoView(true);",prod_name_element_prev)                
                    time.sleep(5)                    
                    self.driver.save_screenshot(".\\Screenshots\\"+"first5ratedproduct.png")
                    try:
                        prod_name_element.click()
                    except ElementClickInterceptedException:
                        print("ElementClickInterceptedException occured while trying to click on Product Name")
                        self.driver.execute_script("arguments[0].scrollIntoView(true);",prod_name_element)                    
                        prod_name_element.click()
                    windowIDs=self.driver.window_handles
                    self.driver.switch_to.window(windowIDs[1])
                    addtowishlist_dropdown=self.driver.find_element(By.XPATH,self.addtowishlist_button_xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);",addtowishlist_dropdown)
                    addtowishlist_dropdown.click()
                    self.driver.find_element(By.XPATH,"//span[normalize-space()='Create another Wish List']").click()
                    newwindowIDs=self.driver.window_handles
                    self.driver.switch_to.window(newwindowIDs[1])                              
                    numbers = string.digits
                    random_string = ''.join(random.choice(numbers) for _ in range(3))
                    self.driver.find_element(By.XPATH,self.wishListName_textbox_name).clear()
                    self.driver.find_element(By.XPATH,self.wishListName_textbox_name).send_keys("Shopping List ",random_string)                
                    self.driver.find_element(By.XPATH,self.createWishList_button_xpath).click()
                    time.sleep(4)
                    self.driver.save_screenshot(".\\Screenshots\\"+"WishListedProduct.png")                
                    wishListAddedProduct_Name=self.driver.find_element(By.XPATH,self.wishListAddedProduct_text_xpath).text                
                    productFoundFlag=True
                    self.driver.find_element(By.XPATH,self.closeWishList_button_xpath).click()
                    self.driver.switch_to.window(newwindowIDs[0])
                    break
        except Exception as e:
            print(e)  
            raise               
        return product_name,productFoundFlag,wishListAddedProduct_Name
    
    def logoutAmazon(self):
        time.sleep(2)
        accountLists=self.driver.find_element(By.XPATH,self.homesignin_button_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView(true);",accountLists)
        signout=self.driver.find_element(By.XPATH,self.amazonsignout_link_xpath)
        self.act.move_to_element(accountLists).move_to_element(signout).click().perform()
        time.sleep(3)
        