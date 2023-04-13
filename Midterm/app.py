from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

def main():

    # 遠端用下面
    # browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    browser.get("https://docs.python.org/3/tutorial/index.html")

    # 選擇中文
    # lan = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'language_switcher_placeholder')))


    h1 = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    print(h1.text)
    para = browser.find_elements(By.XPATH, "//section/p ")
    print(para[0].text)



    # 結束
    time.sleep(3)
    browser.quit()

if __name__ == "__main__":
    main()
