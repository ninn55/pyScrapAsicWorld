from selenium import webdriver

global MaxDepth
MaxDepth = 0

global DataDir
DataDir = "./data"

class ChromeDriver(object):
    def __init__(self):
        
        self._driver = None
        self.setdriver()
        #self.setheadlessdriver()
        
        #self.settimeout()
        
    def setheadlessdriver(self):
        self._driver = webdriver.Chrome(chrome_options=self.usroptions())

    def usroptions(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        return options

    def setdriver(self):
        self._driver = webdriver.Chrome()

    def settimeout(self):
        if self._driver == None:
            raise RuntimeError("set driver first")
        self._driver.set_page_load_timeout(10)

    def getdriver(self):
        if self._driver == None:
            raise RuntimeError("set driver first")
        return self._driver
    
    def __del__(self):
        self._driver.quit()
        del self._driver

global chromedriver
chromedriver = ChromeDriver()

if __name__ == "__main__":
    raise RuntimeError("Not callable")