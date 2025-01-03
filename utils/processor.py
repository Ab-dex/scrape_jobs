import requests
from urllib.parse import urlparse
from time import sleep

def process_links(formatted_data, headers):
    """
    Processes job links to fetch detailed job information.
    """
    all_job_details = []
    for link in formatted_data:
        try:
            parsed_url = urlparse(link)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            subdomain_name = parsed_url.netloc.split(".")[0]
            api_url = f"{base_url}/wday/cxs/{subdomain_name}/{link.split('/')[-1]}/jobs"
            response = requests.post(api_url, headers=headers, json={})
            if response.status_code == 200:
                data = response.json()
                for job in data.get("jobPostings", []):
                    job_details = {
                        "title": job.get("title"),
                        "location": job.get("locationsText"),
                        "postedOn": job.get("postedOn")
                    }
                    job_full_url = api_url[:-1] + "/" + job["externalPath"].split("/")[-1]
                    job_response = requests.get(job_full_url, headers=headers)
                    if job_response.status_code == 200:
                        job_data = job_response.json()
                        company_name = job_data.get("hiringOrganization", {}).get("name", "N/A")
                        job_title = job_data.get("jobPostingInfo", {}).get("title", "N/A")
                        job_description = job_data.get("jobPostingInfo", {}).get("jobDescription", "N/A")
                        job_details.update({
                            "companyName": company_name,
                            "jobTitle": job_title,
                            "jobDescription": job_description
                        })
                    all_job_details.append(job_details)
            else:
                print(f"Error: Received {response.status_code} from {link}")
            sleep(2)
        except Exception as e:
            print(f"Error processing link {link}: {e}")
            continue
    return all_job_details
