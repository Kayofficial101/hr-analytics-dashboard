-- HR attrition case study
-- PostgreSQL-compatible queries for data/hr_attrition.csv loaded as hr_data.

-- 1. Overall attrition.
SELECT
    COUNT(*) AS employees,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS attrited,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM hr_data;

-- 2. Attrition by department and overtime.
SELECT
    department,
    overtime,
    COUNT(*) AS employees,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM hr_data
GROUP BY department, overtime
ORDER BY attrition_rate_pct DESC;

-- 3. Tenure risk bands.
SELECT
    CASE
        WHEN years_at_company < 2 THEN '0-1 years'
        WHEN years_at_company < 5 THEN '2-4 years'
        WHEN years_at_company < 10 THEN '5-9 years'
        ELSE '10+ years'
    END AS tenure_band,
    COUNT(*) AS employees,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM hr_data
GROUP BY tenure_band
ORDER BY MIN(years_at_company);

-- 4. Job-role ranking.
SELECT
    job_role,
    COUNT(*) AS employees,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS attrited,
    ROUND(100.0 * AVG(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END), 1) AS attrition_rate_pct
FROM hr_data
GROUP BY job_role
HAVING COUNT(*) >= 25
ORDER BY attrition_rate_pct DESC;

-- 5. High-risk stay-interview queue.
SELECT
    employee_id,
    department,
    job_role,
    age,
    years_at_company,
    overtime,
    monthly_income
FROM hr_data
WHERE attrition = 'No'
  AND overtime = 'Yes'
  AND years_at_company < 2
ORDER BY monthly_income DESC;

-- 6. Data-quality checks.
SELECT
    COUNT(*) - COUNT(DISTINCT employee_id) AS duplicate_employee_ids,
    COUNT(*) FILTER (WHERE age < 18 OR age > 70) AS invalid_ages,
    COUNT(*) FILTER (WHERE monthly_income < 0) AS negative_income,
    COUNT(*) FILTER (WHERE attrition NOT IN ('Yes', 'No')) AS invalid_attrition_values
FROM hr_data;
