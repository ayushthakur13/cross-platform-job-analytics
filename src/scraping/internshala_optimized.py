import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import hashlib

def scrape_internshala_optimized(categories=None, locations=None, max_pages=10, delay=1.5):
    """
    Optimized Internshala scraper with duplicate detection and consistent output format
    
    Args:
        categories: List of job categories to search for
        locations: List of locations to search in  
        max_pages: Maximum pages to scrape (with early stopping on duplicates)
        delay: Delay between requests in seconds
    """
    
    # Default comprehensive tech categories
    if categories is None:
        categories = [
            "Data Science", "Software Development", "Machine Learning", "Web Development",
            "Mobile App Development", "Android App Development", "iOS App Development",
            "Full Stack Development", "Frontend Development", "Backend Development",
            "JavaScript Development", "Python Development", "Java Development",
            "Node.js Development", "Angular.js Development", "React Development",
            "PHP Development", "Cloud Computing", "DevOps", "Artificial Intelligence (AI)",
            "Big Data", "Computer Science", "Computer Vision", "Cyber Security",
            "Database Building", "Game Development", "Information Technology",
            "Internet of Things (IoT)", "Network Engineering", "Programming", 
            "Software Testing", "UI/UX Design", "Quality Assurance"
        ]
    
    # Default major Indian cities  
    if locations is None:
        locations = [
            "Delhi", "Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai",
            "Gurgaon", "Noida", "Kolkata", "Ahmedabad", "Jaipur", "Indore"
        ]
    
    print(f"🚀 Starting optimized Internshala scraping...")
    print(f"📋 Categories: {len(categories)}")
    print(f"📍 Locations: {len(locations)}")
    print(f"🔍 Smart duplicate detection enabled")
    print("=" * 60)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_jobs = []
    seen_jobs = set()  # Track unique jobs by hash
    stats = {
        'total_combinations': len(categories) * len(locations),
        'successful_combinations': 0,
        'total_pages_scraped': 0,
        'unique_jobs_found': 0,
        'duplicates_skipped': 0,
        'categories_with_data': set(),
        'locations_with_data': set()
    }
    
    combination_count = 0
    
    for category in categories:
        for location in locations:
            combination_count += 1
            
            print(f"\\n[{combination_count}/{stats['total_combinations']}] Processing: {category} in {location}")
            
            # Create clean URL
            category_clean = category.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-').replace('.', '')
            location_clean = location.lower().replace(' ', '-')
            base_url = f"https://internshala.com/jobs/{category_clean}-jobs-in-{location_clean}"
            
            combination_unique_jobs = 0
            combination_duplicates = 0
            pages_with_same_data = 0
            
            for page in range(1, max_pages + 1):
                url = f"{base_url}?page={page}"
                print(f"  📄 Page {page}: ", end="")
                
                try:
                    response = requests.get(url, headers=headers, timeout=15)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    job_cards = soup.select("div.individual_internship")
                    
                    if not job_cards:
                        print("No jobs found, stopping pagination")
                        break
                    
                    page_unique_count = 0
                    page_duplicate_count = 0
                    
                    for card in job_cards:
                        # Extract basic job info for duplicate detection
                        title_el = card.find("a", class_="job-title-href")
                        company_el = card.find("p", class_="company-name")
                        
                        if not title_el or not company_el:
                            continue
                        
                        title = title_el.text.strip()
                        company = company_el.text.strip()
                        
                        # Create unique hash for this job
                        job_hash = hashlib.md5(f"{title}|{company}|{category}|{location}".encode()).hexdigest()
                        
                        if job_hash in seen_jobs:
                            page_duplicate_count += 1
                            stats['duplicates_skipped'] += 1
                            continue
                        
                        seen_jobs.add(job_hash)
                        page_unique_count += 1
                        stats['unique_jobs_found'] += 1
                        
                        # Extract comprehensive job data (consistent format)
                        job_data = {
                            # Basic identifiers
                            'job_id': job_hash,
                            'source': 'Internshala',
                            'scrape_timestamp': datetime.now().isoformat(),
                            'category_searched': category,
                            'location_searched': location,
                            'page_found': page,
                            
                            # Core job information
                            'title': title,
                            'company': company,
                        }
                        
                        # Job URL
                        job_data['job_url'] = f"https://internshala.com{title_el.get('href')}" if title_el.get('href') else None
                        
                        # Location details
                        location_el = card.find("p", class_="row-1-item locations")
                        if location_el:
                            location_links = location_el.find_all("a")
                            job_data['location_full'] = ", ".join([link.text.strip() for link in location_links]) if location_links else location_el.text.strip()
                        else:
                            job_data['location_full'] = None
                        
                        # Extract city and state from location
                        location_text = job_data['location_full'] or ""
                        if ',' in location_text:
                            parts = location_text.split(',')
                            job_data['city'] = parts[0].strip()
                            job_data['state'] = parts[1].strip() if len(parts) > 1 else None
                        else:
                            job_data['city'] = location_text.strip()
                            job_data['state'] = None
                        
                        # Posting date
                        date_el = card.find("div", class_="status-info")
                        if date_el:
                            date_span = date_el.find("span")
                            job_data['posting_date_text'] = date_span.text.strip() if date_span else None
                        else:
                            job_data['posting_date_text'] = None
                        
                        # Salary information
                        salary_els = card.find_all("div", class_="row-1-item")
                        job_data['salary_text'] = None
                        for el in salary_els:
                            if el.find("i", class_="ic-16-money"):
                                salary_span = el.find("span", class_="desktop") or el.find("span", class_="mobile")
                                job_data['salary_text'] = salary_span.text.strip() if salary_span else None
                                break
                        
                        # Skills
                        skills_container = card.find("div", class_="job_skills")
                        if skills_container:
                            skill_divs = skills_container.find_all("div", class_="job_skill")
                            skills_list = [skill.text.strip() for skill in skill_divs]
                            job_data['skills'] = ", ".join(skills_list) if skills_list else None
                        else:
                            job_data['skills'] = None
                        
                        # Job description
                        desc_el = card.find("div", class_="about_job")
                        if desc_el:
                            text_div = desc_el.find("div", class_="text")
                            job_data['description'] = text_div.text.strip() if text_div else None
                        else:
                            job_data['description'] = None
                        
                        # Experience requirement
                        job_data['experience_text'] = None
                        for el in salary_els:
                            if el.find("i", class_="ic-16-briefcase"):
                                exp_span = el.find("span")
                                job_data['experience_text'] = exp_span.text.strip() if exp_span else None
                                break
                        
                        # Job type
                        job_type_el = card.find("div", class_="gray-labels")
                        if job_type_el:
                            type_span = job_type_el.find("span")
                            job_data['job_type'] = type_span.text.strip() if type_span else None
                        else:
                            job_data['job_type'] = None
                        
                        all_jobs.append(job_data)
                    
                    stats['total_pages_scraped'] += 1
                    
                    # Print page results
                    if page_unique_count > 0:
                        print(f"✅ {page_unique_count} unique, {page_duplicate_count} duplicates")
                        combination_unique_jobs += page_unique_count
                        combination_duplicates += page_duplicate_count
                    else:
                        print(f"⚠️ All {len(job_cards)} jobs were duplicates")
                        pages_with_same_data += 1
                        
                        # Stop if we get 2 consecutive pages with all duplicates
                        if pages_with_same_data >= 2:
                            print(f"    🛑 Stopping - found {pages_with_same_data} consecutive pages with all duplicates")
                            break
                    
                except requests.exceptions.RequestException as e:
                    print(f"❌ Request failed: {e}")
                    continue
                except Exception as e:
                    print(f"❌ Error: {e}")
                    continue
                
                time.sleep(delay)
            
            if combination_unique_jobs > 0:
                stats['successful_combinations'] += 1
                stats['categories_with_data'].add(category)
                stats['locations_with_data'].add(location)
                print(f"  📊 Combination total: {combination_unique_jobs} unique jobs")
            else:
                print(f"  ⚠️ No unique jobs found for this combination")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_jobs)
    
    # Print final statistics
    print("\\n" + "="*60)
    print("🎉 INTERNSHALA SCRAPING COMPLETED")
    print("="*60)
    print(f"📊 Final Statistics:")
    print(f"   Total unique jobs: {stats['unique_jobs_found']:,}")
    print(f"   Duplicates skipped: {stats['duplicates_skipped']:,}")
    print(f"   Successful combinations: {stats['successful_combinations']}/{stats['total_combinations']}")
    print(f"   Pages scraped: {stats['total_pages_scraped']}")
    print(f"   Categories with data: {len(stats['categories_with_data'])}")
    print(f"   Locations with data: {len(stats['locations_with_data'])}")
    print(f"   Efficiency: {(stats['unique_jobs_found']/(stats['unique_jobs_found']+stats['duplicates_skipped'])*100):.1f}% unique data")
    
    return df

if __name__ == "__main__":
    # Test with focused categories and locations
    test_categories = [
        "Data Science", "Software Development", "Machine Learning", 
        "Web Development", "Mobile App Development", "Full Stack Development",
        "Artificial Intelligence (AI)", "Cloud Computing"
    ]
    
    test_locations = [
        "Delhi", "Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai"
    ]
    
    df = scrape_internshala_optimized(
        categories=test_categories,
        locations=test_locations,
        max_pages=5,
        delay=1.5
    )
    
    if len(df) > 0:
        print(f"\\n✅ Scraped {len(df)} unique jobs")
        print("Sample data:")
        print(df[['title', 'company', 'city', 'category_searched', 'salary_text']].head())
    else:
        print("❌ No data scraped")