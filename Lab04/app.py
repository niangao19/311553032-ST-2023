from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

if __name__ == '__main__' :
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get('https://www.nycu.edu.tw/')
    button = driver.find_element(By.LINK_TEXT,"新聞") 
    button.click()
    button = driver.find_element(By.CLASS_NAME,"su-post")   
    button.click()
    title = driver.find_element(By.XPATH, '//h1[@class="single-post-title entry-title"]')
    print(title.text)
    content = driver.find_element(By.XPATH, '//div[@class="entry-content clr"]')
    print(content.text)

    driver.get('https://www.google.com')
    input_text = driver.find_element(By.NAME,'q')
    input_text.send_keys('311553032')
    input_text.submit()


    titles= driver.find_elements(By.XPATH, "//h3[@class='LC20lb MBeuO DKV0Md']")
    print(titles[1].text)
    driver.close()
