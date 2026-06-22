-- Top 10 Companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Top 10 Companies by ROCE
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- Highest Net Profit
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- Highest Sales
SELECT company_id, year, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- Highest EPS
SELECT company_id, year, eps
FROM profitandloss
ORDER BY eps DESC
LIMIT 10;