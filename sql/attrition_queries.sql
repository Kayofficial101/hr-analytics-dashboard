-- HR Attrition Analysis

-- 1. Attrition by department and overtime
SELECT 
    Department,
    OverTime,
    COUNT(*) AS employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate
FROM hr_data
GROUP BY Department, OverTime
ORDER BY attrition_rate DESC;

-- 2. Tenure risk analysis
SELECT 
    CASE 
        WHEN YearsAtCompany < 2 THEN '0-2 years'
        WHEN YearsAtCompany < 5 THEN '2-5 years'
        WHEN YearsAtCompany < 10 THEN '5-10 years'
        ELSE '10+ years'
    END AS tenure_band,
    COUNT(*) AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS rate
FROM hr_data
GROUP BY tenure_band
ORDER BY rate DESC;
