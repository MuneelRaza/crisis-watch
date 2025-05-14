from dotenv import load_dotenv
load_dotenv()

import sys
import os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path)) 

if project_root not in sys.path:
    sys.path.insert(0, project_root)


import json

from utils.utils import save_data_to_json, get_report_details, parse_bullet_points
from utils.import_llm import llm
from prompts import summarization_prompt



filename = 'updated_reliefweb_reports_results.json'

reliefweb_data_path = os.getenv('RELIEFWEB_DATA_FILE_PATH')
full_path = '../' + reliefweb_data_path + '/' + filename

with open(full_path, "r") as f:
    reports_results = json.load(f)

# print(type(reports_results))
# print(reports_results[5])


def add_summary(report_dict):
    detail_url = report_dict['resolved_url']
    report_result = get_report_details(detail_url)

    if report_result:
        formatted_prompt = summarization_prompt.format(content=report_result)
        summary = llm.invoke([formatted_prompt])
        report_dict['summary'] = summary.content
        return report_dict
    else:
        print("Content not found.")
        report_dict['summary'] = ""
        return report_dict


updated_reports_results = list(map(add_summary, reports_results))

updated_filename = 'updated_reliefweb_reports_results_v1.json'
save_data_to_json(updated_reports_results, updated_filename)

