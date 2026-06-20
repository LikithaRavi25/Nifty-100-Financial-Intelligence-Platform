-- Q1 Total Companies

SELECT COUNT(*)
FROM companies;


-- Q2 Sector-wise Company Count

SELECT sector,
       COUNT(*) AS total_companies
FROM sectors
GROUP BY sector
ORDER BY total_companies DESC;


-- Q3 Top 10 Companies by Market Cap

SELECT company_id,
       market_cap
FROM market_cap
ORDER BY market_cap DESC
LIMIT 10;


-- Q4 Top 10 Companies by Sales

SELECT company_id,
       sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;


-- Q5 Top 10 Companies by Net Profit

SELECT company_id,
       net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;


-- Q6 Highest EPS Companies

SELECT company_id,
       eps
FROM profitandloss
ORDER BY eps DESC
LIMIT 10;


-- Q7 Highest ROE Companies

SELECT company_name,
       roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;


-- Q8 Highest ROCE Companies

SELECT company_name,
       roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;


-- Q9 Companies with Highest Stock Price

SELECT company_id,
       close_price
FROM stock_prices
ORDER BY close_price DESC
LIMIT 10;


-- Q10 Companies with Highest Dividend Payout

SELECT company_id,
       dividend_payout
FROM profitandloss
ORDER BY dividend_payout DESC
LIMIT 10;