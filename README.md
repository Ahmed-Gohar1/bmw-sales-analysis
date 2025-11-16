# E-Commerce Analytics

SQL project for analyzing e-commerce transactions using PostgreSQL. Includes a normalized 3NF schema, raw-to-clean data transformation, and 20 business intelligence queries using CTEs and window functions.

## How to use
- Run schema setup: `psql -d ecommerce_db -f sql/01_schema_setup.sql`
- Run analysis queries: `psql -d ecommerce_db -f sql/02_business_analysis.sql`
- View ERD: `docs/database_schema.png`
- Place CSV data in: `data/`

## Project Structure
- `sql/` — schema setup + 20 BI queries  
- `docs/` — ERD diagram and documentation  
- `data/` — raw CSV data  
- `Documentation/` — README + quick start  
- `LICENSE` — MIT license  
