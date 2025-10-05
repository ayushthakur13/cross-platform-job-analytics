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
