import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_internshala(query="software", location="", max_pages=5, delay=2):
    jobs = []
    base_url = f"https://internshala.com/internships/{query}-internship-in-{location}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, max_pages+1):
        url = f"{base_url}?page={page}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.select("div.individual_internship")
        if not job_cards:
            break

        for job_card in job_cards:
            title = job_card.find("h3")
            title = title.text.strip() if title else None
            if not title or len(title)<3:
                continue

            company = job_card.find("a", class_="link_display_like_text")
            company = company.text.strip() if company else "Not specified"

            location_text = job_card.find("a", class_="location_link")
            location_text = location_text.text.strip() if location_text else "Not specified"

            posting_date = job_card.find("div", class_="item_body")
            posting_date = posting_date.text.strip().split("\n")[0] if posting_date else "Not specified"

            stipend = job_card.find("span", class_="stipend")
            salary = stipend.text.strip() if stipend else "Not specified"

            skill_tags = job_card.select("div.other_info_container span.internship_tags_container a")
            skills = ", ".join([s.text.strip() for s in skill_tags]) if skill_tags else "Not specified"

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "posting_date": posting_date,
                "salary": salary,
                "skills": skills,
                "source": "Internshala"
            })

        time.sleep(delay)

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_internshala("data scientist", "Delhi", max_pages=10)
    print(df.head())
    df.to_csv("data/raw/internshala_jobs.csv", index=False)
