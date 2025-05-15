from dotenv import load_dotenv
load_dotenv()

import sys
import os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path)) 

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from newspaper import Article



def save_data_to_json(data: list, filename: str):
    reliefweb_data_path = os.getenv('RELIEFWEB_DATA_FILE_PATH')

    full_path = reliefweb_data_path + '/' + filename

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def resolve_url(raw_url_article):
    try:
        response = requests.get(raw_url_article['url'], allow_redirects=True)

        if response.status_code == 200:
            print("Actual URL: ", raw_url_article['url'])
            print("Resolved URL: ", response.url)
            raw_url_article['resolved_url'] = response.url

        else:
            raw_url_article['resolved_url'] = None
    
    except Exception as e:
        raw_url_article['resolved_url'] = None
    
    return raw_url_article
    


def get_pdf_url(page_url):
    try:
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        attachment_section = soup.select_one('section.rw-attachment--report.rw-attachment.rw-file-list')
        if not attachment_section:
            print("Attachment section not found.")
            return None
        
        pdf_tag = attachment_section.select_one('ul li a[href$=".pdf"]')
        if not pdf_tag:
            print("PDF link not found in attachment section.")
            return None
        
        return urljoin(page_url, pdf_tag['href'])

    except Exception as e:
        print(f"Error: {e}")
        return None
    


def download_url(pdf_url, save_path):
    try:
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()       

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"PDF downloaded successfully: {save_path}")
        return True
    
    except Exception as e:
        print(f"Failed to download PDF: {e}")
        return False
    


def get_report_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    content_div = soup.find('div', class_='rw-article__content')

    if content_div:
        return content_div.get_text(strip=True)
    else:
        return None
    

def parse_bullet_points(text):
    lines = text.strip().split('\n')
    bullets = [line.lstrip('- ').strip() for line in lines if line.strip().startswith('-')]
    return bullets

def remove_asterisks(text: str) -> str:
    cleaned_lines = []
    for line in text.strip().split('\n'):
        cleaned_line = line.lstrip('*-• ').strip()
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)



def get_title_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch article: {response.status_code} - {url}")

    article = Article(url)
    article.set_html(response.text)
    article.parse()

    return article.title, article.text
    


def get_gnews_articles():
    filename = 'gnews_data.json'

    reliefweb_data_path = os.getenv('RELIEFWEB_DATA_FILE_PATH')
    full_path = reliefweb_data_path + '/' + filename


    with open(full_path, "r") as f:
        reports_results = json.load(f)

    return reports_results