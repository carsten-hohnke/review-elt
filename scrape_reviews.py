# Import libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

# Set up headless browser
options = Options()
options.headless = False

# Set up driver
driver = webdriver.Chrome(options=options)

# Set up URL
url = 'https://www.trustpilot.com/review/ourbranch.com'

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
    #get the button to click

    time.sleep(5)
    
    # Extract HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract reviews
    reviews = soup.find_all('article', {'class': 'paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv styles_reviewCard__hcAvl'})
    for review in reviews:
        # Extract review text
        review_text = review.find('p', {'class': 'typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn'}).text.strip()
        review_text = review_text.replace(',', '')
        
        # Extract rating. Note: rating is in the form of stars, so we need to extract the alt text from the image tag following the div tag of class 'star-rating_starRating__4rrcf star-rating_medium__iN6Ty'
        rating = review.find('div', {'class': 'star-rating_starRating__4rrcf star-rating_medium__iN6Ty'}).find('img').get('alt').strip()
        rating_strip = len("Rated ")
        rating = rating[rating_strip:rating_strip+1]
        
        # Extract date
        date = review.find('p', {'class': 'typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn'}).text.strip()
        date_strip = len("Date of experience: ")
        date = date[date_strip:]
        
        # Write to CSV file
        row = [review_text, rating, date]
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    
    # Check if there are more reviews
    load_more_button = driver.find_element(By.NAME, 'pagination-button-next')
    if load_more_button:
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(5)
    else:
        break

# Close driver
print('Scraping complete!')
driver.quit()