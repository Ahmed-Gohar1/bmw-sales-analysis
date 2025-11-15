WITH sales_by_model AS (
    SELECT 
        Model,
        COUNT(*) as total_records,
        SUM(Sales_Volume) as total_sales,
        AVG(Sales_Volume) as avg_sales,
        AVG(Price_USD) as avg_price,
        MIN(Price_USD) as min_price,
        MAX(Price_USD) as max_price
    FROM bmw_sales
    GROUP BY Model
),
ranked_models AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY total_sales DESC) as sales_rank,
        RANK() OVER (ORDER BY avg_price DESC) as price_rank
    FROM sales_by_model
)
SELECT 
    Model,
    total_records,
    total_sales,
    avg_sales,
    avg_price,
    sales_rank,
    price_rank
FROM ranked_models
ORDER BY total_sales DESC;

WITH regional_metrics AS (
    SELECT 
        Region,
        COUNT(*) as total_records,
        SUM(Sales_Volume) as total_sales,
        AVG(Sales_Volume) as avg_sales_volume,
        AVG(Price_USD) as avg_price,
        COUNT(DISTINCT Model) as unique_models
    FROM bmw_sales
    GROUP BY Region
),
region_with_share AS (
    SELECT 
        *,
        ROUND(100.0 * total_sales / SUM(total_sales) OVER (), 2) as market_share_pct
    FROM regional_metrics
)
SELECT 
    Region,
    total_records,
    total_sales,
    avg_sales_volume,
    avg_price,
    unique_models,
    market_share_pct
FROM region_with_share
ORDER BY total_sales DESC;

WITH model_region_sales AS (
    SELECT 
        Region,
        Model,
        SUM(Sales_Volume) as total_sales,
        AVG(Price_USD) as avg_price,
        COUNT(*) as num_records
    FROM bmw_sales
    GROUP BY Region, Model
),
ranked_by_region AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY Region ORDER BY total_sales DESC) as region_rank
    FROM model_region_sales
)
SELECT 
    Region,
    Model,
    total_sales,
    avg_price,
    num_records,
    region_rank
FROM ranked_by_region
WHERE region_rank <= 3
ORDER BY Region, region_rank;

WITH fuel_metrics AS (
    SELECT 
        Fuel_Type,
        COUNT(*) as total_records,
        SUM(Sales_Volume) as total_sales,
        AVG(Sales_Volume) as avg_sales,
        AVG(Price_USD) as avg_price,
        AVG(Engine_Size_L) as avg_engine_size
    FROM bmw_sales
    GROUP BY Fuel_Type
),
fuel_with_share AS (
    SELECT 
        *,
        ROUND(100.0 * total_records / SUM(total_records) OVER (), 2) as record_share_pct,
        ROUND(100.0 * total_sales / SUM(total_sales) OVER (), 2) as sales_share_pct
    FROM fuel_metrics
)
SELECT 
    Fuel_Type,
    total_records,
    record_share_pct,
    total_sales,
    sales_share_pct,
    avg_price,
    avg_engine_size
FROM fuel_with_share
ORDER BY total_sales DESC;

WITH transmission_metrics AS (
    SELECT 
        Transmission,
        COUNT(*) as total_records,
        SUM(Sales_Volume) as total_sales,
        AVG(Price_USD) as avg_price,
        AVG(Mileage_KM) as avg_mileage
    FROM bmw_sales
    GROUP BY Transmission
)
SELECT 
    Transmission,
    total_records,
    ROUND(100.0 * total_records / SUM(total_records) OVER (), 2) as pct_of_total,
    total_sales,
    avg_price,
    avg_mileage
FROM transmission_metrics
ORDER BY total_sales DESC;

WITH yearly_metrics AS (
    SELECT 
        Year,
        COUNT(*) as total_records,
        SUM(Sales_Volume) as total_sales,
        AVG(Price_USD) as avg_price,
        COUNT(DISTINCT Model) as unique_models
    FROM bmw_sales
    GROUP BY Year
),
year_over_year AS (
    SELECT 
        *,
        LAG(total_sales) OVER (ORDER BY Year) as prev_year_sales,
        LAG(avg_price) OVER (ORDER BY Year) as prev_year_price
    FROM yearly_metrics
)
SELECT 
    Year,
    total_records,
    total_sales,
    prev_year_sales,
    CASE 
        WHEN prev_year_sales IS NOT NULL 
        THEN ROUND(100.0 * (total_sales - prev_year_sales) / prev_year_sales, 2)
        ELSE NULL 
    END as sales_growth_pct,
    avg_price,
    CASE 
        WHEN prev_year_price IS NOT NULL 
        THEN ROUND(100.0 * (avg_price - prev_year_price) / prev_year_price, 2)
        ELSE NULL 
    END as price_growth_pct,
    unique_models
FROM year_over_year
ORDER BY Year;

WITH classification_metrics AS (
    SELECT 
        Sales_Classification,
        COUNT(*) as total_records,
        AVG(Sales_Volume) as avg_sales_volume,
        AVG(Price_USD) as avg_price,
        AVG(Mileage_KM) as avg_mileage
    FROM bmw_sales
    GROUP BY Sales_Classification
)
SELECT 
    Sales_Classification,
    total_records,
    ROUND(100.0 * total_records / SUM(total_records) OVER (), 2) as pct_distribution,
    avg_sales_volume,
    avg_price,
    avg_mileage
FROM classification_metrics
ORDER BY Sales_Classification;

WITH price_segments AS (
    SELECT 
        CASE 
            WHEN Price_USD < 50000 THEN 'Budget (<50K)'
            WHEN Price_USD < 80000 THEN 'Mid-Range (50-80K)'
            WHEN Price_USD < 110000 THEN 'Premium (80-110K)'
            ELSE 'Luxury (110K+)'
        END as price_segment,
        Sales_Volume,
        Price_USD,
        Model
    FROM bmw_sales
),
segment_metrics AS (
    SELECT 
        price_segment,
        COUNT(*) as total_records,
        SUM(Sales_Volume) as total_sales,
        AVG(Sales_Volume) as avg_sales,
        AVG(Price_USD) as avg_price,
        COUNT(DISTINCT Model) as unique_models
    FROM price_segments
    GROUP BY price_segment
)
SELECT 
    price_segment,
    total_records,
    total_sales,
    avg_sales,
    avg_price,
    unique_models
FROM segment_metrics
ORDER BY avg_price;

WITH model_fuel_matrix AS (
    SELECT 
        Model,
        Fuel_Type,
        COUNT(*) as records,
        SUM(Sales_Volume) as total_sales,
        AVG(Price_USD) as avg_price
    FROM bmw_sales
    GROUP BY Model, Fuel_Type
)
SELECT 
    Model,
    Fuel_Type,
    records,
    total_sales,
    avg_price
FROM model_fuel_matrix
ORDER BY Model, total_sales DESC;

WITH revenue_analysis AS (
    SELECT 
        Model,
        Region,
        Fuel_Type,
        COUNT(*) as num_records,
        SUM(Sales_Volume * Price_USD) as estimated_revenue,
        AVG(Price_USD) as avg_price,
        SUM(Sales_Volume) as total_sales
    FROM bmw_sales
    GROUP BY Model, Region, Fuel_Type
),
ranked_revenue AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY estimated_revenue DESC) as revenue_rank
    FROM revenue_analysis
)
SELECT 
    Model,
    Region,
    Fuel_Type,
    num_records,
    estimated_revenue,
    avg_price,
    total_sales,
    revenue_rank
FROM ranked_revenue
WHERE revenue_rank <= 10
ORDER BY revenue_rank;
