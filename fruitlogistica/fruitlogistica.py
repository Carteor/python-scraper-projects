import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


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

    print(listing_data)
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

listing_element = driver.find_element(
    By.CSS_SELECTOR,
    '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.listContentContainer > div > div.EWP5KKC-e-J > div:nth-child(1)'
)
listing_element.click()

print(scrape_listing(driver))

