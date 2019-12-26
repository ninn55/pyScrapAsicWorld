from selenium import webdriver

global MaxDepth
MaxDepth = 2

global DataDir
DataDir = "./data"

class ChromeDriver(object):
    def __init__(self):
        
        self._driver = None
        self._options = webdriver.ChromeOptions()
        self.usroptionsextension()
        #self.settimeout()
        self.setdriver()
        
    def usroptionsextension(self):
        self._options.add_argument("load-extension=%(path)s"%{
            "path": ".\\uBlock\\uBlock0.chromium"
            })

    def usroptionsheadless(self):
        self._options.add_argument('headless')

    def setdriver(self):
        self._driver = webdriver.Chrome(chrome_options=self._options)

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