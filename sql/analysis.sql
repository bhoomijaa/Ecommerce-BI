USE ecommerce_bi;

-- KPI 1: Total Revenue

SELECT 
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM order_payments;