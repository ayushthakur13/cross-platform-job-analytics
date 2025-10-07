# Data Quality Report

## Dataset Overview
- Shape: 24141 rows × 20 columns
- Duplicates: 22931

## Missing Values (Top 20)
```
posting_date_text     22061
job_type              20681
skills                15596
state                 15574
city                    204
experience_text         204
salary_text             204
location_full           204
collection_session        0
description               0
job_id                    0
source                    0
job_url                   0
company                   0
title                     0
page_found                0
location_searched         0
category_searched         0
scrape_timestamp          0
collection_date           0
```
## Dtypes
```
job_id                object
source                object
scrape_timestamp      object
category_searched     object
location_searched     object
page_found             int64
title                 object
company               object
job_url               object
location_full         object
city                  object
state                 object
posting_date_text     object
salary_text           object
skills                object
description           object
experience_text       object
job_type              object
collection_session    object
collection_date       object
```
## Distribution: salary_text
```
salary_text
Competitive salary         7504
₹ 15,00,000 - 20,00,000     960
₹ 5,00,000 - 12,00,000      475
₹ 2,00,000 - 3,00,000       463
₹ 2,00,000 - 2,50,000       452
₹ 5,00,000 - 25,00,000      391
₹ 4,80,000 - 7,20,000       364
₹ 2,00,000 - 4,00,000       348
₹ 3,00,000 - 5,00,000       344
₹ 3,00,000 - 7,00,000       314
₹ 10,00,000 - 12,00,000     309
₹ 5,00,000 - 18,00,000      306
₹ 2,00,000                  304
₹ 2,00,000 - 3,50,000       301
₹ 3,00,000 - 4,00,000       299
```
## Distribution: experience_text
```
experience_text
1 year(s)     6952
4 year(s)     4071
0 year(s)     3092
5 year(s)     1946
2 year(s)     1728
3 year(s)     1666
6 year(s)     1305
7 year(s)     1192
12 year(s)     896
8 year(s)      632
10 year(s)     405
nan            204
15 year(s)      48
9 year(s)        4
```
## Distribution: job_type
```
job_type
nan                                          20681
Fresher  Job                                  3092
Part time                                      163
Job offer upto ₹ 3LPA post internship           31
Job offer upto ₹ 5LPA post internship           23
Job offer starting ₹ 2LPA post internship       21
Job offer upto ₹ 3.5LPA post internship         19
Job offer upto ₹ 8LPA post internship           17
Job offer upto ₹ 4LPA post internship           12
Job offer upto ₹ 6LPA post internship           11
Job offer upto ₹ 3.6LPA post internship         10
Job offer upto ₹ 2.4LPA post internship          9
Job offer upto ₹ 7LPA post internship            8
Job offer upto ₹ 2.5LPA post internship          8
International                                    7
```
## Distribution: city
```
city
Chennai       6213
Ahmedabad     2758
Gurgaon       1863
Indore        1485
Mumbai        1325
Noida         1188
Delhi         1122
Pune           926
Hyderabad      691
Surat          641
Bangalore      576
Jaipur         400
Cochin         380
Coimbatore     364
Kolkata        295
```
## Distribution: category_searched
```
category_searched
DevOps                    843
iOS App Development       836
Frontend Development      830
Python Development        830
Java Development          830
React Development         830
Quality Assurance         819
Software Development      799
Data Science              795
Full Stack Development    777
Computer Science          776
Backend Development       770
Web Development           770
Machine Learning          767
Mobile App Development    757
```
## Distribution: source
```
source
Internshala    24141
```
## Sample Rows
```
                                  title                            company     city             salary_text experience_text     job_type      source
             Curriculum Developer-AI/ML              Trojan Hunt India LLP Dehradun   ₹ 2,00,000 - 4,00,000       1 year(s)    Part time Internshala
              AI Trainer At SMARRTIF AI                        SMARRTIF AI    Delhi   ₹ 2,00,500 - 3,01,000       1 year(s)          NaN Internshala
              Performance Test Engineer                      E - Solutions  Chennai ₹ 15,00,000 - 20,00,000       6 year(s)          NaN Internshala
             Associate Business Analyst                     Stirring Minds    Delhi   ₹ 2,00,000 - 3,20,000       1 year(s)          NaN Internshala
Artificial Intelligence (AI) Specialist                     Stirring Minds    Delhi   ₹ 2,00,000 - 3,00,000       1 year(s)          NaN Internshala
             Associate Business Analyst         Beri Udyog Private Limited    Delhi   ₹ 2,00,000 - 3,00,000       0 year(s) Fresher  Job Internshala
              Digital Marketing Trainee                     Stirring Minds    Delhi   ₹ 2,00,000 - 3,00,000       1 year(s)          NaN Internshala
   Artificial Intelligence (AI) Manager                     Stirring Minds    Delhi   ₹ 2,00,000 - 5,00,000       1 year(s)    Part time Internshala
 Artificial Intelligence (AI) Executive                     Stirring Minds    Delhi   ₹ 2,00,000 - 5,00,000       1 year(s)          NaN Internshala
                     Big Data Executive True Lineage India Private Limited    Delhi   ₹ 2,00,000 - 2,16,000       1 year(s)          NaN Internshala
```
---

## Cleaning Summary
Rows: 1193 (from 24141)
- Non-null min_salary_inr: 878 (73.6%)
- Non-null max_salary_inr: 878 (73.6%)
- Non-null avg_salary_inr: 878 (73.6%)
- Non-null exp_min_years: 1114 (93.4%)
- Non-null exp_max_years: 1114 (93.4%)
- Non-null experience_level: 865 (72.5%)
- Non-null posting_date: 137 (11.5%)
- Non-null location_tier: 1114 (93.4%)
---

## Preprocessing Summary
Top skills used: Python, English Proficiency (Spoken), Ms-Excel, Effective Communication, Adobe Photoshop, Adobe Illustrator, Javascript, English Proficiency (Written), HTML, Ms-Office, CSS, Ui & Ux Design, Video Editing, Mysql, Adobe Premiere Pro, Node.Js, React, Coreldraw, Rest Api, SQL, Php, Adobe Creative Suite, Hindi Proficiency (Spoken), Interpersonal Skills, Adobe Indesign, Mongodb, Java, Sales, Machine Learning, Client Relationship Management (Crm)
Feature columns: 81

---

## EDA Summary
Rows analyzed: 1193
Rows with salary: 878
Top cities: Mumbai (108), Bangalore (93), Chennai (80), Ahmedabad (71), Hyderabad (63)
Top categories: Data Science (374), Database Building (253), UI/UX Design (139), Quality Assurance (91), Software Development (91)
Top companies: Intertec Softwares Pvt Ltd (19), IBM (16), Sana Search International (14), Kiash Solutions LLP (14), HCL (14)
Experience levels: Junior (537), Mid (165), Senior (163)
Figures: reports\figures\salary_distribution.png, reports\figures\salary_by_city.png, reports\figures\top_categories.png, reports\figures\top_companies.png, reports\figures\top_skills.png, reports\figures\skills_cooccurrence.png, reports\figures\salary_by_experience_level.png, reports\figures\salary_vs_experience.png, reports\figures\city_category_heatmap.png