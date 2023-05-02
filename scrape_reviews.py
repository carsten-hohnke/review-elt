# Import libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

# Set up headless browser
options = Options()
options.headless = True

# Set up driver
driver = webdriver.Chrome(options=options)

# Set up URL
url = 'https://www.trustpilot.com/review/branchapp.com'

# Set up CSV file
filename = 'branch_reviews.csv'
header = ['review', 'rating', 'date']
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# Scrape reviews
while True:
    # Get page
    driver.get(url)
    time.sleep(5)
    
    # Extract HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract reviews
    reviews = soup.find_all('div', {'class': 'review__content'})
    for review in reviews:
        # Extract review text
        review_text = review.find('p', {'class': 'review-content__text'}).text.strip()
        
        # Extract rating
        rating = review.find('img', {'class': 'star-rating__star'}).get('alt').strip()
        
        # Extract date
        date = review.find('div', {'class': 'review-content-header__dates'}).find_all('div')[1].text.strip()
        
        # Write to CSV file
        row = [review_text, rating, date]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    
    # Check if there are more reviews
    load_more_button = driver.find_element_by_xpath('//button[@data-qa="reviews-show-more-button"]')
    if load_more_button:
        load_more_button.click()
        time.sleep(5)
    else:
        break

# Close driver
print('Scraping complete!')
driver.quit()