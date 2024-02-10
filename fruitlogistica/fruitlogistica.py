import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import math


def scrape_listing(driver):
    # Scrape the listing popup
    popup_content_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'div.popupContent'
        ))
    )
    print('popup content element located')

    legal_name = WebDriverWait(popup_content_element, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'div[itemprop="legalName"]'
        ))
    )

    street_address = popup_content_element.find_element(
        By.CSS_SELECTOR,
        'div[itemprop="streetAddress"]'
    )

    postal_code = popup_content_element.find_element(
        By.CSS_SELECTOR,
        'span[itemprop="postalCode"]'
    )

    address_locality = popup_content_element.find_element(
        By.CSS_SELECTOR,
        'span[itemprop="addressLocality"]'
    )

    address_country = popup_content_element.find_element(
        By.CSS_SELECTOR,
        'div[itemprop="addressCountry"]'
    )

    a_elements = popup_content_element.find_elements(
        By.CSS_SELECTOR,
        'a'
    )

    hall_stand = a_elements[2].text
    branches = a_elements[3].text
    product_groups = a_elements[4].text

    listing_data = {
        'Legal Name': legal_name.text,
        'Street Address': street_address.text,
        'Postal Code': postal_code.text,
        'Address Locality': address_locality.text,
        'Address Country': address_country.text,
        'Hall | Stand': hall_stand,
        'Branches': branches,
        'Product groups': product_groups,
    }

    close_button = driver.find_element(
        By.CSS_SELECTOR,
        '#onlineGuidePopup > div > div > div.xIcon.EWP5KKC-y-l'
    )
    close_button.click()

    return listing_data


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


unique_link_texts = set()

entries_number_element = driver.find_element(
    By.CSS_SELECTOR,
    '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.EWP5KKC-u-b > div.EWP5KKC-u-e')
entries_number = entries_number_element.text.split()[0]
max_entries_number = entries_number_element.text.split()[2]
print(f'{entries_number} of {max_entries_number}')
pages = math.ceil(int(max_entries_number)/int(entries_number))

for p in range(pages+1):
    print(f'Page: {p}')

    listing_elements = driver.find_elements(
        By.CSS_SELECTOR,
        '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.listContentContainer > div > div.EWP5KKC-e-J > div'
    )
    print(f'len(listing_elements): {len(listing_elements)}')

    for listing_element in listing_elements[len(unique_link_texts):]:
        link_text = listing_element.find_elements(
            By.CSS_SELECTOR,
            'a.gwt-Anchor')[-1].get_attribute('href')
        print(f'link_text: {link_text}')

        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(listing_element))
        ActionChains(driver).move_to_element(listing_element).perform()

        if link_text not in unique_link_texts:
            print('unique element')
            unique_link_texts.add(link_text)

            listing_element.click()
            listing_data = scrape_listing(driver)
            print(listing_data)
        else:
            print('not an unique element, moving along...')


    show_more_button = driver.find_element(
        By.CSS_SELECTOR,
        '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.EWP5KKC-u-b > div.EWP5KKC-u-c'
    )
    show_more_button.click()