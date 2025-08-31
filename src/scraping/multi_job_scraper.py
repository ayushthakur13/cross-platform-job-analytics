# src/scraping/multi_job_scraper.py
import pandas as pd
from .internshala_scraper import scrape_internshala
from .timesjobs_scraper import scrape_timesjobs
from .adzuna_scraper import scrape_adzuna

def scrape_all_jobs(query="data scientist", location="Delhi", pages=5):
    # Scrape Internshala
    df_internshala = scrape_internshala(query=query, location=location, max_pages=pages)
    print(f"Internshala jobs scraped: {len(df_internshala)}")
    
    # Scrape TimesJobs
    df_timesjobs = scrape_timesjobs(query=query, location=location, max_pages=pages)
    print(f"TimesJobs jobs scraped: {len(df_timesjobs)}")
    
    # Scrape Adzuna
    df_adzuna = scrape_adzuna(query=query, location="in", pages=pages, results_per_page=20)
    print(f"Adzuna jobs scraped: {len(df_adzuna)}")
    
    # Concatenate all dataframes
    combined_df = pd.concat([df_internshala, df_timesjobs, df_adzuna], ignore_index=True)
    
    # Drop exact duplicates
    combined_df.drop_duplicates(subset=["title", "company", "location", "posting_date"], inplace=True)
    
    # Save final dataset
    combined_df.to_csv("data/raw/all_jobs.csv", index=False)
    print(f"Total jobs after combining: {len(combined_df)}")
    
    return combined_df

if __name__ == "__main__":
    df = scrape_all_jobs(query="data scientist", location="Delhi", pages=5)
