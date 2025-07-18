import re
import time
from datetime import datetime, timedelta

import pandas as pd
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def scrape_reviews_per_movie(driver, movie_id, movie_title, release_date, review_url, is_first_iteration):

    print(f'\nScraping reviews for movie: {movie_title}...')
    driver.get(review_url)
    time.sleep(2)

    # Accept Cookie if first time opening browser
    if is_first_iteration:
        try:
            cookies_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div[2]/div/button[2]')
            cookies_button.click()
            time.sleep(2)
        except:
            print('No cookie button found.')
    
    # Click 'All' to expand reviews
    try:
        all_button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[3]/div/span[2]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_button)
        time.sleep(1)
        all_button.click()
        time.sleep(1)
    except:
        print("No 'All' button found.")
    
    # Define cutoff date (one week after movie release)
    cutoff_date = release_date + timedelta(days=7)
    
    # Initialize review data per movie
    reviews_per_movie = []

    # Find all reviews for the movie
    review_articles = driver.find_elements(By.CLASS_NAME, 'user-review-item')

    # Iterate each review found
    for idx, review in enumerate(review_articles, 1):
        print(f'***Scraping review {idx}...***')
        try:
            
            # Review date
            review_date_el = review.find_elements(By.CLASS_NAME, 'review-date')
            review_date_str = review_date_el[0].text if review_date_el else "N/A"

            try:
                review_date = datetime.strptime(review_date_str, '%b %d, %Y')
                print(f"Parsed review date: {review_date.strftime('%Y/%m/%d')} | Cutoff: {cutoff_date.strftime('%Y/%m/%d')}")
                if review_date > cutoff_date:
                    print(f"Review {idx} is after the cutoff ({cutoff_date.date()}), stopping.")
                    break
                review_date = review_date.strftime("%Y/%m/%d")
            except Exception as e:
                print(f"Could not parse review date '{review_date_str}' for review {idx}: {e}")
                continue
                
            # Title
            title_el = review.find_elements(By.CLASS_NAME, 'ipc-title__text')
            title = title_el[0].text if title_el else "N/A"

            # Author
            author_el = review.find_elements(By.CSS_SELECTOR, '[data-testid="author-link"]')
            author = author_el[0].text if author_el else "N/A"

            # Rating
            rating_el = review.find_elements(By.CLASS_NAME, 'ipc-rating-star--rating')
            rating = rating_el[0].text if rating_el else "0"

            # Helpful counts
            helpful_count_up_el = review.find_elements(By.CLASS_NAME, 'ipc-voting__label__count--up')
            helpful_count_up = helpful_count_up_el[0].text if helpful_count_up_el else "0"

            helpful_count_down_el = review.find_elements(By.CLASS_NAME, 'ipc-voting__label__count--down')
            helpful_count_down = helpful_count_down_el[0].text if helpful_count_down_el else "0"

            # Spoiler button
            spoiler_btn = review.find_elements(By.CLASS_NAME, 'review-spoiler-button')
            if spoiler_btn:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", spoiler_btn[0])
                time.sleep(0.3)
                spoiler_btn[0].click()
                # print('Spoiler button found.')
                time.sleep(0.5)

            # Read more button
            read_more_btn = review.find_elements(By.CLASS_NAME, "ipc-overflowText-overlay")
            if read_more_btn:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", read_more_btn[0])
                time.sleep(0.3)
                read_more_btn[0].click()
                # print('Read more button found.')
                time.sleep(0.5)

            # Content
            content_el = review.find_elements(By.CLASS_NAME, 'ipc-html-content-inner-div')
            content = content_el[0].text if content_el else "N/A"

            # Store result
            reviews_per_movie.append({
                'movie_id': movie_id,
                'movie_title': movie_title,
                'release_date': release_date.strftime("%Y/%m/%d"),
                'review_title': title,
                'review_author': author,
                'review_date': review_date,
                'rating': rating,
                'review_content': content,
                'helpful_count_up': helpful_count_up,
                'helpful_count_down': helpful_count_down
            })

            print(f"Scraped review {idx}")

        except Exception as e:
            print(f"Error scraping review {idx}: {e}")
    return reviews_per_movie


def scrape_reviews_all_movies(movies_df):
    driver = webdriver.Chrome()
    all_reviews = []
    is_first_iteration = True

    total_num_movies = movies_df.shape[0]

    for index, row in movies_df.iterrows():
        print(f'\n=========Processing movie: {index+1}/{total_num_movies} ==========')
        movie_id = row['movie_id']
        movie_title = row['movie_title']
        release_date = datetime.strptime(row['release_date'], "%Y/%m/%d")
        review_url = row['imdb_review_url']

        reviews = scrape_reviews_per_movie(driver, movie_id, movie_title, release_date, review_url, is_first_iteration)
        is_first_iteration = False

        all_reviews.extend(reviews)

    driver.quit()

    all_reviews_df = pd.DataFrame(all_reviews)

    # save_path = "../data/all_reviews.csv"
    # all_reviews_df.to_csv(save_path, index=False)

    return all_reviews_df