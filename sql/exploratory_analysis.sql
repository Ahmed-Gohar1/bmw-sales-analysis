WITH dataset_summary AS (
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT Model) as unique_models,
        COUNT(DISTINCT Region) as unique_regions,
        COUNT(DISTINCT Fuel_Type) as unique_fuel_types,
        COUNT(DISTINCT Transmission) as unique_transmissions,
        MIN(Year) as earliest_year,
        MAX(Year) as latest_year
    FROM bmw_sales
)
SELECT * FROM dataset_summary;

WITH missing_values AS (
    SELECT 
        'Model' as column_name,
        COUNT(*) - COUNT(Model) as null_count,
        ROUND(100.0 * (COUNT(*) - COUNT(Model)) / COUNT(*), 2) as null_percentage
    FROM bmw_sales
    
    UNION ALL
    
    SELECT 
        'Year',
        COUNT(*) - COUNT(Year),
        ROUND(100.0 * (COUNT(*) - COUNT(Year)) / COUNT(*), 2)
    FROM bmw_sales
    
    UNION ALL
    
    SELECT 
        'Price_USD',
        COUNT(*) - COUNT(Price_USD),
        ROUND(100.0 * (COUNT(*) - COUNT(Price_USD)) / COUNT(*), 2)
    FROM bmw_sales
    
    UNION ALL
    
    SELECT 
        'Sales_Volume',
        COUNT(*) - COUNT(Sales_Volume),
        ROUND(100.0 * (COUNT(*) - COUNT(Sales_Volume)) / COUNT(*), 2)
    FROM bmw_sales
    
    UNION ALL
    
    SELECT 
        'Mileage_KM',
        COUNT(*) - COUNT(Mileage_KM),
        ROUND(100.0 * (COUNT(*) - COUNT(Mileage_KM)) / COUNT(*), 2)
    FROM bmw_sales
    
    UNION ALL
    
    SELECT 
        'Engine_Size_L',
        COUNT(*) - COUNT(Engine_Size_L),
        ROUND(100.0 * (COUNT(*) - COUNT(Engine_Size_L)) / COUNT(*), 2)
    FROM bmw_sales
)
SELECT * FROM missing_values
WHERE null_count > 0
ORDER BY null_count DESC;

WITH record_counts AS (
    SELECT 
        Model,
        Year,
        Region,
        Fuel_Type,
        Transmission,
        Price_USD,
        COUNT(*) as duplicate_count
    FROM bmw_sales
    GROUP BY Model, Year, Region, Fuel_Type, Transmission, Price_USD
    HAVING COUNT(*) > 1
)
SELECT 
    COUNT(*) as groups_with_duplicates,
    SUM(duplicate_count) as total_duplicate_records
FROM record_counts;

WITH price_stats AS (
    SELECT 
        'Price_USD' as metric,
        MIN(Price_USD) as min_value,
        AVG(Price_USD) as avg_value,
        MAX(Price_USD) as max_value,
        STDDEV(Price_USD) as std_dev
    FROM bmw_sales
),
sales_stats AS (
    SELECT 
        'Sales_Volume' as metric,
        MIN(Sales_Volume) as min_value,
        AVG(Sales_Volume) as avg_value,
        MAX(Sales_Volume) as max_value,
        STDDEV(Sales_Volume) as std_dev
    FROM bmw_sales
),
mileage_stats AS (
    SELECT 
        'Mileage_KM' as metric,
        MIN(Mileage_KM) as min_value,
        AVG(Mileage_KM) as avg_value,
        MAX(Mileage_KM) as max_value,
        STDDEV(Mileage_KM) as std_dev
    FROM bmw_sales
),
engine_stats AS (
    SELECT 
        'Engine_Size_L' as metric,
        MIN(Engine_Size_L) as min_value,
        AVG(Engine_Size_L) as avg_value,
        MAX(Engine_Size_L) as max_value,
        STDDEV(Engine_Size_L) as std_dev
    FROM bmw_sales
)
SELECT * FROM price_stats
UNION ALL SELECT * FROM sales_stats
UNION ALL SELECT * FROM mileage_stats
UNION ALL SELECT * FROM engine_stats;

WITH model_distribution AS (
    SELECT 
        'Model' as category,
        Model as value,
        COUNT(*) as record_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
    FROM bmw_sales
    GROUP BY Model
)
SELECT * FROM model_distribution
ORDER BY record_count DESC;

WITH region_distribution AS (
    SELECT 
        'Region' as category,
        Region as value,
        COUNT(*) as record_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
    FROM bmw_sales
    GROUP BY Region
)
SELECT * FROM region_distribution
ORDER BY record_count DESC;

WITH fuel_distribution AS (
    SELECT 
        'Fuel_Type' as category,
        Fuel_Type as value,
        COUNT(*) as record_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
    FROM bmw_sales
    GROUP BY Fuel_Type
)
SELECT * FROM fuel_distribution
ORDER BY record_count DESC;

WITH price_quartiles AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Price_USD) as Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Price_USD) as Q3
    FROM bmw_sales
),
price_bounds AS (
    SELECT 
        Q1,
        Q3,
        Q3 - Q1 as IQR,
        Q1 - 1.5 * (Q3 - Q1) as lower_bound,
        Q3 + 1.5 * (Q3 - Q1) as upper_bound
    FROM price_quartiles
),
outliers AS (
    SELECT 
        Model,
        Year,
        Price_USD,
        CASE 
            WHEN Price_USD < (SELECT lower_bound FROM price_bounds) THEN 'Below Lower Bound'
            WHEN Price_USD > (SELECT upper_bound FROM price_bounds) THEN 'Above Upper Bound'
        END as outlier_type
    FROM bmw_sales
    WHERE Price_USD < (SELECT lower_bound FROM price_bounds)
       OR Price_USD > (SELECT upper_bound FROM price_bounds)
)
SELECT 
    outlier_type,
    COUNT(*) as outlier_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM bmw_sales), 2) as percentage
FROM outliers
GROUP BY outlier_type;

WITH sales_ranges AS (
    SELECT 
        CASE 
            WHEN Sales_Volume < 3000 THEN '0-3K'
            WHEN Sales_Volume < 5000 THEN '3K-5K'
            WHEN Sales_Volume < 7000 THEN '5K-7K'
            ELSE '7K+'
        END as sales_range,
        Sales_Volume,
        Price_USD,
        Model
    FROM bmw_sales
),
range_summary AS (
    SELECT 
        sales_range,
        COUNT(*) as record_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
        AVG(Price_USD) as avg_price,
        COUNT(DISTINCT Model) as unique_models
    FROM sales_ranges
    GROUP BY sales_range
)
SELECT * FROM range_summary
ORDER BY 
    CASE sales_range
        WHEN '0-3K' THEN 1
        WHEN '3K-5K' THEN 2
        WHEN '5K-7K' THEN 3
        WHEN '7K+' THEN 4
    END;

WITH yearly_counts AS (
    SELECT 
        Year,
        COUNT(*) as record_count,
        COUNT(DISTINCT Model) as unique_models,
        AVG(Price_USD) as avg_price,
        AVG(Sales_Volume) as avg_sales
    FROM bmw_sales
    GROUP BY Year
)
SELECT 
    Year,
    record_count,
    unique_models,
    ROUND(avg_price, 2) as avg_price,
    ROUND(avg_sales, 2) as avg_sales
FROM yearly_counts
ORDER BY Year;

WITH model_region_matrix AS (
    SELECT 
        Model,
        Region,
        COUNT(*) as record_count,
        AVG(Sales_Volume) as avg_sales
    FROM bmw_sales
    GROUP BY Model, Region
),
model_coverage AS (
    SELECT 
        Model,
        COUNT(DISTINCT Region) as regions_covered,
        SUM(record_count) as total_records
    FROM model_region_matrix
    GROUP BY Model
)
SELECT 
    Model,
    regions_covered,
    total_records,
    CASE 
        WHEN regions_covered = (SELECT COUNT(DISTINCT Region) FROM bmw_sales) 
        THEN 'Full Coverage'
        ELSE 'Partial Coverage'
    END as coverage_status
FROM model_coverage
ORDER BY regions_covered DESC, total_records DESC;

WITH price_sales_segments AS (
    SELECT 
        CASE 
            WHEN Price_USD < 60000 THEN 'Low Price'
            WHEN Price_USD < 90000 THEN 'Medium Price'
            ELSE 'High Price'
        END as price_segment,
        CASE 
            WHEN Sales_Volume < 4000 THEN 'Low Sales'
            WHEN Sales_Volume < 6000 THEN 'Medium Sales'
            ELSE 'High Sales'
        END as sales_segment,
        Price_USD,
        Sales_Volume
    FROM bmw_sales
),
segment_counts AS (
    SELECT 
        price_segment,
        sales_segment,
        COUNT(*) as record_count,
        AVG(Price_USD) as avg_price,
        AVG(Sales_Volume) as avg_sales
    FROM price_sales_segments
    GROUP BY price_segment, sales_segment
)
SELECT 
    price_segment,
    sales_segment,
    record_count,
    ROUND(avg_price, 2) as avg_price,
    ROUND(avg_sales, 2) as avg_sales
FROM segment_counts
ORDER BY price_segment, sales_segment;

WITH engine_fuel_analysis AS (
    SELECT 
        Fuel_Type,
        COUNT(*) as record_count,
        MIN(Engine_Size_L) as min_engine,
        AVG(Engine_Size_L) as avg_engine,
        MAX(Engine_Size_L) as max_engine,
        AVG(Price_USD) as avg_price
    FROM bmw_sales
    GROUP BY Fuel_Type
)
SELECT 
    Fuel_Type,
    record_count,
    ROUND(min_engine, 2) as min_engine,
    ROUND(avg_engine, 2) as avg_engine,
    ROUND(max_engine, 2) as max_engine,
    ROUND(avg_price, 2) as avg_price
FROM engine_fuel_analysis
ORDER BY avg_engine DESC;

WITH sample_records AS (
    SELECT 
        Model,
        Year,
        Price_USD,
        Sales_Volume,
        Region,
        Fuel_Type,
        Transmission,
        ROW_NUMBER() OVER (ORDER BY RANDOM()) as rn
    FROM bmw_sales
)
SELECT 
    Model,
    Year,
    Price_USD,
    Sales_Volume,
    Region,
    Fuel_Type,
    Transmission
FROM sample_records
WHERE rn <= 10;
