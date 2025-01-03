import os
from dotenv import load_dotenv
import pandas as pd
from utils.scraper import scrape_google_results, extract_unique_links
from utils.processor import process_links

# Load .env file
load_dotenv()

# Environment variables
user_agent = os.getenv("AGENT")
headers = {"User-Agent": user_agent}

# Parameters for Google search
params = {
    "q": "engineer site:*.myworkdayjobs.com",
    "hl": "en",
    "gl": "US",
    "start": "0",
}

# Step 1: Scrape Google search results
print("Scraping Google search results...")
raw_data = scrape_google_results(params, headers)

# Step 2: Extract unique job links
print("Extracting unique job links...")
unique_links = extract_unique_links(raw_data)

# Step 3: Process job links to fetch details
print("Processing job links...")
job_details = process_links(unique_links, headers)

# Step 4: Save to CSV
if job_details:
    df = pd.DataFrame(job_details)
    df.to_csv("job_details.csv", index=False)
    print("Job details have been saved to 'job_details.csv'.")
else:
    print("No job details found.")
