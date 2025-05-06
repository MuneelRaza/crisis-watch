from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def save_data_to_json(data: list, filename: str):
    reliefweb_data_path = os.getenv('RELIEFWEB_DATA_FILE_PATH')

    full_path = '../' + reliefweb_data_path + '/' + filename

    print(full_path)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def resolve_url(raw_url_article):
    try:
        response = requests.get(raw_url_article['url'], allow_redirects=True)

        if response.status_code == 200:
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