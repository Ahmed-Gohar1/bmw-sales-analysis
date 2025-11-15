"""BMW Sales Data - Data Visualizations"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
sns.set_palette("husl")


def main():
    print("Libraries loaded successfully!")
    
    # Load the cleaned dataset
    df = pd.read_csv('../data/BMW_sales_data_cleaned.csv')
    
    print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Ready for visualization!")
    
    # Price distribution
    print("\n=== PRICE AND SALES DISTRIBUTIONS ===")
    plt.figure(figsize=(10, 6))
    plt.hist(df['Price_USD'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Price Distribution', fontsize=12)
    plt.xlabel('Price (USD)')
    plt.ylabel('Count')
    plt.axvline(df['Price_USD'].mean(), color='red', linestyle='--', 
                label=f"Avg: ${df['Price_USD'].mean():,.0f}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.ylim(1500, 1750)
    plt.show()
    
    # Sales volume distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['Sales_Volume'], bins=30, color='lightcoral', edgecolor='black')
    plt.title('Sales Volume Distribution', fontsize=12)
    plt.xlabel('Sales Volume')
    plt.ylabel('Count')
    plt.axvline(df['Sales_Volume'].mean(), color='red', linestyle='--',
                label=f"Avg: {df['Sales_Volume'].mean():,.0f}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.ylim(1500, 1750)
    plt.show()
    
    print(f"Avg Price: ${df['Price_USD'].mean():,.0f} | Avg Sales: {df['Sales_Volume'].mean():,.0f}")
    
    # Category comparison dashboard - 2x2 layout
    print("\n=== CATEGORY COMPARISON DASHBOARD ===")
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Total sales by BMW model (top-left)
    ax1 = plt.subplot(2, 2, 1)
    model_sales = df.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=False)
    ax1.bar(model_sales.index, model_sales.values, color='steelblue', edgecolor='black')
    ax1.set_title('Total Sales by BMW Model', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Model', fontsize=10)
    ax1.set_ylabel('Total Sales Volume', fontsize=10)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim(22000000, 24000000)
    
    # 2. Average price by fuel type (top-right)
    ax2 = plt.subplot(2, 2, 2)
    fuel_price = df.groupby('Fuel_Type')['Price_USD'].mean().sort_values()
    ax2.barh(fuel_price.index, fuel_price.values, color='coral', edgecolor='black')
    ax2.set_title('Average Price by Fuel Type', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Average Price (USD)', fontsize=10)
    ax2.set_ylabel('Fuel Type', fontsize=10)
    ax2.grid(axis='x', alpha=0.3)
    ax2.set_xlim(74000, 76000)
    
    # 3. Sales by region (bottom-left)
    ax3 = plt.subplot(2, 2, 3)
    region_sales = df.groupby('Region')['Sales_Volume'].sum().sort_values()
    ax3.barh(region_sales.index, region_sales.values, color='lightgreen', edgecolor='black')
    ax3.set_title('Total Sales by Region', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Total Sales Volume', fontsize=10)
    ax3.set_ylabel('Region', fontsize=10)
    ax3.grid(axis='x', alpha=0.3)
    ax3.set_xlim(40000000, 44000000)
    
    # 4. Distribution by transmission type (bottom-right)
    ax4 = plt.subplot(2, 2, 4)
    trans_counts = df['Transmission'].value_counts()
    colors_trans = ['#3498db', '#e74c3c']
    ax4.pie(trans_counts, labels=trans_counts.index, autopct='%1.1f%%', 
            colors=colors_trans, startangle=90, textprops={'fontsize': 10})
    ax4.set_title('Transmission Type Distribution', fontsize=12, fontweight='bold')
    
    # Add overall title
    fig.suptitle('BMW Sales - Category Comparison Dashboard', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.show()
    
    print("Category comparison dashboard created")
    print(f"Models analyzed: {df['Model'].nunique()}")
    print(f"Regions covered: {df['Region'].nunique()}")
    print(f"Fuel types: {df['Fuel_Type'].nunique()}")
    
    # Exploring Relationships Between Variables
    print("\n=== TRENDS OVER TIME ===")
    
    # Sales trend over years
    yearly_sales = df.groupby('Year')['Sales_Volume'].sum()
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_sales.index, yearly_sales.values, marker='o', 
             linewidth=2, markersize=6, color='green')
    plt.xlabel('Year')
    plt.ylabel('Total Sales Volume')
    plt.title('Sales Trend Over Years', fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Price trend over years
    yearly_price = df.groupby('Year')['Price_USD'].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_price.index, yearly_price.values, marker='s', 
             linewidth=2, markersize=6, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Average Price (USD)')
    plt.title('Price Trend Over Years', fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Interactive Plotly visualizations
    print("\n=== INTERACTIVE VISUALIZATIONS ===")
    
    # Bar chart showing average price by model
    avg_price_model = df.groupby('Model')['Price_USD'].mean().sort_values(ascending=False).reset_index()
    
    fig = px.bar(avg_price_model, x='Model', y='Price_USD',
                 title='Average Price by BMW Model',
                 labels={'Price_USD': 'Average Price (USD)'},
                 color='Price_USD',
                 color_continuous_scale='Blues')
    fig.update_layout(height=500)
    fig.update_yaxes(range=[74000, 76000])
    fig.show()
    
    # Box plot to compare price distributions
    fig = px.box(df, x='Fuel_Type', y='Price_USD',
                 title='Price Distribution by Fuel Type',
                 labels={'Price_USD': 'Price (USD)', 'Fuel_Type': 'Fuel Type'},
                 color='Fuel_Type')
    fig.update_layout(height=500, showlegend=False)
    fig.show()
    
    # Heatmaps to See Patterns
    print("\n=== HEATMAPS ===")
    
    # Heatmap: Average sales by Model and Region
    heatmap_data = df.pivot_table(values='Sales_Volume', 
                                   index='Model', 
                                   columns='Region', 
                                   aggfunc='mean')
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Avg Sales Volume'})
    plt.title('Average Sales Volume by Model and Region', fontsize=12)
    plt.xlabel('Region')
    plt.ylabel('Model')
    plt.tight_layout()
    plt.show()
    
    print("Observation: This shows which models perform best in each region.")
    
    # Correlation heatmap
    numeric_cols = ['Price_USD', 'Sales_Volume', 'Mileage_KM', 'Engine_Size_L', 'Year']
    correlation = df[numeric_cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('Correlation Between Variables', fontsize=12)
    plt.tight_layout()
    plt.show()
    
    print("How to read: 1=strong positive, -1=strong negative, 0=no relationship")
    
    # Trends Over Time - Fuel type popularity
    print("\n=== FUEL TYPE TRENDS ===")
    fuel_yearly = df.groupby(['Year', 'Fuel_Type']).size().reset_index(name='Count')
    
    fig = px.line(fuel_yearly, x='Year', y='Count', color='Fuel_Type',
                  markers=True, title='Fuel Type Popularity Over Time',
                  labels={'Count': 'Number of Records'})
    fig.update_layout(height=500)
    fig.show()
    
    # Which models have been most popular over time?
    top_3_models = df['Model'].value_counts().head(3).index
    model_yearly = df[df['Model'].isin(top_3_models)].groupby(['Year', 'Model']).size().reset_index(name='Count')
    
    fig = px.line(model_yearly, x='Year', y='Count', color='Model',
                  markers=True, title='Popularity of Top 3 Models Over Time',
                  labels={'Count': 'Number of Records'})
    fig.update_layout(height=500)
    fig.show()
    
    # Regional Comparison
    print("\n=== REGIONAL COMPARISON ===")
    
    # Compare regions on multiple metrics
    region_summary = df.groupby('Region').agg({
        'Sales_Volume': 'sum',
        'Price_USD': 'mean',
        'Model': 'count'
    }).reset_index()
    region_summary.columns = ['Region', 'Total_Sales', 'Avg_Price', 'Number_of_Records']
    
    # Total sales by region
    plt.figure(figsize=(10, 6))
    plt.barh(region_summary['Region'], region_summary['Total_Sales'], color='steelblue')
    plt.xlabel('Total Sales Volume')
    plt.title('Total Sales by Region', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.xlim(41000000, 44000000)
    plt.show()
    
    # Average price by region
    plt.figure(figsize=(10, 6))
    plt.barh(region_summary['Region'], region_summary['Avg_Price'], color='coral')
    plt.xlabel('Average Price (USD)')
    plt.title('Average Price by Region', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.xlim(74000, 76000)
    plt.show()
    
    # Number of records (market presence)
    plt.figure(figsize=(10, 6))
    plt.barh(region_summary['Region'], region_summary['Number_of_Records'], color='lightgreen')
    plt.xlabel('Number of Records')
    plt.title('Market Presence by Region', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.xlim(8200, 8600)
    plt.show()
    
    # Comparing High vs Low Sales Performance
    print("\n=== HIGH VS LOW SALES COMPARISON ===")
    
    # Compare high vs low sales performance
    high_sales = df[df['Sales_Classification'] == 'High']
    low_sales = df[df['Sales_Classification'] == 'Low']
    
    # Price comparison
    plt.figure(figsize=(10, 6))
    plt.hist([high_sales['Price_USD'], low_sales['Price_USD']], 
             bins=30, label=['High Sales', 'Low Sales'], color=['green', 'red'], alpha=0.6)
    plt.xlabel('Price (USD)')
    plt.title('Price: High vs Low Sales', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Sales volume comparison
    plt.figure(figsize=(10, 6))
    plt.hist([high_sales['Sales_Volume'], low_sales['Sales_Volume']], 
             bins=30, label=['High Sales', 'Low Sales'], color=['green', 'red'], alpha=0.6)
    plt.xlabel('Sales Volume')
    plt.title('Volume: High vs Low Sales', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"High Sales Avg Price: ${high_sales['Price_USD'].mean():,.0f}")
    print(f"Low Sales Avg Price: ${low_sales['Price_USD'].mean():,.0f}")
    
    # Final Summary Dashboard
    print("\n=== EXECUTIVE SUMMARY DASHBOARD ===")
    
    # Summary dashboard with key metrics in a 2x2 layout
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Top 5 models by sales (top-left)
    ax1 = plt.subplot(2, 2, 1)
    top_models = df.groupby('Model')['Sales_Volume'].sum().nlargest(5)
    ax1.barh(top_models.index, top_models.values, color='steelblue')
    ax1.set_xlabel('Total Sales Volume', fontsize=10)
    ax1.set_title('Top 5 Best Selling Models', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    ax1.set_xlim(23000000, 24000000)
    
    # 2. Sales by region (top-right, pie chart)
    ax2 = plt.subplot(2, 2, 2)
    region_sales = df.groupby('Region')['Sales_Volume'].sum()
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
    ax2.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', 
            startangle=90, colors=colors[:len(region_sales)])
    ax2.set_title('Sales Distribution by Region', fontsize=12, fontweight='bold')
    
    # 3. Average price by fuel type (bottom-left)
    ax3 = plt.subplot(2, 2, 3)
    fuel_price = df.groupby('Fuel_Type')['Price_USD'].mean().sort_values()
    ax3.barh(fuel_price.index, fuel_price.values, color='coral')
    ax3.set_xlabel('Average Price (USD)', fontsize=10)
    ax3.set_title('Average Price by Fuel Type', fontsize=12, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    ax3.set_xlim(74000, 76000)
    
    # 4. Sales trend over years (bottom-right)
    ax4 = plt.subplot(2, 2, 4)
    yearly = df.groupby('Year')['Sales_Volume'].sum()
    ax4.plot(yearly.index, yearly.values, marker='o', linewidth=2.5, 
             markersize=8, color='green')
    ax4.set_xlabel('Year', fontsize=10)
    ax4.set_ylabel('Total Sales', fontsize=10)
    ax4.set_title('Sales Trend (2010-2024)', fontsize=12, fontweight='bold')
    ax4.grid(alpha=0.3)
    
    # Add overall title
    fig.suptitle('BMW Sales Analysis - Executive Dashboard', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.show()
    
    print("Dashboard created with 4 key visualizations")
    print(f"Dataset: {len(df):,} records analyzed")
    print(f"Time period: {df['Year'].min()}-{df['Year'].max()}")
    print(f"Total sales volume: {df['Sales_Volume'].sum():,.0f}")


if __name__ == "__main__":
    main()
