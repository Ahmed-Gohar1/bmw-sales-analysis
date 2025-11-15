"""BMW Sales Data - Statistical Analysis"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, f_oneway, chi2_contingency
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 5)


def main():
    print("Libraries loaded")
    
    # Load the cleaned dataset
    df = pd.read_csv('../data/BMW_sales_data_cleaned.csv')
    
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nFirst few rows:")
    print(df.head())
    
    # Correlation Analysis
    print("\n=== CORRELATION ANALYSIS ===")
    numeric_cols = ['Price_USD', 'Sales_Volume', 'Mileage_KM', 'Engine_Size_L', 'Vehicle_Age']
    
    correlation_matrix = df[numeric_cols].corr()
    
    print("Correlation between variables:")
    print(correlation_matrix.round(2))
    print("\nNote: 1.0 = perfect positive relationship, -1.0 = perfect negative relationship")
    
    # Visualize the relationships with a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('How Variables Relate to Each Other', fontsize=12)
    plt.tight_layout()
    plt.show()
    
    # Price Analysis - Average price by Model
    print("\n=== PRICE ANALYSIS ===")
    price_by_model = df.groupby('Model')['Price_USD'].agg(['mean', 'median', 'std', 'count']).round(2)
    price_by_model = price_by_model.sort_values('mean', ascending=False)
    
    print("Average Price by Model:")
    print(price_by_model)
    
    # Visualize price distribution by model
    plt.figure(figsize=(12, 6))
    df.boxplot(column='Price_USD', by='Model', figsize=(12, 6), patch_artist=True)
    plt.suptitle('')
    plt.title('Price Distribution by BMW Model', fontsize=14, fontweight='bold')
    plt.xlabel('Model')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Average price by Region
    price_by_region = df.groupby('Region')['Price_USD'].agg(['mean', 'median', 'count']).round(2)
    price_by_region = price_by_region.sort_values('mean', ascending=False)
    
    print("\nAverage Price by Region:")
    print(price_by_region)
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    price_by_region['mean'].plot(kind='barh', color='teal', edgecolor='black', ax=ax)
    ax.set_xlabel('Average Price (USD)')
    ax.set_ylabel('Region')
    ax.set_title('Average Price by Region', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.xlim(74000, 76000)
    plt.show()
    
    # Price analysis by Fuel Type
    price_by_fuel = df.groupby('Fuel_Type')['Price_USD'].agg(['mean', 'median', 'count']).round(2)
    price_by_fuel = price_by_fuel.sort_values('mean', ascending=False)
    
    print("\nAverage Price by Fuel Type:")
    print(price_by_fuel)
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    price_by_fuel['mean'].plot(kind='bar', color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'], 
                               edgecolor='black', ax=ax)
    ax.set_xlabel('Fuel Type')
    ax.set_ylabel('Average Price (USD)')
    ax.set_title('Average Price by Fuel Type', fontsize=14, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.ylim(74000, 76000)
    plt.show()
    
    # Sales Volume Analysis
    print("\n=== SALES VOLUME ANALYSIS ===")
    sales_by_model = df.groupby('Model')['Sales_Volume'].agg([
        ('Total_Sales', 'sum'),
        ('Avg_Sales', 'mean'),
        ('Records', 'count')
    ]).round(2)
    sales_by_model = sales_by_model.sort_values('Total_Sales', ascending=False)
    
    print("Sales Volume by Model:")
    print(sales_by_model)
    
    # Visualize total sales by model
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Total sales
    sales_by_model['Total_Sales'].plot(kind='bar', color='steelblue', edgecolor='black', ax=axes[0])
    axes[0].set_title('Total Sales Volume by Model', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Model')
    axes[0].set_ylabel('Total Sales Volume')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].set_ylim(21000000, 24000000)
    
    # Average sales
    sales_by_model['Avg_Sales'].plot(kind='bar', color='coral', edgecolor='black', ax=axes[1])
    axes[1].set_title('Average Sales Volume by Model', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Model')
    axes[1].set_ylabel('Average Sales Volume')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].set_ylim(4900, 5200)
    
    plt.tight_layout()
    plt.show()
    
    # Sales by Region
    sales_by_region = df.groupby('Region')['Sales_Volume'].agg([
        ('Total_Sales', 'sum'),
        ('Avg_Sales', 'mean')
    ]).round(2)
    sales_by_region = sales_by_region.sort_values('Total_Sales', ascending=False)
    
    print("\nSales Volume by Region:")
    print(sales_by_region)
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    sales_by_region['Total_Sales'].plot(kind='barh', color='mediumseagreen', edgecolor='black', ax=ax)
    ax.set_xlabel('Total Sales Volume')
    ax.set_ylabel('Region')
    ax.set_title('Total Sales Volume by Region', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.xlim(41000000, 44000000)
    plt.show()
    
    # Hypothesis Testing
    print("\n=== HYPOTHESIS TESTING ===")
    
    # Hypothesis 1: Price difference between Automatic and Manual
    print("\nHypothesis 1: Is there a significant difference in price between Automatic and Manual transmissions?")
    automatic_prices = df[df['Transmission'] == 'Automatic']['Price_USD']
    manual_prices = df[df['Transmission'] == 'Manual']['Price_USD']
    
    t_stat, p_value = ttest_ind(automatic_prices, manual_prices)
    
    print("Testing: Price difference between Automatic vs Manual")
    print(f"• Automatic avg: ${automatic_prices.mean():,.0f}")
    print(f"• Manual avg: ${manual_prices.mean():,.0f}")
    print(f"• P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("→ YES, there's a significant difference!")
    else:
        print("→ No significant difference")
    
    # Hypothesis 2: Sales volume across fuel types
    print("\nHypothesis 2: Is there a significant difference in sales volume across different fuel types?")
    fuel_groups = [df[df['Fuel_Type'] == ft]['Sales_Volume'] for ft in df['Fuel_Type'].unique()]
    
    f_stat, p_value = f_oneway(*fuel_groups)
    
    print("Testing: Sales volume across fuel types")
    for fuel_type in df['Fuel_Type'].unique():
        sales = df[df['Fuel_Type'] == fuel_type]['Sales_Volume']
        print(f"• {fuel_type}: {sales.mean():,.0f} avg sales")
    
    print(f"\nP-value: {p_value:.4f}")
    if p_value < 0.05:
        print("→ YES, fuel type affects sales!")
    else:
        print("→ No significant difference")
    
    # Hypothesis 3: Sales Classification and Region
    print("\nHypothesis 3: Is there a significant relationship between Sales Classification and Region?")
    contingency_table = pd.crosstab(df['Sales_Classification'], df['Region'])
    
    print("Sales Classification vs Region:")
    print(contingency_table)
    
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    
    print(f"\nP-value: {p_value:.4f}")
    if p_value < 0.05:
        print("→ YES, sales classification depends on region!")
    else:
        print("→ No significant relationship")
    
    # Temporal Analysis
    print("\n=== TEMPORAL ANALYSIS ===")
    yearly_trends = df.groupby('Year').agg({
        'Sales_Volume': 'sum',
        'Price_USD': 'mean'
    }).round(0)
    
    print("Yearly Trends:")
    print(yearly_trends)
    
    # Visualize trends over time
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Sales volume trend
    axes[0].plot(yearly_trends.index, yearly_trends['Sales_Volume'], 
                 marker='o', linewidth=2, markersize=8, color='steelblue')
    axes[0].set_title('Total Sales Volume by Year', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Total Sales Volume')
    axes[0].grid(alpha=0.3)
    
    # Average price trend
    axes[1].plot(yearly_trends.index, yearly_trends['Price_USD'], 
                 marker='s', linewidth=2, markersize=8, color='coral')
    axes[1].set_title('Average Price by Year', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Average Price (USD)')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Model Category Analysis
    print("\n=== MODEL CATEGORY ANALYSIS ===")
    category_analysis = df.groupby('Model_Category').agg({
        'Sales_Volume': 'sum',
        'Price_USD': 'mean'
    }).round(0)
    
    print("Sales and Price by Model Category:")
    print(category_analysis)
    
    # Visualize model category comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Sales comparison
    category_analysis['Sales_Volume'].plot(kind='bar', color='teal', edgecolor='black', ax=axes[0])
    axes[0].set_title('Total Sales by Model Category', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Model Category')
    axes[0].set_ylabel('Total Sales Volume')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.3)
    
    # Price comparison
    category_analysis['Price_USD'].plot(kind='bar', color='orange', edgecolor='black', ax=axes[1])
    axes[1].set_title('Average Price by Model Category', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Model Category')
    axes[1].set_ylabel('Average Price (USD)')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].set_ylim(74000, 76000)
    
    plt.tight_layout()
    plt.show()
    
    # Key Statistical Insights Summary
    print("\n=== KEY FINDINGS ===\n")
    
    print(f"• Average price: ${df['Price_USD'].mean():,.0f}")
    print(f"• Most expensive model: {price_by_model.index[0]} (${price_by_model.iloc[0]['mean']:,.0f})")
    print(f"• Best seller: {sales_by_model.index[0]} ({sales_by_model.iloc[0]['Total_Sales']:,.0f} units)")
    print(f"• Top region: {sales_by_region.index[0]}")
    
    fuel_pref = df['Fuel_Type'].value_counts()
    trans_pref = df['Transmission'].value_counts()
    print(f"• Popular fuel: {fuel_pref.index[0]} ({fuel_pref.iloc[0]} records)")
    print(f"• Popular transmission: {trans_pref.index[0]}")


if __name__ == "__main__":
    main()
