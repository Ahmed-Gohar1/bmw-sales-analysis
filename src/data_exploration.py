"""BMW Sales Data - Data Exploration"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 5)


def main():
    print("All libraries loaded successfully!")
    
    # Load the data
    df = pd.read_csv('../data/BMW_sales_data.csv')
    print(f"\nDataset loaded successfully!")
    print(f"Shape: {df.shape[0]} rows and {df.shape[1]} columns")
    
    # Display first few rows
    print("\nFirst 10 rows of the dataset:")
    print(df.head(10))
    
    # Display last few rows
    print("\nLast 5 rows of the dataset:")
    print(df.tail())
    
    # Get basic information about the dataset
    print("\nDataset Information:")
    df.info()
    
    # Check column names and their data types
    print("\nColumn Names and Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"{col:25} : {dtype}")
    
    # Check for missing values
    print("\nMissing Values Count:")
    missing_counts = df.isnull().sum()
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Missing Count': missing_counts,
        'Percentage': missing_percentage
    })
    
    print(missing_df[missing_df['Missing Count'] > 0])
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")
    print(f"Percentage of duplicates: {(duplicates/len(df))*100:.2f}%")
    
    # Check unique values for categorical columns
    categorical_cols = df.select_dtypes(include='object').columns
    
    print("\nUnique values in categorical columns:")
    for col in categorical_cols:
        print(f"\n{col}: {df[col].nunique()} unique values")
        print(df[col].unique())
    
    # Statistical summary for numeric columns
    print("\nStatistical Summary - Numeric Columns:")
    print(df.describe().round(2))
    
    # Statistical summary for categorical columns
    print("\nStatistical Summary - Categorical Columns:")
    print(df.describe(include='object'))
    
    # Basic statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    print("\nStatistics for Numeric Columns:")
    for col in numeric_cols:
        print(f"\n{col}:")
        print(f"  Mean: {df[col].mean():.2f}")
        print(f"  Median: {df[col].median():.2f}")
        print(f"  Min: {df[col].min():.2f}, Max: {df[col].max():.2f}")
    
    # Count of records by Model
    print("\nDistribution by BMW Model:")
    model_counts = df['Model'].value_counts()
    print(model_counts)
    
    plt.figure(figsize=(10, 6))
    model_counts.plot(kind='bar', color='steelblue', edgecolor='black')
    plt.title('Number of Sales Records by BMW Model', fontsize=14, fontweight='bold')
    plt.xlabel('Model')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.ylim(4400, 4800)
    plt.show()
    
    # Distribution by Region
    print("\nDistribution by Region:")
    region_counts = df['Region'].value_counts()
    print(region_counts)
    
    plt.figure(figsize=(10, 6))
    region_counts.plot(kind='barh', color='coral', edgecolor='black')
    plt.title('Number of Sales Records by Region', fontsize=14, fontweight='bold')
    plt.xlabel('Count')
    plt.ylabel('Region')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.xlim(8200, 8500)
    plt.show()
    
    # Distribution by Fuel Type
    print("\nDistribution by Fuel Type:")
    fuel_counts = df['Fuel_Type'].value_counts()
    print(fuel_counts)
    
    plt.figure(figsize=(8, 8))
    plt.pie(fuel_counts, labels=fuel_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette('Set2'))
    plt.title('Distribution of Fuel Types', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    # Distribution by Transmission Type
    print("\nDistribution by Transmission:")
    trans_counts = df['Transmission'].value_counts()
    print(trans_counts)
    
    plt.figure(figsize=(8, 6))
    trans_counts.plot(kind='bar', color=['#2ecc71', '#e74c3c'], edgecolor='black')
    plt.title('Distribution of Transmission Types', fontsize=14, fontweight='bold')
    plt.xlabel('Transmission Type')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.ylim(24000, 26000)
    plt.show()
    
    # Distribution by Sales Classification
    print("\nDistribution by Sales Classification:")
    sales_class_counts = df['Sales_Classification'].value_counts()
    print(sales_class_counts)
    
    plt.figure(figsize=(8, 6))
    sales_class_counts.plot(kind='bar', color=['#3498db', '#e67e22'], edgecolor='black')
    plt.title('Distribution of Sales Classification', fontsize=14, fontweight='bold')
    plt.xlabel('Sales Classification')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Quick Insights
    print("\nKEY FINDINGS\n")
    
    print(f"• Total records: {len(df):,}")
    print(f"• Missing values: {df.isnull().sum().sum()}")
    print(f"• BMW models: {df['Model'].nunique()}")
    print(f"• Most common model: {df['Model'].mode()[0]}")
    print(f"• Price range: ${df['Price_USD'].min():,.0f} - ${df['Price_USD'].max():,.0f}")
    print(f"• Average price: ${df['Price_USD'].mean():,.0f}")
    print(f"• Years covered: {df['Year'].min()} - {df['Year'].max()}")


if __name__ == "__main__":
    main()
