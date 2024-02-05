# Web Scraping Job Description Techspec

## Job Description

I am looking for a skilled web scraping specialist to extract data from a specific website that lists companies. The task involves scraping company names from the main page, navigating to each company's sub-page, and then extracting detailed information about each company.

## Main Page URL

[https://www.bcorporation.net/en-us/find-a-b-corp/?refinement%5Bcountries%5D%5B0%5D=Belgium](https://www.bcorporation.net/en-us/find-a-b-corp/?refinement%5Bcountries%5D%5B0%5D=Belgium)

## Details

- The filter on the main page should be set to "Belgium".
- There are 479 companies listed across approximately 20+ pages.

## Sub-Page Information Extraction

For each company listed on the main page, the script should navigate to the company's sub-page (e.g., [ATIPIK SA](https://www.bcorporation.net/en-us/find-a-b-corp/company/atipik-sa/)) and extract the following details:

- **Name:** ATIPIK SA
- **Headquarters:** Canton of Geneva, Switzerland
- **Certified Since:** January 2024
- **Industry:** Computer programming services
- **Sector:** Service with Minor Environmental Footprint
- **Operates In:** Belgium, France, Switzerland, United States
- **Website:** [www.atipik.ch](http://www.atipik.ch)

## Output Format

The extracted data should be organized and delivered in a structured format such as CSV or Excel.