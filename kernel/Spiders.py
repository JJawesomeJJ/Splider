#Description it is the spiders class to collect the data of website and we use "requests" and "selenium" as driver
import requests
from selenium import webdriver
class Spiders():
    url=None
    diver="requests"
    proxies =None
    def __init__(self,url):
        self.url=url
    def get_page_content(self,method='GET',params={},header={}):
        if self.diver=="requests":
            if method == 'GET':
                return requests.get(self.url, params=params, headers=header,proxies=self.proxies).text
            else:
                return requests.post(self.url, params=params, headers=header,proxies=self.proxies).text
        if self.diver=="webdriver":
            return self.webdriver(self.url)
    def set_diver(self,driver="requests"):
        self.diver=driver
        return self
    def set_proxies(self,proxies):
        self.proxies=proxies
        return self
    def webdriver(self,url):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        result=driver.page_source
        driver.close()
        return result