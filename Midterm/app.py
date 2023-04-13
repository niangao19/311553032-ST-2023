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
    # sel = Select(browser.find_element(By.ID, 'language_select'))
    #sel.select_by_value("zh-tw")
    #sel.select_by_index(8)

    # target = browser.find_element(By.XPATH, "//select[@id='language_select']/options[@value='zh-tw')]")
    # print(target)

    h1 = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    print(h1.text)
    para = browser.find_elements(By.XPATH, "//section/p ")
    print(para[0].text)

    #search = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.NAME, 'q') and (By.XPATH, "//form/input")))
    # search = browser.find_elements(By.TAG_NAME, 'input')
    # for i in range(len(search)):
    #     if(search[i].get_attribute("type") == "text" and search[i].get_attribute("placeholder")):
    #         print(search[i])

    # 結束
    time.sleep(3)
    browser.quit()

if __name__ == "__main__":
    main()