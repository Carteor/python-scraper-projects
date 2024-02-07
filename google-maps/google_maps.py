import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import pandas as pd


def scrape_panel(listing):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(listing))

    try:
        listing.click()
    except ElementClickInterceptedException:
        driver.execute_script("""
        var button = document.querySelector('#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button');
        if (button) {
            button.remove();
        }
        """)
        listing.click()

    time.sleep(2)

    panel_element = driver.find_element(
        By.CSS_SELECTOR,
        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc'
    )

    heading_element = panel_element.find_element(
        By.CSS_SELECTOR,
        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1'
    )
    # print(heading_element.text)
    # Name Of Business
    name = heading_element.text
    # Address Of Business
    address = panel_element.find_element(
        By.CSS_SELECTOR,
        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(7) > div:nth-child(3) > button > div > div.rogA2c > div.Io6YTe.fontBodyMedium.kR99db'
    ).text
    # print(address)
    # Phone Number
    try:
        phone_number = panel_element.find_element(
            By.CSS_SELECTOR,
            '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(7) > div:nth-child(6) > button > div > div.rogA2c > div.Io6YTe.fontBodyMedium.kR99db'
            # '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(7) > div:nth-child(7) > button > div > div.rogA2c > div.Io6YTe.fontBodyMedium.kR99db'
        ).text
    except NoSuchElementException:
        phone_number = 'No phone number available'
    # print(phone_number)
    # Email - businesses don't have emails?
    # try:
    #     email = panel_element.find_element(
    #     By.CSS_SELECTOR,
    #     ''
    # ).text
    # except NoSuchElementException:
    #     email = 'No email available'

    # Website
    try:
        website = panel_element.find_element(
        By.CSS_SELECTOR,
        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(7) > div:nth-child(7) > a > div > div.rogA2c.ITvuef > div.Io6YTe.fontBodyMedium.kR99db'
    ).text
    except NoSuchElementException:
        website = 'No website available'
    # print(website)

    return {
        'name': name,
        'address': address,
        'phone_number': phone_number,
        #'email': email,
        'website': website
    }


url = 'https://www.google.com/maps/'

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get(url)

input_element = driver.find_element(
    By.CSS_SELECTOR,
    'input#searchboxinput'
)

location = ''
business = 'dentist'

input_element.send_keys(f'{location} {business}')
input_element.send_keys(Keys.ENTER)

time.sleep(4)

unique_labels = set()
businesses_list = []

for i in range(20):
    print(i)

    listings = driver.find_elements(
        By.CSS_SELECTOR,
        'a.hfpxzc'
    )

    print(f'Number of listings: {len(listings)}')

    for listing in listings:
        aria_label = listing.get_attribute('aria-label')

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(listing))
        ActionChains(driver).move_to_element(listing).perform()

        if aria_label not in unique_labels:
            unique_labels.add(aria_label)

            panel_data = scrape_panel(listing)
            businesses_list.append(panel_data)
            print(panel_data)

    for j in range(5):
        main_panel = driver.find_element(By.CSS_SELECTOR, 'div[role="main"]')
        ActionChains(driver).send_keys_to_element(main_panel, Keys.DOWN).perform()

    time.sleep(1)

df = pd.DataFrame(businesses_list)
df.to_csv('output.csv', index=False)