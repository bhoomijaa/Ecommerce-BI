USE ecommerce_bi;

-- =====================================================
-- 1. MONTHLY SALES VIEW
-- =====================================================

CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(DISTINCT c.customer_unique_id) AS customers,
    ROUND(SUM(p.payment_value), 2) AS revenue,
    ROUND(
        SUM(p.payment_value) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN (
    SELECT
        order_id,
        SUM(payment_value) AS payment_value
    FROM order_payments
    GROUP BY order_id
) p
    ON o.order_id = p.order_id
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m');


-- =====================================================
-- 2. CATEGORY PERFORMANCE VIEW
-- =====================================================

CREATE OR REPLACE VIEW vw_category_performance AS
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS category,

    COUNT(DISTINCT oi.order_id) AS orders,

    ROUND(SUM(oi.price), 2) AS revenue,

    ROUND(AVG(oi.price), 2) AS average_item_price,

    ROUND(AVG(r.review_score), 2) AS average_review_score

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN product_category_translation t
    ON p.product_category_name = t.product_category_name

LEFT JOIN order_reviews r
    ON oi.order_id = r.order_id

GROUP BY category;


-- =====================================================
-- 3. CUSTOMER SEGMENT VIEW
-- =====================================================

CREATE OR REPLACE VIEW vw_customer_segments AS

SELECT
    customer_unique_id,

    order_count,

    total_spend,

    CASE
        WHEN order_count = 1
            THEN 'One-Time Customer'

        WHEN order_count BETWEEN 2 AND 3
            THEN 'Repeat Customer'

        ELSE 'Loyal Customer'
    END AS customer_segment

FROM (

    SELECT
        c.customer_unique_id,

        COUNT(DISTINCT o.order_id) AS order_count,

        ROUND(
            SUM(COALESCE(p.payment_value, 0)),
            2
        ) AS total_spend

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    LEFT JOIN (
        SELECT
            order_id,
            SUM(payment_value) AS payment_value
        FROM order_payments
        GROUP BY order_id
    ) p
        ON o.order_id = p.order_id

    GROUP BY c.customer_unique_id

) customer_data;


-- =====================================================
-- 4. DELIVERY PERFORMANCE VIEW
-- =====================================================

CREATE OR REPLACE VIEW vw_delivery_performance AS

SELECT

    c.customer_state,

    COUNT(DISTINCT o.order_id) AS delivered_orders,

    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_days,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN o.order_delivered_customer_date >
                     o.order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        )
        / COUNT(DISTINCT o.order_id),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN order_reviews r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL

GROUP BY c.customer_state;


-- =====================================================
-- VERIFY THE VIEWS
-- =====================================================

SELECT * FROM vw_monthly_sales;
SELECT * FROM vw_category_performance;
SELECT * FROM vw_customer_segments LIMIT 10;
SELECT * FROM vw_delivery_performance;