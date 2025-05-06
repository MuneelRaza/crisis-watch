from dotenv import load_dotenv
load_dotenv()

import sys
import os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path)) 

if project_root not in sys.path:
    sys.path.insert(0, project_root)


import requests
import json
from datetime import datetime, timedelta

from utils.utils import save_data_to_json, resolve_url, get_pdf_url, download_url



def fetch_reliefweb_articles(query="conflict", limit=10):
    url = "https://api.reliefweb.int/v1/reports"
    params = {
        "appname": "crisiswatch",
        "profile": "list"
    }

    payload = {
        "query": {
            "value": query,
            "operator": "AND"
        },
        "limit": limit,
        "sort": ["date:desc"]
    }

    response = requests.post(url, params=params, json=payload)
    data = response.json()
    articles = []

    for item in data['data']:
        fields = item['fields']
        articles.append({
            "source": "ReliefWeb",
            "title": fields.get("title"),
            "date": fields.get("date", {}).get("created"),
            "url": fields.get("url"),
            "body": fields.get("body-html", ""),
            "countries": [c.get("name") for c in fields.get("country", [])],
            "tags": [d.get("name") for d in fields.get("theme", [])],
        })

    return articles



# reliefweb_results = fetch_reliefweb_articles()
# print(type(reliefweb_results))

filename = 'reliefweb_reports_results.json'
# save_data_to_json(reliefweb_results, filename)


# reliefweb_data_path = os.getenv('RELIEFWEB_DATA_FILE_PATH')
# full_path = '../' + reliefweb_data_path + '/' + filename

# with open(full_path, "r") as f:
#     reports_results = json.load(f)

# print(type(reports_results))

# updated_reports_results = list(map(resolve_url, reports_results))

updated_filename = 'updated_reliefweb_reports_results.json'
# save_data_to_json(updated_reports_results, updated_filename)



reliefweb_data_path = os.getenv('RELIEFWEB_DATA_FILE_PATH')
full_path = '../' + reliefweb_data_path + '/' + updated_filename

with open(full_path, "r") as f:
    resolved_url_articles = json.load(f)


# pdf saving path
reports_dir_path = os.getenv('RELIEFWEB_PDF_REPORTS_DIR_PATH')
full_path = '../' + reports_dir_path + '/'


for article in resolved_url_articles:
    pdf_url = get_pdf_url(article['resolved_url'])
    print(pdf_url)
    if pdf_url:
        filename = os.path.basename(pdf_url.split("?")[0])  # remove query params from filename
        download_url(pdf_url, save_path=filename)
        
