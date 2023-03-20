from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')  # maximize the window
options.add_argument('--disable-gpu')


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get("https://www.nycu.edu.tw/")

# click news
element_news = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "新聞")))
element_news.click()


# click first news
element_first_news = driver.find_element(
    By.CSS_SELECTOR, ".su-posts-list-loop a")
element_first_news.click()


# print title and content
element_title = driver.find_element(
    By.CSS_SELECTOR, ".entry-header h1").text
element_content = driver.find_elements(
    By.CSS_SELECTOR, ".entry-content p")
print(element_title)
for content in element_content:
    print(content.text)


# open new tab and switch
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

driver.get("https://www.google.com")

# input id and return
element_input_id = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "q")))
element_input_id.send_keys("311553032")
element_input_id.send_keys(Keys.RETURN)


# print second title
element_second_title = driver.find_element(
    By.XPATH, '//*[@id="rso"]/div[3]/div/div/div[1]/div/a/h3').text
print(element_second_title)


# close the browser
driver.quit()
