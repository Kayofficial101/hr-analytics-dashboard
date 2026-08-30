# HR Analytics: Employee Attrition Dashboard

This **Python + SQL** case looks at where HR should investigate attrition first. It uses 1,470 synthetic employee records and includes a compact dashboard, source data, query layer and written recommendations.

> Data note: every employee record is synthetic. No employer or employee data is used.

![HR attrition dashboard](visuals/dashboard.svg)

## Start here

- [Read the case study](CASE_STUDY.md)
- [Review the generator and analysis](scripts/generate_and_analyze.py)
- [Inspect the SQL](sql/attrition_queries.sql)
- [Open the source data](data/hr_attrition.csv)

## Headline findings

- **14.4%** overall attrition
- **23.8%** attrition with overtime versus **10.6%** without overtime
- **19.8%** attrition among Sales Representatives, the highest generated role-level rate
- Department rates remain close, which suggests investigating role and workload before broad department-level action

## Repository map

| Path | Purpose |
|---|---|
| `data/hr_attrition.csv` | 1,470-row source dataset |
| `scripts/generate_and_analyze.py` | Deterministic data generation, analysis and SVG dashboard |
| `outputs/summary.json` | Machine-readable KPI reconciliation |
| `sql/attrition_queries.sql` | Segmentation, risk queue and QA queries |
| `CASE_STUDY.md` | Findings, recommendations and limitations |

## Reproduce

```bash
python scripts/generate_and_analyze.py
```

The script uses only Python's standard library and a fixed seed.
