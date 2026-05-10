-- TELCO CUSTOMER CHURN ANALYSIS SQL

-- Total Customers
SELECT COUNT(*) AS total_customers
FROM telco_churn;

-- Churn Customers
SELECT COUNT(*) AS churn_customers
FROM telco_churn
WHERE [Churn Label] = 'Yes';

-- Churn Rate
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN [Churn Label] = 'Yes' THEN 1 ELSE 0 END) AS churn_customers,
    ROUND(
        SUM(CASE WHEN [Churn Label] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM telco_churn;

-- Contract Analysis
SELECT
    Contract,
    COUNT(*) AS customers,
    ROUND(AVG([Monthly Charge]), 2) AS avg_monthly_charge
FROM telco_churn
GROUP BY Contract
ORDER BY customers DESC;

-- Internet Type Analysis
SELECT
    [Internet Type],
    COUNT(*) AS customers,
    ROUND(AVG([Monthly Charge]), 2) AS avg_monthly_charge
FROM telco_churn
GROUP BY [Internet Type]
ORDER BY customers DESC;

-- Payment Method Analysis
SELECT
    [Payment Method],
    COUNT(*) AS customers,
    ROUND(AVG([Monthly Charge]), 2) AS avg_monthly_charge
FROM telco_churn
GROUP BY [Payment Method]
ORDER BY avg_monthly_charge DESC;

-- Gender Analysis
SELECT
    Gender,
    COUNT(*) AS customers
FROM telco_churn
GROUP BY Gender;

-- Senior Citizen Analysis
SELECT
    [Senior Citizen],
    COUNT(*) AS customers,
    ROUND(AVG([Monthly Charge]), 2) AS avg_monthly_charge
FROM telco_churn
GROUP BY [Senior Citizen];
