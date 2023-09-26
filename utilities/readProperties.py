import configparser

config=configparser.RawConfigParser()

config.read(".\\Configurations\\config.ini")

class ReadConfig:
    @staticmethod
    def getbaseURL():
        baseURL=config.get('common info','baseURL')
        return baseURL
    
    @staticmethod
    def getSearchTextGoogle():
        search_text_Google=config.get('common info','search_text_Google')
        return search_text_Google
    
    @staticmethod
    def getChromeOptionsArguments():
        chrome_options_arguments=config.get('common info','chrome_options_arguments')
        return chrome_options_arguments
    
    @staticmethod
    def getServiceObject():
        service_object=config.get('common info','service_object')
        return service_object
    
    @staticmethod
    def getemailorMobileNumber():
        emailorMobileNumber=config.get('common info','emailorMobileNumber')
        return emailorMobileNumber
    
    @staticmethod
    def getpassword():
        password=config.get('common info','password')
        return password
    
    @staticmethod
    def getproduct_category():
        product_category=config.get('common info','product_category')
        return product_category
    
    @staticmethod
    def getproductsearch():
        productsearch=config.get('common info','productsearch')
        return productsearch
    
    @staticmethod
    def getminprice():
        minprice=config.get('common info','minprice')
        return minprice
    
    @staticmethod
    def maxprice():
        maxprice=config.get('common info','maxprice')
        return maxprice