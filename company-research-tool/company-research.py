import json
import requests


API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()


def load_keywords():
    keywords_file = "keywords.json"
    with open(keywords_file, 'r', encoding='utf-8') as keywordsfile:
        keywords_data = json.load(keywordsfile)
        return dict(keywords_data)


def load_companies():
    company_file = "companies.json"
    with open(company_file, 'r', encoding='utf-8') as comp_file:
        company_data = json.load(comp_file)
        return company_data['companies']


def search(search_query):
    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'dateRestrict': '2023-08-01',
        'lr': 'lang_en'
    }

    response = requests.get(url, params=params)
    results = response.json()

    if 'items' in results:
        items = results['items']
        results = []
        for index, item in enumerate(items):
            data = {'title': item['title'], 'link': item['link']}
            results.append(data)

    return results


keywords = load_keywords()
companies = load_companies()

data_dict = {}
for company in companies:
    print("Company: ", company)
    company_data = {}

    for category, value_list in keywords.items():
        print("Category: ", category)
        category_data = []

        for value in value_list:
            data = search(f'{company} {value}')
            print(data)

            category_data.append(data)

        company_data[category] = category_data
    data_dict[company] = company_data

with open('result.json', 'w') as output:
    json.dump(data_dict, output, indent=4)
