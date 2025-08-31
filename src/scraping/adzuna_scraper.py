import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

def scrape_adzuna(query="data scientist", location="in", pages=3, results_per_page=20, delay=1):
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError("Please set ADZUNA_APP_ID and ADZUNA_APP_KEY in your .env file")
    jobs = []

    for page in range(1, pages+1):
        url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/{page}"
        print(f"Fetching: {url}")
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": results_per_page,
            "what": query,
            "content-type": "application/json"
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            break
        data = response.json()
        results = data.get("results", [])
        if not results:
            break

        for job in results:
            title = job.get("title")
            if not title or len(title)<3:
                continue

            company = job.get("company", {}).get("display_name") or "Not specified"
            location_text = job.get("location", {}).get("display_name") or "Not specified"
            posting_date = job.get("created") or "Not specified"
            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")
            salary = f"{salary_min}-{salary_max}" if salary_min and salary_max else "Not specified"
            skills = "Not specified"  # Adzuna does not give skills

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "posting_date": posting_date,
                "salary": salary,
                "skills": skills,
                "source": "Adzuna"
            })

        time.sleep(delay)

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_adzuna("data scientist", "in", pages=5, results_per_page=20)
    print(df.head())
    df.to_csv("data/raw/adzuna_jobs.csv", index=False)
