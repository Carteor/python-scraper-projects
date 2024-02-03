from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import math
import time
import pandas as pd

def scrape_details(driver):
    try:
        element_to_scroll = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                By.CSS_SELECTOR,
                'div[data-testid="storyline-header"]'
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        time.sleep(1)
    except TimeoutException:
        print("Project in development")

    #  Genres
    try:
        genres_ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[4]/div[2]/ul[2]/li[1]/div/ul')
            )
        )
        genres = genres_ul_element.text
    except TimeoutException:
        genres = 'No genres available'

    #  Release Year
    try:
        release_year_element = driver.find_element(By.XPATH,
                                                   '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a')
        release_year = release_year_element.text
    except NoSuchElementException:
        release_year = 'No release year available'

    # print(release_year)

    #  Ratings
    try:
        ratings_element = driver.find_element(
            By.CSS_SELECTOR,
            'div[data-testid="hero-rating-bar__aggregate-rating__score"]')
        ratings = ratings_element.text.replace('\n', '')
    except NoSuchElementException:
        ratings = 'No ratings available'
    # print(f'ratings: \'{ratings.strip()}\'')

    #  Box Office
    try:
        box_office_element = driver.find_element(By.XPATH,
                                                 '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[4]/div/ul/li/span')
        box_office = box_office_element.text
    except NoSuchElementException:
        box_office = 'No box office available'
    # print(box_office)

    # #  YouTube Trailer Link
    try:
        trailer_link_element = driver.find_element(By.XPATH,
                                                   '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[2]/div[2]/a[2]')
        trailer_link = trailer_link_element.get_attribute('href')
    except NoSuchElementException:
        trailer_link = 'No trailer link available'
    # print(trailer_link)

    return {
        'genres:': genres,
        'release_year': release_year,
        'ratings': ratings,
        'box_office': box_office,
        'trailer_link': trailer_link
    }


def scrape_page(driver):
    movies_element = driver.find_elements(
        By.CSS_SELECTOR,
        '#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-a80fc520-0.kpyNQn > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li'
    )

    print(len(movies_element))

    movies_list = []
    # columns = ['title', 'description', 'url', 'genres:', 'release_year', 'ratings', 'box_office', 'trailer_link']
    # df = pd.DataFrame(columns=columns)

    for movie in movies_element:
        title = movie.find_element(By.CSS_SELECTOR,
                                   'h3.ipc-title__text').text
        try:
            description = movie.find_element(By.CSS_SELECTOR,
                                             'div.ipc-html-content-inner-div').text
        except NoSuchElementException:
            description = 'Not available'

        url = movie.find_element(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper').get_attribute('href')

        x = {
            'title': title,
            'description': description,
            'url': url}

        driver.execute_script("window.open('{}', '_blank');".format(url))
        driver.switch_to.window(driver.window_handles[-1])

        y = scrape_details(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        z = {**x, **y}

        movies_list.append(z)
        print(z)

        df = pd.DataFrame(movies_list)
        df.to_csv('movies.csv', mode='w', header=True, index=False)

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
# url = 'https://www.imdb.com/title/tt5765844/'
driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get(url)

title = driver.title
print(title)

page_number_element = driver.find_element(By.XPATH,
                                          '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[1]')
page_number = math.ceil(int(page_number_element.text.split()[2].replace(',', '')) / 50)
print(page_number)

movie_list = scrape_page(driver)
print(movie_list)

driver.quit()