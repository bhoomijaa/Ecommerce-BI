-- =====================================================================
-- E-Commerce BI & Analytics Platform — MySQL Schema
-- Source data: Olist Brazilian E-Commerce Public Dataset (Kaggle)
-- =====================================================================
-- Design notes:
--   * order_items is the revenue grain (1 row per product line per order)
--   * order_payments and order_items use composite PKs because Olist
--     orders can have multiple items and multiple (split) payments
--   * customers.customer_unique_id identifies the real person;
--     customers.customer_id is a per-order surrogate assigned by Olist
--   * date_dim is populated during ETL (Phase 3), not from raw CSVs
-- =====================================================================

CREATE DATABASE IF NOT EXISTS ecommerce_bi
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ecommerce_bi;

-- ---------------------------------------------------------------------
-- Reference / lookup tables
-- ---------------------------------------------------------------------

CREATE TABLE product_category_translation (
    product_category_name          VARCHAR(100) NOT NULL,
    product_category_name_english  VARCHAR(100) NOT NULL,
    PRIMARY KEY (product_category_name)
) ENGINE=InnoDB;

-- Conformed date dimension, populated during ETL to cover the full
-- range of order_purchase_timestamp. Enables fast month/quarter/weekday
-- grouping without repeated date functions in every analytical query.
CREATE TABLE date_dim (
    date_id         INT NOT NULL,                 -- YYYYMMDD, e.g. 20180115
    full_date       DATE NOT NULL,
    day             TINYINT NOT NULL,
    day_name        VARCHAR(10) NOT NULL,
    day_of_week     TINYINT NOT NULL,              -- 1=Monday ... 7=Sunday
    is_weekend      TINYINT(1) NOT NULL,
    month           TINYINT NOT NULL,
    month_name      VARCHAR(10) NOT NULL,
    quarter         TINYINT NOT NULL,
    year            SMALLINT NOT NULL,
    PRIMARY KEY (date_id),
    UNIQUE KEY uq_date_dim_full_date (full_date)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Core entities
-- ---------------------------------------------------------------------

CREATE TABLE customers (
    customer_id                VARCHAR(32) NOT NULL,
    customer_unique_id         VARCHAR(32) NOT NULL,
    customer_zip_code_prefix   INT NOT NULL,
    customer_city              VARCHAR(100) NOT NULL,
    customer_state             CHAR(2) NOT NULL,
    PRIMARY KEY (customer_id),
    KEY idx_customers_unique_id (customer_unique_id),
    KEY idx_customers_state (customer_state)
) ENGINE=InnoDB;

CREATE TABLE sellers (
    seller_id                VARCHAR(32) NOT NULL,
    seller_zip_code_prefix   INT NOT NULL,
    seller_city              VARCHAR(100) NOT NULL,
    seller_state              CHAR(2) NOT NULL,
    PRIMARY KEY (seller_id),
    KEY idx_sellers_state (seller_state)
) ENGINE=InnoDB;

CREATE TABLE products (
    product_id                     VARCHAR(32) NOT NULL,
    product_category_name          VARCHAR(100) NULL,
    product_name_length            SMALLINT NULL,
    product_description_length     SMALLINT NULL,
    product_photos_qty             SMALLINT NULL,
    product_weight_g               INT NULL,
    product_length_cm              INT NULL,
    product_height_cm              INT NULL,
    product_width_cm               INT NULL,
    PRIMARY KEY (product_id),
    KEY idx_products_category (product_category_name),
    CONSTRAINT fk_products_category
        FOREIGN KEY (product_category_name)
        REFERENCES product_category_translation (product_category_name)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE orders (
    order_id                        VARCHAR(32) NOT NULL,
    customer_id                     VARCHAR(32) NOT NULL,
    order_status                    VARCHAR(20) NOT NULL,
    order_purchase_timestamp        DATETIME NOT NULL,
    order_approved_at               DATETIME NULL,
    order_delivered_carrier_date    DATETIME NULL,
    order_delivered_customer_date   DATETIME NULL,
    order_estimated_delivery_date   DATETIME NOT NULL,
    order_purchase_date_id          INT NOT NULL,   -- FK to date_dim
    PRIMARY KEY (order_id),
    KEY idx_orders_customer (customer_id),
    KEY idx_orders_status (order_status),
    KEY idx_orders_purchase_ts (order_purchase_timestamp),
    KEY idx_orders_date_id (order_purchase_date_id),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_orders_date
        FOREIGN KEY (order_purchase_date_id)
        REFERENCES date_dim (date_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE order_items (
    order_id             VARCHAR(32) NOT NULL,
    order_item_id        SMALLINT NOT NULL,
    product_id           VARCHAR(32) NOT NULL,
    seller_id             VARCHAR(32) NOT NULL,
    shipping_limit_date   DATETIME NOT NULL,
    price                 DECIMAL(10,2) NOT NULL,
    freight_value          DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, order_item_id),
    KEY idx_order_items_product (product_id),
    KEY idx_order_items_seller (seller_id),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers (seller_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE order_payments (
    order_id                VARCHAR(32) NOT NULL,
    payment_sequential      SMALLINT NOT NULL,
    payment_type            VARCHAR(20) NOT NULL,
    payment_installments    SMALLINT NOT NULL,
    payment_value           DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, payment_sequential),
    KEY idx_order_payments_type (payment_type),
    CONSTRAINT fk_order_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE order_reviews (
    review_id                  VARCHAR(32) NOT NULL,
    order_id                   VARCHAR(32) NOT NULL,
    review_score                TINYINT NOT NULL,
    review_comment_title        VARCHAR(255) NULL,
    review_comment_message      TEXT NULL,
    review_creation_date        DATETIME NOT NULL,
    review_answer_timestamp     DATETIME NOT NULL,
    PRIMARY KEY (review_id),
    KEY idx_order_reviews_order (order_id),
    KEY idx_order_reviews_score (review_score),
    CONSTRAINT fk_order_reviews_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Notes on deliberately excluded constraints
-- ---------------------------------------------------------------------
-- review_score has no CHECK constraint enforced at DB level for wider
-- MySQL version compatibility (CHECK is enforced from MySQL 8.0.16+).
-- It is validated in the Python ETL layer before load (Phase 3).
-- If running MySQL 8.0.16+, you may optionally add:
--   ALTER TABLE order_reviews ADD CONSTRAINT chk_review_score
--     CHECK (review_score BETWEEN 1 AND 5);
