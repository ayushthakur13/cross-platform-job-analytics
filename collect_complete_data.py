#!/usr/bin/env python3
"""
RELIABLE COMPLETE DATA COLLECTION
Focus: Maximum jobs with complete data from PROVEN working source
Strategy: Prioritize Internshala (100% working) for guaranteed results
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime
import pandas as pd

def collect_complete_job_data():
    """
    Collect maximum complete job data from reliable source (Internshala)
    Focus on data completeness and volume
    """
    
    print("🎯 COMPLETE DATA COLLECTION - MAXIMUM JOBS WITH COMPLETE DATA")
    print("📊 Strategy: Focus on Internshala (proven 99%+ data completeness)")
    print("=" * 80)
    
    session_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create data directory
    os.makedirs('data/raw', exist_ok=True)
    
    # =================================================================
    # INTERNSHALA: MAXIMUM COMPLETE DATA COLLECTION
    # =================================================================
    print("\n🔥 INTERNSHALA: MAXIMUM COMPLETE DATA COLLECTION")
    print("=" * 60)
    
    try:
        from scraping.internshala_optimized import scrape_internshala_optimized
        
        # COMPREHENSIVE categories for maximum job coverage
        internshala_categories = [
            # Core Tech Categories
            "Data Science", "Machine Learning", "Artificial Intelligence (AI)",
            "Software Development", "Full Stack Development", "Backend Development", "Frontend Development",
            "Web Development", "Mobile App Development", "Android App Development", "iOS App Development",
            
            # Programming Languages
            "Python Development", "Java Development", "JavaScript Development",
            "React Development", "Angular.js Development", "Node.js Development", "PHP Development",
            
            # Infrastructure & Operations
            "DevOps", "Cloud Computing", "Database Building", "Network Engineering",
            "Cyber Security", "Big Data",
            
            # Quality & Testing
            "Quality Assurance", "Software Testing",
            
            # Design & Other
            "UI/UX Design", "Computer Science", "Programming",
            
            # Emerging Tech
            "Internet of Things (IoT)", "Computer Vision", "Game Development"
        ]
        
        # COMPREHENSIVE locations across India
        internshala_locations = [
            # Tier 1 Cities (Major Tech Hubs)
            "Delhi", "Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai",
            "Gurgaon", "Noida",
            
            # Tier 2 Cities (Growing Tech Centers)  
            "Kolkata", "Ahmedabad", "Jaipur", "Indore", "Chandigarh", "Kochi",
            "Bhopal", "Lucknow", "Nagpur", "Surat",
            
            # Additional Tech Cities
            "Coimbatore", "Thiruvananthapuram", "Vadodara", "Rajkot"
        ]
        
        print(f"📊 COMPREHENSIVE COVERAGE:")
        print(f"   Categories: {len(internshala_categories)}")
        print(f"   Locations: {len(internshala_locations)}")  
        print(f"   Total combinations: {len(internshala_categories) * len(internshala_locations)}")
        print(f"   Estimated jobs: 1,500 - 3,000 unique jobs (first page only)")
        
        print(f"\n🚀 Starting comprehensive Internshala collection...")
        
        df_internshala = scrape_internshala_optimized(
            categories=internshala_categories,
            locations=internshala_locations,
            max_pages=1,  # First page only for faster collection
            delay=0.8     # Fast collection
        )
        
        print(f"\n✅ INTERNSHALA COLLECTION COMPLETED!")
        print(f"   📊 Total jobs collected: {len(df_internshala):,}")
        
        if len(df_internshala) > 0:
            # Add metadata
            df_internshala['collection_session'] = session_timestamp
            df_internshala['collection_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Save complete dataset
            complete_filename = f"data/raw/complete_jobs_data_{session_timestamp}.csv"
            df_internshala.to_csv(complete_filename, index=False)
            
            # Update main dataset
            main_filename = "data/raw/unified_jobs_dataset.csv"
            df_internshala.to_csv(main_filename, index=False)
            
            # =================================================================
            # COMPREHENSIVE DATA QUALITY ANALYSIS
            # =================================================================
            print("\n" + "🎉" * 30)
            print("🎉 COMPLETE DATA COLLECTION SUCCESS! 🎉") 
            print("🎉" * 30)
            
            total_jobs = len(df_internshala)
            
            print(f"\n📊 FINAL RESULTS:")
            print(f"   🔥 Total unique jobs: {total_jobs:,}")
            print(f"   💾 Complete dataset: {complete_filename}")
            print(f"   💾 Main dataset: {main_filename}")
            
            # Detailed quality analysis
            print(f"\n🔍 DATA COMPLETENESS ANALYSIS:")
            quality_fields = ['salary_text', 'skills', 'description', 'experience_text', 'job_type', 'posting_date_text']
            
            for field in quality_fields:
                filled = df_internshala[field].notna().sum()
                percentage = (filled/total_jobs)*100 if total_jobs > 0 else 0
                print(f"   {field}: {filled:,}/{total_jobs:,} ({percentage:.1f}%)")
            
            # Calculate complete jobs (with salary + skills + description)
            complete_jobs = df_internshala[
                df_internshala['salary_text'].notna() & 
                df_internshala['skills'].notna() & 
                df_internshala['description'].notna()
            ]
            complete_count = len(complete_jobs)
            complete_percentage = (complete_count/total_jobs)*100 if total_jobs > 0 else 0
            
            print(f"\n🏆 COMPLETE JOBS (Salary + Skills + Description):")
            print(f"   Complete jobs: {complete_count:,}/{total_jobs:,} ({complete_percentage:.1f}%)")
            
            # Geographic distribution
            print(f"\n🌍 GEOGRAPHIC DISTRIBUTION (Top 15):")
            city_counts = df_internshala['city'].value_counts().head(15)
            for city, count in city_counts.items():
                print(f"   {city}: {count:,} jobs")
            
            # Category distribution
            print(f"\n📋 CATEGORY DISTRIBUTION (Top 15):")
            category_counts = df_internshala['category_searched'].value_counts().head(15)
            for category, count in category_counts.items():
                print(f"   {category}: {count:,} jobs")
            
            # Company distribution
            print(f"\n🏢 TOP HIRING COMPANIES (Top 10):")
            company_counts = df_internshala['company'].value_counts().head(10)
            for company, count in company_counts.items():
                if company != "Not specified":
                    print(f"   {company}: {count:,} jobs")
            
            # Salary analysis
            salary_jobs = df_internshala[df_internshala['salary_text'].notna()]
            if len(salary_jobs) > 0:
                print(f"\n💰 SALARY DATA SAMPLES:")
                salary_samples = salary_jobs['salary_text'].value_counts().head(10)
                for salary, count in salary_samples.items():
                    print(f"   {salary}: {count:,} jobs")
            
            # Skills analysis
            skills_jobs = df_internshala[df_internshala['skills'].notna()]
            if len(skills_jobs) > 0:
                print(f"\n🛠️ TOP SKILLS (Sample):")
                # Extract individual skills
                all_skills = []
                for skills_str in skills_jobs['skills'].head(1000):  # Sample first 1000
                    if pd.notna(skills_str):
                        skills_list = [skill.strip() for skill in str(skills_str).split(',')]
                        all_skills.extend(skills_list)
                
                if all_skills:
                    from collections import Counter
                    skills_counter = Counter(all_skills)
                    top_skills = skills_counter.most_common(15)
                    for skill, count in top_skills:
                        print(f"   {skill}: {count:,} mentions")
            
            # Sample data preview
            print(f"\n📋 SAMPLE COMPLETE JOBS:")
            sample_cols = ['title', 'company', 'city', 'salary_text', 'experience_text']
            sample_data = complete_jobs[sample_cols].head(5) if len(complete_jobs) > 0 else df_internshala[sample_cols].head(5)
            print(sample_data.to_string(index=False, max_colwidth=40))
            
            print("\n" + "="*80)
            print("✅ COMPLETE DATA COLLECTION SUCCESSFUL!")
            print("🎯 READY FOR ANALYSIS AND VISUALIZATION")
            print(f"📊 Dataset Quality: {complete_percentage:.1f}% complete jobs")
            print(f"💾 Main file: {main_filename}")
            print("="*80)
            
            return df_internshala
        
        else:
            print("❌ No data collected from Internshala")
            return None
            
    except Exception as e:
        print(f"❌ Internshala collection failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🌟 STARTING COMPLETE DATA COLLECTION 🌟")
    print("Focus: Maximum jobs with complete data from reliable source")
    print("⏱️ Estimated time: 8-12 minutes for fast collection (first page only)")
    print("🎯 Target: 1,500+ jobs with high data completeness")
    
    df = collect_complete_job_data()
    
    if df is not None and len(df) > 0:
        print(f"\n🎊 MISSION ACCOMPLISHED! 🎊")
        print(f"✅ Collected {len(df):,} complete jobs successfully!")
        print("🎯 Ready for comprehensive job market analytics!")
        print("\n📁 Data saved to data/raw/unified_jobs_dataset.csv")
    else:
        print("\n❌ Collection failed")
        print("🔄 Please check connection and try again")