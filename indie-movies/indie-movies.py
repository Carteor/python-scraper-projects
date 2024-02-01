from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import math
import time


def scrape_page(driver):
    movies_element = driver.find_elements(
        By.CSS_SELECTOR,
        '#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-a80fc520-0.kpyNQn > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li'
    )

    print(len(movies_element))

    movies_list = []
    for movie in movies_element:
        title = movie.find_element(By.CSS_SELECTOR,
                                   'h3.ipc-title__text').text
        try:
            description = movie.find_element(By.CSS_SELECTOR,
                                             'div.ipc-html-content-inner-div').text
        except NoSuchElementException:
            description = 'Not available'

        url = movie.find_element(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper').get_attribute('href')

        movies_list.append({'title': title,
                            'description': description,
                            'url': url})

    return movies_list


# TODO: implement dynamic loading of required number of pages
def load_pages(page_number, driver):
    print("load_pages()")
    for i in range(2):
        see_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              'button.ipc-see-more__button'))
        )

        ActionChains(driver).move_to_element(see_more_button).perform()

        time.sleep(10)
        # see_more_button.click()


url = 'https://www.imdb.com/search/title/?sort=release_date,desc&keywords=independent-film'

driver = webdriver.Chrome()
driver.implicitly_wait(1)
driver.get(url)

title = driver.title
print(title)

page_number_element = driver.find_element(By.XPATH,
                                          '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[1]')
page_number = math.ceil(int(page_number_element.text.split()[2].replace(',', '')) / 50)
print(page_number)

# load_pages(2, driver)

movie_list = scrape_page(driver)
print(movie_list)

# TODO: implement
#  Genres
# data-testid="storyline-genres"
#  Release Year
release_year = driver.find_element(By.XPATH,
                                   '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a')
#  Ratings
ratings = driver.find_element(By.XPATH,
                              '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[1]/span[1]')
#  Box Office
box_office = driver.find_element(By.XPATH,
                                 '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[4]/div/ul/li/span')
#  YouTube Trailer Link
trailer_link = driver.find_element(By.XPATH,
                                   '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[2]/div[2]/a[2]')

driver.quit()
