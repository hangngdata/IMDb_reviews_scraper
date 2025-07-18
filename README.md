## Movie Data & IMDb User Reviews Scrapers

Ever wondered what people said about a movie before you watched it? Or want to turn online reactions into a predictor of box office success? This scraper’s got you covered!

Leveraging the power of BeautifulSoup, Selenium, and IMDb packages, this tool automates the process of collecting movie data and IMDb user reviews together with ratings, review text, and reactions to the review. A starting point for your project, whether it is to build a dataset or to predict the success of a blockbuster.

## Usage

- Step 1: Scrape movie data from [The Number] (//the-numbers.com/market/2025/top-grossing-movies) (eg. top-grossing movies)
- Step 2: Clean and prepare the movie dataset
- Step 3: Find IMDb review URLs for each movie 
- Step 4: Scrape user reviews, ratings, and reactions from IMDb

## Repository organization

- ``example_notebook``: A small walkthrough notebook showing how to use the scraper step-by-step
- ``src``: All scraping and cleaning scripts
- ``data``: Output dataframes of the scraped movie data and user reviews

## Suggested applications

- Perform sentiment analysis or topic modeling on pre- vs post-release reviews
- Use review embeddings + movie features to predict box office sales
- Create word clouds, explore genre-based review patterns, or detect review biases
- Fine-tune LLMs on curated movie review datasets
- Analyze audience reactions over time for marketing or journalism

Have fun scraping! 😎🍿🕵️‍♂️🎬