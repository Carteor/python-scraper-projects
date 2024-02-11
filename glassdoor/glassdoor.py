import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def scrape_details(driver):
    # new tab opens automatically so let's switch to it
    driver.switch_to.window(driver.window_handles[-1])

    # Company Name
    name_element = driver.find_element(
        By.CSS_SELECTOR,
        'div.info'
    )
    name = name_element.text

    # Average review score
    review_score_element = driver.find_element(
        By.CSS_SELECTOR,
        'span.employer-overview__employer-overview-module__employerOverviewRating'
    )
    review_score = review_score_element.text.split()[0]
    print(f'Company Name: {name}')
    print(f'Review score: {review_score}')

    # Number of reviews
    # Data is absent on the page

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
        'Review score': review_score,
        'Company Size': company_size,
        'Website': website,
        'Location': location,
    }

    # After scraping the conten tof the tab, close it and switch back to the first tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return company_data


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

listing_element = driver.find_element(
    By.CSS_SELECTOR,
    'div[data-test="employer-card-single"]'
)
listing_element.click()

print(scrape_details(driver))

time.sleep(5)