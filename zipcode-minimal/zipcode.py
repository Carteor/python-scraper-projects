#There was an attempt to create a simple script without using big dependencies using just urllib and websockets
# but I failed...

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# location = input("City: ")
location = 'New York'

url = 'https://www.christopher-vogt.com/city2zip/'

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get(url)
print(driver.title)

textarea_element = driver.find_element(By.CSS_SELECTOR,
                                       'textarea#city_data')
textarea_element.send_keys(location)

search_button_element = driver.find_element(
    By.CSS_SELECTOR,
    'button#search_button'
)
search_button_element.click()

result_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR,
        'p.result'
    )
    )
)
result = result_element.text
print(result)