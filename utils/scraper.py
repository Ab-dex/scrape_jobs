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
    for i in range(len(data)):
        if "/job" in data[i]:
            url_home = data[i].split("/job")[0]
        elif "/detail" in data[i]:
            url_home = data[i].split("/detail")[0]
        else:
            url_home = data[i]
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
