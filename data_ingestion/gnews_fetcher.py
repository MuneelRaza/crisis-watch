from dotenv import load_dotenv
load_dotenv()

import sys
import os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path)) 

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import json
import urllib.request
import os

from utils.utils import save_data_to_json



def fetch_gnews_news(category):
    apikey = os.getenv('GNEWS_API_KEY')
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"


    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

    return articles



gnews_results = fetch_gnews_news("crisis")
print(type(gnews_results))

filename = 'gnews_api_results.json'
save_data_to_json(gnews_results, filename)


