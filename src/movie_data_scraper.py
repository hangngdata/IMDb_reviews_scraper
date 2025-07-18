from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_movie_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    df = pd.read_html(str(table))[0]

    df = df.iloc[:-2]

    return df

def clean_movie_data(df):
    df = df.reset_index(drop=True)
    df['movie_id'] = df.index
    
    renamed_map = {
        'Rank': 'rank',
        'Movie': 'movie_title',
        'Release Date': 'release_date',
        'Distributor': 'distributor',
        'Genre': 'genre',
        'Tickets Sold': 'tickets_sold'
    }
    gross_col = next((col for col in df.columns if col.endswith('Gross')), None)
    if gross_col:
        year = gross_col.split()[0]
        new_col_name = f'gross_{year}'
        df = df.rename(columns={gross_col: new_col_name})

    df = df.rename(columns=renamed_map)

    df['release_date'] = pd.to_datetime(df['release_date'], format='%b %d, %Y', errors='coerce')
    df['release_year'] = df['release_date'].dt.year

    df['release_date'] = df['release_date'].dt.strftime('%Y/%m/%d')

    df[f'gross_{year}'] = df[f'gross_{year}'].astype(str).str.replace(r'[\$,]', '', regex=True).astype(float)

    df['tickets_sold'] = df['tickets_sold'].astype(str).str.replace(',', '').astype(float)

    cols = ['movie_id'] + [col for col in df.columns if col != 'movie_id']
    df = df[cols]

    return df