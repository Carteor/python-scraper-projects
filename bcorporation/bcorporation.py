import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import pandas as pd


def scrape_details(driver):
    panel_element = driver.find_element(By.XPATH,
                                        '//*[@id="gatsby-focus-wrapper"]/div/main/div[1]/div[3]/div[2]')

    p_elements = panel_element.find_elements(By.TAG_NAME, 'p')
    # for index, p_element in enumerate(p_elements):
    #     print(f'{index}: {p_element.text}')

    a_element = panel_element.find_element(By.TAG_NAME, 'a')
    # print(f'{a_element.get_attribute('href')}')

    headquarters = p_elements[0].text
    certified_since = p_elements[1].text
    industry = p_elements[2].text
    sector = p_elements[3].text
    operates_in = ' '.join([element.text for element in p_elements[4:]])
    website = a_element.get_attribute('href')

    # return {
    #     'headquarters': headquarters,
    #     'certified_since': certified_since,
    #     'industry': industry,
    #     'sector': sector,
    #     'operates_in': operates_in,
    #     'website': website
    # }
    return headquarters, certified_since, industry, sector, operates_in, website


def scrape_page(driver):
    items = driver.find_elements(By.CSS_SELECTOR, 'li[class="ais-Hits-item"]')

    corporation_list = []

    for item in items:
        # Name
        title = item.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name-desktop"]').text

        link = item.find_element(By.CSS_SELECTOR, 'a[data-testid="profile-link"]').get_attribute('href')
        print(title)
        print(link)

        driver.execute_script("window.open('{}', '_blank');".format(link))
        driver.switch_to.window(driver.window_handles[-1])

        headquarters, certified_since, industry, sector, operates_in, website = scrape_details(driver)

        corporation = {
            'Name': title,
            'Headquarters': headquarters,
            'Certified Since': certified_since,
            'Industry': industry,
            'Sector': sector,
            'Operates In': operates_in,
            'Website': website
        }

        corporation_list.append(corporation)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return corporation_list

driver = webdriver.Chrome()
driver.implicitly_wait(10)

url = 'https://www.bcorporation.net/en-us/find-a-b-corp/?refinement%5Bcountries%5D%5B0%5D=Belgium'
# url = 'https://www.bcorporation.net/en-us/find-a-b-corp/company/atipik-sa/'
driver.get(url)

number_element = driver.find_element(
    By.CSS_SELECTOR,
    '#gatsby-focus-wrapper > div > div > main > div.bg-surface-variant-light.flex.flex-col.py-8.px-6 > div > div.text-center.text-fiber-neutral-500.mt-10'
)
number_of_pages = int(number_element.text.split()[-1])

corporation_list = []
for i in range(1, number_of_pages+1):
    pagination_url = f'&page={i}'
    driver.get(url+pagination_url)
    corporations = scrape_page(driver)
    corporation_list.extend(corporations)

    df = pd.DataFrame(corporation_list)
    df.to_csv('bcorporations.csv', mode='w', index=False)
