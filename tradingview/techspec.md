### Project: Web Scraping Data from Tradingview

**Description:**
The task involves scraping data from the website Tradingview and organizing it into a CSV or Google Sheets format. The data will be related to various trading strategies available on the platform.

**Deliverables:**
The deliverable will be a CSV file or Google Sheets document containing the scraped data. This document should be downloadable or accessible for further analysis.

**Instructions:**
1. **Account Setup:**
   - Create a free account on Tradingview or use provided credentials.

2. **Data Collection:**
   - Navigate to the charts section and select "BTCUSD" on the main page.
   - Change the time frame from "1 day" to "30 minutes."
   - Click on the "Indicators" button and search for "strategy."
   - Scroll down to the "Community Scripts" section.
   - Click on a strategy with a chart icon.
   
3. **Configuration:**
   - Click on the gear icon next to the strategy name.
   - Set the order size to 1 contract and commission to $50 per contract.
   - Click "Ok" to confirm.

4. **Data Extraction:**
   - Go to the strategy tester at the bottom of the page.
   - Copy the fields into a CSV or Google Sheets file.
     - Fields include: "Strategy Link", "Net Profit", "Net Profit Percentage", "Total Closed Trades", "Percent Profitable", etc.

5. **Iteration:**
   - Close the strategy and proceed to the next one.
   - Continue until reaching strategies with less than 300 votes.