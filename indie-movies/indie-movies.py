from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.imdb.com/search/title/?sort=release_date,desc&keywords=independent-film'

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.get(url)

title = driver.title
print(title)

movies = driver.find_elements(
    By.CSS_SELECTOR,
    '#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-a80fc520-0.kpyNQn > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li'
)

print(len(movies))

for movie in movies:
    #title
    title = movie.find_element(By.CSS_SELECTOR,
                               '#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-a80fc520-0.kpyNQn > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div.ipc-metadata-list-summary-item__c > div > div > div.sc-73c670dc-3.cFICGu > div.sc-1e00898e-0.jyXHpt > div > a > h3')
    #description
    #url

driver.quit()