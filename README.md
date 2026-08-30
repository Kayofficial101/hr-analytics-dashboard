# HR attrition analysis

This project uses Python and SQL to narrow an overall attrition number into specific questions an HR team can investigate.

## What I was trying to solve

A company-wide rate is too broad to guide action. I wanted to find where attrition was concentrated and produce a smaller follow-up list for managers.

## What I did

1. Analyzed 1,470 employee records.
2. Compared attrition by role, department and overtime status.
3. Used SQL to create repeatable manager views.
4. Converted the strongest patterns into follow-up questions instead of claiming they were causes.

![HR attrition dashboard](visuals/dashboard.svg)

## What I found

- Overall attrition was **14.4%**.
- Attrition among employees with overtime was **23.8%**, compared with **10.6%** without overtime.
- Sales Representatives had the highest role-level attrition at **19.8%**.
- Department rates were close, so a department-wide response would be poorly targeted.

The first review would focus on overtime frequency, staffing capacity, newer employees working overtime, and role or manager patterns among Sales Representatives.

## Tools used

Python, SQL and workforce segmentation.

## Main files

- [Case study](CASE_STUDY.md): findings and follow-up plan
- [Python analysis](scripts/generate_and_analyze.py): data generation and calculations
- [SQL queries](sql/attrition_queries.sql): recurring HR views
- [Employee data](data/hr_attrition.csv): records used in the project

The records were created for this project. Run `python scripts/generate_and_analyze.py` to rebuild the analysis.
