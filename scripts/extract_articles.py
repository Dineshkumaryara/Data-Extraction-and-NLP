import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load input data
input_file = os.path.join('..', 'data', 'Input.xlsx')
df = pd.read_excel(input_file)

# Create directory for extracted articles if it doesn't exist
extracted_articles_dir = os.path.join('..', 'data', 'extracted_articles')
os.makedirs(extracted_articles_dir, exist_ok=True)

def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1').get_text(strip=True)
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
    
    return title, article_text

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    try:
        title, article_text = extract_article_text(url)
        file_path = os.path.join(extracted_articles_dir, f'{url_id}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n\n{article_text}")
        print(f'Successfully extracted and saved article {url_id}')
    except Exception as e:
        print(f'Failed to extract article {url_id}: {e}')
