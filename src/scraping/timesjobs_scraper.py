import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_timesjobs(query="software developer", location="", max_pages=5, delay=2):
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, max_pages+1):
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={query}&txtLocation={location}&sequence={page}&startPage={page}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        if not job_cards:
            break

        for job in job_cards:
            title_el = job.find("h2")
            title = title_el.text.strip() if title_el else None
            if not title or len(title)<3:
                continue

            company_el = job.find("h3", class_="joblist-comp-name")
            company = company_el.text.strip().replace("\n", "") if company_el else "Not specified"

            loc_el = job.find("ul", class_="top-jd-dtl clearfix")
            location_text = loc_el.find_all("li")[1].text.strip() if loc_el and len(loc_el.find_all("li"))>1 else "Not specified"

            date_el = job.find("span", class_="sim-posted")
            posting_date = date_el.text.strip() if date_el else "Not specified"

            skills_el = job.find("span", class_="srp-skills")
            skills = skills_el.text.strip().replace("\n", "").replace("  ", "") if skills_el else "Not specified"

            salary = "Not specified"  # TimesJobs does not provide salary

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "posting_date": posting_date,
                "salary": salary,
                "skills": skills,
                "source": "TimesJobs"
            })

        time.sleep(delay)

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_timesjobs("data scientist", "Delhi", max_pages=5)
    print(df.head())
    df.to_csv("data/raw/timesjobs_jobs.csv", index=False)
