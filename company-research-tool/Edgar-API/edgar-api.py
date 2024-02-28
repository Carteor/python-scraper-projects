import requests
from lxml import etree
import pandas as pd
from bs4 import BeautifulSoup
import re


def get_company_facts(cik):
    company_facts_url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK0000{cik}.json'

    company_facts = requests.get(company_facts_url, headers=headers).json()

    cf_df = pd.DataFrame(company_facts)

    return (cf_df.columns)


def make_url(cik, row):
    accessionNumber = row['accessionNumber'].replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{row['accessionNumber']}.txt"


def get_data_by_cik(cik):
    edgar_filings = requests.get(f"https://data.sec.gov/submissions/CIK{cik:0>10}.json", headers=headers).json()

    recents = pd.DataFrame(edgar_filings['filings']['recent'])

    latest_filing = recents.iloc[0]

    url = make_url(cik, latest_filing)

    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.content, 'html.parser')

    sec_header = soup.find_all("sec-header")

    txt_content = str(sec_header.pop())
    start_index = txt_content.find("COMPANY DATA:")
    end_index = txt_content.find("FILED BY:")

    company_data_text = txt_content[start_index:end_index]

    company_data = {}

    lines = company_data_text.split("\n")

    current_key = None
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            company_data[key] = value
        elif current_key:
            company_data[current_key] += " " + line.strip()

    return company_data


email="email@email.com"
website="website.com"

headers = {"User-Agent": f"{website} {email}"}

form = "https://www.sec.gov/Archives/edgar/data/320193/000032019322000063/wf-form4_165248105838188.xml"
res = requests.get(form, headers=headers)

try:
    res.raise_for_status()
except requests.HTTPError as err:
    print(err)

# Get json that contains cik and ticker
symbol_to_cik = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
# for i in range(5):
#     print(i, symbol_to_cik[f"{i}"])

# Makes a dictionary pairing the ticker and cik
cik_lookup = dict([(val['ticker'], val['cik_str']) for key, val in symbol_to_cik.items()])

cik = cik_lookup['AAPL']
print(cik)

data = get_data_by_cik(cik)
print(data)
