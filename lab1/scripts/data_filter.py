from bs4 import BeautifulSoup
import csv

# Read HTML content from file
with open('../data/raw_data/web_data.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract Market Data
market_cards = soup.select('.MarketCard-container')
market_data = []

for card in market_cards:
    symbol = card.select_one('.MarketCard-symbol').get_text(strip=True)
    position = card.select_one('.MarketCard-stockPosition').get_text(strip=True)
    change_pct = card.select_one('.MarketCard-changesPct').get_text(strip=True)
    market_data.append([symbol, position, change_pct])

# Write market_data.csv
with open('../data/processed_data/market_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol', 'Position', 'Change Percentage'])
    writer.writerows(market_data)

# Extract News Data
news_items = soup.select('.LatestNews-item')
news_data = []

for item in news_items:
    timestamp = item.select_one('.LatestNews-timestamp').get_text(strip=True)
    link_tag = item.select_one('.LatestNews-headline')
    title = link_tag.get_text(strip=True)
    link = link_tag['href']
    news_data.append([timestamp, title, link])

# Write news_data.csv
with open('../data/processed_data/news_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Title', 'Link'])
    writer.writerows(news_data)

print("Data extraction complete. Files saved as 'market_data.csv' and 'news_data.csv'.")
