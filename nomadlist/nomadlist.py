from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import re
import pandas as pd
import time

def get_details(driver):

    table_element = driver.find_element(
        By.CSS_SELECTOR,
        'table.details'
    )

    key_elements = table_element.find_elements(
        By.CSS_SELECTOR,
        'td.key'
    )
    value_elements = table_element.find_elements(
        By.CSS_SELECTOR,
        'td.value'
    )

    keys = [key.text for key in key_elements]
    values = [value.text for value in value_elements]

    data = dict(zip(keys, values))

    return data


driver = webdriver.Chrome()
driver.implicitly_wait(10)

url = 'https://nomadlist.com/'

driver.get(url)
print(driver.title)

master_list = []
unique_labels = set()

for i in range(20):

    city_elements = driver.find_elements(
        By.CSS_SELECTOR,
        'li[data-type="city"]'
    )

    print(f"{i}: len(city_elements): {len(city_elements)}")

    last_element = city_elements[0]

    for index, city_element in enumerate(city_elements):
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable(city_element))
        # ActionChains(driver).move_to_element(city_element).perform()

        city_name = city_element.find_element(By.CSS_SELECTOR,
                                              'div.text h2').text
        city_name_id = city_element.get_attribute('data-slug')
        print(f'{index}: {city_name_id}')

        if city_name != '':

            if city_name not in unique_labels:
                unique_labels.add(city_name)

                print(f'{index}: {city_name}')


                city_name_id = re.sub(r"\s+", "-", city_name_id.lower())

                city_url = f'https://nomadlist.com/{city_name_id}'

                driver.execute_script("window.open('{}', '_blank');".format(city_url))
                driver.switch_to.window(driver.window_handles[-1])

                city_details = get_details(driver)
                # print(city_details)

                master_list.append({'city_name': city_name} | city_details)
                df = pd.DataFrame(master_list)

                df.to_csv('output.csv', index=False)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                last_element = city_element
        else:
            print('City name is empty')
            WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(last_element))
            ActionChains(driver).move_to_element(last_element).perform()
            time.sleep(1)

    print(f"{i} finished iterating through city_elements")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    time.sleep(1)