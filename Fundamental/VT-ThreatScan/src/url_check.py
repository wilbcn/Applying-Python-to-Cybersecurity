import requests
import os
from dotenv import load_dotenv
import json
from collections import Counter
from utils import CSV
from datetime import datetime
import time

# Securely load the API key
load_dotenv()
api_key = os.getenv('VT_API_KEY')

def get_analysis_id():
    """
    Gets the URL via input and makes POST request to VirusTotal in order to get the analysisID
    :return: Returns the analysis id along with the URL submitted via the CLI
    """

    url = "https://www.virustotal.com/api/v3/urls"

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "x-apikey": api_key
    }

    while True:
        print("Please paste the url you wish to scan")
        url_to_check = input("URL: ").strip()

        if not url_to_check:
            print("Input cannot be empty")
            continue

        payload = { "url": url_to_check}
        # POST request NOT get
        print("Getting analysis ID for this URL scan...")
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code} from the API call.")
            return False

        response_data = json.loads(response.text)
        analysis_id = response_data['data']['id']
        return analysis_id, url_to_check


def get_url_analysis():
    """
    Gets the analysisID and url submitted via the CLI to proceed. Makes a GET request to VirusTotal to get the file report
    on the specified URL.
    :return: Returns the file report along with the URL
    """

    analysis_id, url_to_check = get_analysis_id()
    if analysis_id is False:
        return None

    url = "https://www.virustotal.com/api/v3/analyses/"
    complete_url = url + analysis_id

    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    # GET request NOT post
    print(f"Performing URL scan on: '{url_to_check}'...")
    response = requests.get(complete_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} from the API call.")
        return False

    response_data = json.loads(response.text)
    time.sleep(6)  # Allows enough time for the API call.
    return response_data, url_to_check


def review_analysis():
    """
    Works through our file report on the specified URL. Counts instances of particular engine results such as
    Malicious count, Suspicious count, etc.

    We then save this information calling the log_entry method from CSV, to create a permanent log of this search.
    :return: N/A
    """

    url_analysis, url_to_check = get_url_analysis()

    if not url_analysis:
        return False

    analysis_data = url_analysis['data']['attributes']['results']

    # Collect all the category values into a single list
    categories = [engine['category'] for engine in analysis_data.values()]
    results = [engine['result'] for engine in analysis_data.values()]

    # Work out the totals for each category and result per Engine(Anti Virus)
    summary_categories = Counter(categories)
    summary_results = Counter(results)

    info_to_log = {}

    print("\n--- Analysis Summary by Category ---")
    for category, count in summary_categories.items():
        info_to_log[category] = count
        print(f"{category.title()}: {count}")

    print("\n--- Analysis Summary by Result ---")
    for result, count in summary_results.items():
        info_to_log[result] = count
        print(f"{result.title()}: {count}")

    # Log the hash search
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    CSV.log_entry(date, "URL", url_to_check, info_to_log)
