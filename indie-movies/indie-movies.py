from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import math
import time


def scrape_details(driver, movie_url='https://www.imdb.com/title/tt0335345/'):
    driver.get(movie_url)

    photos_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             'section[data-testid="Photos"]')
        )
    )
    driver.execute_script("arguments[0].scrollIntoView();",
                          photos_section)

    # Scroll to Storyline element to start loading remaining data
    storyline_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-a83bf66d-1.gYStnb.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(25) > div.ipc-title.ipc-title--base.ipc-title--section-title.ipc-title--on-textPrimary > div > hgroup > h3 > span')
        )
    )


    # Use Javascript to avoid bugs
    driver.execute_script("arguments[0].scrollIntoView();",
                          storyline_element)
    # Take a break to load the element
    time.sleep(5)

    #  Genres
    genres_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[6]/div[2]/ul[2]/li[2]/div/ul')
        )
    )
    genres = genres_element.text
    # print(genres)

    #  Release Year
    release_year_element = driver.find_element(By.XPATH,
                                               '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a')
    release_year = release_year_element.text
    # print(release_year)

    #  Ratings
    ratings_element = driver.find_element(
        By.CSS_SELECTOR,
        'div[data-testid="hero-rating-bar__aggregate-rating__score"]')
    ratings = ratings_element.text.replace('\n', '')
    # print(f'ratings: \'{ratings.strip()}\'')

    #  Box Office
    box_office_element = driver.find_element(By.XPATH,
                                             '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[4]/div/ul/li/span')
    box_office = box_office_element.text
    # print(box_office)

    # #  YouTube Trailer Link
    trailer_link_element = driver.find_element(By.XPATH,
                                               '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[2]/div[2]/a[2]')
    trailer_link = trailer_link_element.get_attribute('href')
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

        y = scrape_details(driver, url)

        z = {**x, **y}

        movies_list.append(z)

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
driver.implicitly_wait(10)

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

driver.quit()