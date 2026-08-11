# 🛒 E-Commerce Business Analytics Dashboard

An end-to-end **E-Commerce Business Intelligence project** built using **Python, MySQL, SQL, and Power BI**.

This project takes raw Brazilian e-commerce data, cleans and transforms it using Python, loads it into a structured MySQL database, performs business analysis using SQL, and presents the resulting insights through an interactive Power BI dashboard.

---

## 📌 Project Overview

The objective of this project is to analyze e-commerce business performance and answer important business questions related to:

- Revenue and sales performance
- Customer behavior
- Customer segmentation
- Product category performance
- Order trends
- Average Order Value
- Delivery performance
- Geographic performance
- Seller performance

The project demonstrates a complete analytics workflow:

**Raw Data → Python Data Processing → MySQL Database → SQL Analysis → Power BI Dashboard**

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data inspection, cleaning and transformation |
| Pandas | Data manipulation and preprocessing |
| MySQL | Relational database and data storage |
| SQL | Business analysis and analytical views |
| Power BI | Data visualization and dashboarding |
| Git & GitHub | Version control |

---

## 📂 Project Structure

    Ecommerce-BI/
    │
    ├── data/
    │   ├── raw/
    │   │   ├── olist_customers_dataset.csv
    │   │   ├── olist_geolocation_dataset.csv
    │   │   ├── olist_order_items_dataset.csv
    │   │   ├── olist_order_payments_dataset.csv
    │   │   ├── olist_order_reviews_dataset.csv
    │   │   ├── olist_orders_dataset.csv
    │   │   ├── olist_products_dataset.csv
    │   │   ├── olist_sellers_dataset.csv
    │   │   └── product_category_name_translation.csv
    │   │
    │   └── cleaned/
    │       ├── customers_clean.csv
    │       ├── order_items_clean.csv
    │       ├── order_payments_clean.csv
    │       ├── order_reviews_clean.csv
    │       ├── orders_clean.csv
    │       ├── products_clean.csv
    │       └── sellers_clean.csv
    │
    ├── python/
    │   ├── inspect_data.py
    │   ├── transform.py
    │   ├── fix_categories.py
    │   ├── load.py
    │   └── create_date_dim.py
    │
    ├── sql/
    │   ├── schema.sql
    │   ├── analysis.sql
    │   └── views.sql
    │
    ├── Ecommerce_Business_Analytics.pbix
    ├── .gitignore
    └── README.md

---

## 📊 Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains information about:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Product categories
- Geographic information

The raw datasets were cleaned and transformed before being loaded into MySQL for analysis.

---

## 🔄 Data Pipeline

### 1. Data Inspection

The raw CSV files were first inspected using Python to understand:

- Dataset structure
- Column names
- Data types
- Missing values
- Duplicate records
- Relationships between datasets

The inspection was performed using `inspect_data.py`.

### 2. Data Cleaning & Transformation

The raw datasets were cleaned and prepared for database loading.

The transformation process included:

- Handling missing values
- Standardizing data types
- Cleaning categorical information
- Preparing datasets for relational storage
- Creating cleaned CSV files

The main transformation scripts are:

- `transform.py`
- `fix_categories.py`

### 3. MySQL Database

The cleaned datasets were loaded into a MySQL database named:

`ecommerce_bi`

The database schema is defined in:

`sql/schema.sql`

### 4. Date Dimension

A dedicated date dimension was created for time-based analysis.

The script:

`python/create_date_dim.py`

creates and populates the date dimension used for analyzing trends over time.

### 5. SQL Business Analysis

SQL was used to perform business-oriented analysis on the loaded data.

The analysis covers:

- Revenue
- Orders
- Customers
- Products
- Categories
- Delivery performance
- Customer segments
- Geographic performance

The analytical queries are stored in:

`sql/analysis.sql`

### 6. Analytical Views

Reusable SQL views were created to simplify reporting and provide Power BI with prepared analytical datasets.

The views are defined in:

`sql/views.sql`

These views combine and aggregate relevant data before it is consumed by Power BI.

---

## 📈 Power BI Dashboard

The final dashboard was created using **Microsoft Power BI**.

### Key KPIs

The dashboard includes:

- **Total Revenue**
- **Total Orders**
- **Total Customers**
- **Average Order Value**

### Visualizations

The dashboard provides analysis of:

- Revenue by month
- Revenue by product category
- Customer segmentation
- Average delivery performance by state
- Product and category performance

The Power BI report is available in:

`Ecommerce_Business_Analytics.pbix`

---

## 💡 Key Business Questions

The project was designed to answer questions such as:

1. How is revenue changing over time?
2. Which product categories generate the most revenue?
3. How many unique customers does the business have?
4. What is the Average Order Value?
5. How are customers distributed across different segments?
6. Which states have higher delivery performance metrics?
7. Which product categories contribute the most to overall revenue?
8. What trends can be observed in e-commerce sales?

---

## 🧠 Customer Segmentation

Customers were categorized into different segments based on their purchasing behavior.

The dashboard includes:

- **One-Time Customer**
- **Repeat Customer**
- **Loyal Customer**

This segmentation helps analyze customer retention and purchasing patterns.

---

## 🗄️ Database Architecture

The project follows a relational database approach where different aspects of the e-commerce business are stored in separate tables.

Major entities include:

- Customers
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Product Categories
- Date Dimension

Relationships between these entities allow the data to be combined for analytical queries.

---

## 🔍 SQL Analysis

The SQL layer transforms transactional data into business-oriented metrics.

The analysis includes:

- Revenue analysis
- Customer analysis
- Order analysis
- Product and category analysis
- Delivery analysis
- Customer segmentation
- Geographic analysis

The complete queries can be found in:

`sql/analysis.sql`

---

## 📊 Dashboard Design

The Power BI dashboard follows a KPI-driven design.

The top section presents the major business metrics:

**Total Revenue | Total Orders | Total Customers | Average Order Value**

The remaining sections provide visual analysis of:

**Revenue Trends → Category Performance → Customer Segmentation → Delivery Performance**

This allows users to move from high-level business performance to more detailed analysis.

---

## 🚀 How to Run the Project

### Prerequisites

Install the following:

- Python 3.x
- MySQL
- Microsoft Power BI Desktop

Install the required Python libraries using:

    pip install pandas mysql-connector-python

### Step 1: Prepare the Database

Create the MySQL database and tables using:

`sql/schema.sql`

### Step 2: Inspect the Data

Run:

    python python/inspect_data.py

### Step 3: Transform the Data

Run:

    python python/transform.py
    python python/fix_categories.py

### Step 4: Create the Date Dimension

Run:

    python python/create_date_dim.py

### Step 5: Load Data into MySQL

Run:

    python python/load.py

### Step 6: Run SQL Analysis

Execute the queries from:

`sql/analysis.sql`

Create the analytical views using:

`sql/views.sql`

### Step 7: Open the Power BI Dashboard

Open:

`Ecommerce_Business_Analytics.pbix`

Connect Power BI to the MySQL database and refresh the data if required.

---

## 🔐 Environment Variables

Database credentials are stored locally using environment variables and are intentionally excluded from the repository.

Example configuration:

    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=ecommerce_bi

The `.env` file is excluded using `.gitignore` to prevent credentials from being committed to GitHub.

---

## 📌 Project Highlights

- End-to-end data analytics pipeline
- Python-based data preprocessing
- Relational MySQL database design
- SQL-based business analysis
- Analytical SQL views
- Customer segmentation
- Time-based analysis using a date dimension
- Interactive Power BI dashboard
- Git/GitHub version control

---

## 🎯 Skills Demonstrated

### Data Analytics

- Data Cleaning
- Data Transformation
- Exploratory Data Analysis
- Business Analysis
- KPI Development

### SQL

- Joins
- Aggregations
- Grouping
- Filtering
- Subqueries
- Analytical Queries
- SQL Views

### Python

- Pandas
- Data preprocessing
- CSV handling
- MySQL database connectivity
- ETL-style workflows

### Business Intelligence

- Power BI
- Data Modeling
- Dashboard Design
- KPI Cards
- Interactive Visualizations
- Business-oriented Reporting

---

## 📁 Main Files

| File | Description |
|---|---|
| `inspect_data.py` | Inspects and explores the raw datasets |
| `transform.py` | Cleans and transforms datasets |
| `fix_categories.py` | Cleans product category information |
| `load.py` | Loads cleaned datasets into MySQL |
| `create_date_dim.py` | Creates the date dimension |
| `schema.sql` | Defines the database schema |
| `analysis.sql` | Contains business analysis queries |
| `views.sql` | Creates reusable analytical SQL views |
| `Ecommerce_Business_Analytics.pbix` | Power BI dashboard |

---

## 📌 Future Improvements

Potential future improvements include:

- Adding advanced customer lifetime value analysis
- Building additional Power BI dashboard pages
- Adding automated data refresh
- Adding detailed seller performance analysis
- Implementing additional customer retention metrics
- Automating the complete ETL pipeline

---

## 👩‍💻 Author

**Bhoomija**

Computer Science Engineering Student

GitHub: [@bhoomijaa](https://github.com/bhoomijaa)
