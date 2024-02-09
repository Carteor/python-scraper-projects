import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


url = 'https://www.fruitlogistica.com/en/trade-visitors/exhibitor-search/#/search/f=h-entity_orga;st=2;v_sg=0;v_fg=0;v_fpa=FUTURE;desc=true'

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get(url)
print(driver.title)

# After loading the page a popup asking about cookies appears.
# The standard methods to locate and press buttons to accept cookies don't work
# We need to locate the whole element that would intercept our clicks on listings
interceptor_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR,
        'div#usercentrics-root'
    ))
)
print('interception element located')

# Let's try deleting the intercepting element from DOM using Javascript
driver.execute_script("arguments[0].remove();", interceptor_element)

listing_element = driver.find_element(
    By.CSS_SELECTOR,
    '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.listContentContainer > div > div.EWP5KKC-e-J > div:nth-child(1)'
)
listing_element.click()

time.sleep(100)
