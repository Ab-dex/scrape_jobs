from bs4 import BeautifulSoup
from requests import get
from time import sleep
import pandas as pd
from urllib.parse import urlparse

def extract_unique_links(data):
    """
    Extracts unique base URLs from a list of links.
    """
    unique_links = set()

    for url in data:
        

        # Remove query strings and rebuild the URL without the query part
        parsed_url = urlparse(url)
        sanitized_url = urlunparse(parsed_url._replace(query=""))

        # Extract the base URL based on specific path segments
        if "/job" in sanitized_url:
            url_home = sanitized_url.split("/job")[0]
        elif "/detail" in sanitized_url:
            url_home = sanitized_url.split("/detail")[0]
        else:
            url_home = sanitized_url

        # Add the sanitized URL to the set
        unique_links.add(url_home)

    return unique_links

def scrape_google_results(params, headers):
    """
    Scrapes Google search results for job postings.
    """
    data = []
    page_num = 0
    while True:
        params["start"] = page_num
        response = get("https://www.google.com/search", params=params, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".tF2Cxc")
        if not results:
            break
        for result in results:
            link = result.select_one("a")["href"]
            data.append(link)
        if not soup.select_one(".d6cvqb a[id$='pnnext'] .oeN89d"):
            break
        page_num += 10
        sleep(2)
    return data
