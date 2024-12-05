import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the paths
INPUT_FILE = "../data/input.xlsx"
OUTPUT_DIR = "../data/output/extracted_articles/"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load input URLs from Excel
def load_input_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Function to extract article content
def extract_article(url, url_id):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else 'No Title Found'

            # Extract text from <p> tags
            paragraphs = soup.find_all('p')
            article_content = [p.get_text(strip=True) for p in paragraphs]

            # Join all the text content into a single string
            article_text = ' '.join(article_content)

            # Save the article content
            file_path = os.path.join(OUTPUT_DIR, f"{url_id}.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"Title: {title}\n\n")
                file.write(f"Article Text:\n{article_text}")

            print(f"Article {url_id} extracted and saved to {file_path}")

            return title, article_text

        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return None, None

    except Exception as e:
        print(f"Error extracting the article: {str(e)}")
        return None, None

# Main extraction process
def extract_articles():
    df = load_input_data(INPUT_FILE)
    for index, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        print(f"Processing URL_ID {url_id}: {url}")

        title, article_text = extract_article(url, url_id)
        if title and article_text:
            print(f"Extracted Title: {title}")
        else:
            print(f"Skipping article {url_id} due to extraction failure.")

if __name__ == "__main__":
    extract_articles()
