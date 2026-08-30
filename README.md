# HR attrition analysis

This Python and SQL project looks at where an HR team should investigate attrition first.

> Data note: the 1,470 employee records are generated for this project.

![HR attrition dashboard](visuals/dashboard.svg)

## Findings

- Overall attrition: **14.4%**
- Attrition with overtime: **23.8%**, compared with **10.6%** without overtime
- Sales Representative attrition: **19.8%**, the highest role-level rate in the data
- Department rates are close, so a department-wide response would be poorly targeted

The useful follow-up is narrower: review overtime frequency and staffing capacity, speak with newer employees who work overtime, and inspect role and manager patterns among Sales Representatives.

## Files

- [Case notes](CASE_STUDY.md)
- [Python analysis](scripts/generate_and_analyze.py)
- [SQL queries](sql/attrition_queries.sql)
- [Source records](data/hr_attrition.csv)

## Rebuild

```bash
python scripts/generate_and_analyze.py
```
