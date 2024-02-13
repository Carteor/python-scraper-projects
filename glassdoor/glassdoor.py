import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException


def scrape_details(driver):
    # new tab opens automatically so let's switch to it
    driver.switch_to.window(driver.window_handles[-1])

    # Company Name
    name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div.info'
            )
        )
    )
    name = name_element.text

    # Average review score
    review_score_element = driver.find_element(
        By.CSS_SELECTOR,
        'span.employer-overview__employer-overview-module__employerOverviewRating'
    )
    review_score = review_score_element.text.split()[0]
    # print(f'Company Name: {name}')
    # print(f'Review score: {review_score}')

    # Number of reviews
    review_number_element = driver.find_element(
        By.CSS_SELECTOR,
        'div[data-test="ei-nav-reviews-count"]'
    )
    review_number = review_number_element.text

    company_details_element = driver.find_element(
        By.CSS_SELECTOR,
        'ul[data-test="companyDetails"]'
    )
    li_elements = company_details_element.find_elements(
        By.CSS_SELECTOR,
        'li'
    )
    # Company Size. Interpreting this as number of employees
    company_size = li_elements[2].text

    # Website
    website = li_elements[0].find_element(
        By.CSS_SELECTOR,
        'a'
    ).get_attribute('href')
    # Location
    location = li_elements[1].text

    company_data = {
        'Company Name': name,
        'Review Score': review_score,
        'Review Number': review_number,
        'Company Size': company_size,
        'Website': website,
        'Location': location,
    }

    # After scraping the content tof the tab, close it and switch back to the first tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return company_data


def remove_popup():
    try:
        intercepting_element = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#qual_ol'))
        )
    except TimeoutException:
        intercepting_element = []

    print(f'len: {len(intercepting_element)}')

    if intercepting_element:
        print("There is a intercepting element")
        print(len(intercepting_element))
        answer_buttons = intercepting_element[0].find_elements(
           By.CSS_SELECTOR, 'div.qual_x_close')
        # time.sleep(100)
        answer_buttons[0].click()


url = 'https://www.glassdoor.com/Reviews/index.htm'

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get(url)
print(driver.title)

#input the City, Location
#placeholder for development
city = "New York"
location = "US"

input_element = driver.find_element(
    By.CSS_SELECTOR,
    'input[name="Location"]'
)
input_element.send_keys(f'{city}, {location}')
input_element.send_keys(Keys.ENTER)

listing_elements_by ='div[data-test="employer-card-single"]'
listing_elements = driver.find_elements(
    By.CSS_SELECTOR,
    listing_elements_by
)

for index, listing_element in enumerate(listing_elements):
    try:
        listing_element.click()
    except StaleElementReferenceException:
        print("Caught StaleElementReferenceException")
        listing_element = driver.find_elements(
            By.CSS_SELECTOR,
            listing_elements_by
        )[index]
        listing_element.click()
    except ElementClickInterceptedException:
        print("Caught ElementClickInterceptedException")
        remove_popup()
        listing_element = driver.find_elements(
            By.CSS_SELECTOR,
            listing_elements_by
        )[index]
        listing_element.click()

    print(scrape_details(driver))



