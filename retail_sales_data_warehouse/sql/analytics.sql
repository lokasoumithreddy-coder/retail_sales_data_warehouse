-- 1. Total sales and transaction count
SELECT COUNT(*) AS transactions,
       ROUND(SUM(sales_amount), 2) AS total_revenue
FROM fact_sales;

-- 2. Revenue by product
SELECT p.product_name,
       SUM(f.quantity) AS units_sold,
       ROUND(SUM(f.sales_amount), 2) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC;

-- 3. Revenue by category
SELECT p.category,
       ROUND(SUM(f.sales_amount), 2) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;

-- 4. Monthly revenue
SELECT d.year, d.month, d.month_name,
       ROUND(SUM(f.sales_amount), 2) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 5. Top 5 customers by revenue
SELECT c.customer_id,
       ROUND(SUM(f.sales_amount), 2) AS total_spent
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5;

-- 6. Average transaction value
SELECT ROUND(AVG(sales_amount), 2) AS average_transaction_value
FROM fact_sales;
