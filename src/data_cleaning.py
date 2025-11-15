"""BMW Sales Data - Data Cleaning"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
sns.set_style('whitegrid')


def main():
    print("Libraries loaded\n")
    
    # Load data
    df = pd.read_csv('../data/BMW_sales_data.csv')
    print(f"Original dataset shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
    
    # Check for missing values
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum().values,
        'Missing_Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    
    print("\nMissing Values Summary:")
    print(missing_summary[missing_summary['Missing_Count'] > 0])
    
    if missing_summary['Missing_Count'].sum() == 0:
        print("\nGreat! No missing values found in the dataset.")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")
    
    if duplicates > 0:
        print(f"\nRemoving {duplicates} duplicate rows...")
        df = df.drop_duplicates()
        print(f"New shape after removing duplicates: {df.shape}")
    else:
        print("\nNo duplicate rows found.")
    
    # Check for outliers
    def detect_outliers_iqr(data, column):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        return outliers, lower_bound, upper_bound
    
    numeric_cols = ['Price_USD', 'Sales_Volume', 'Mileage_KM', 'Engine_Size_L']
    
    print("\nChecking for unusual values:\n")
    
    for col in numeric_cols:
        outliers, lower, upper = detect_outliers_iqr(df, col)
        outlier_percentage = (len(outliers) / len(df)) * 100
        
        print(f"{col}: Found {len(outliers)} outliers ({outlier_percentage:.1f}%)")
    
    print("\nNote: These outliers are probably real - luxury cars cost more, some have high mileage, etc.")
    
    # Visualize with box plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols):
        axes[idx].boxplot(df[col], vert=True, patch_artist=True,
                          boxprops=dict(facecolor='lightblue', alpha=0.7))
        axes[idx].set_title(f'{col}')
        axes[idx].set_ylabel(col)
        axes[idx].grid(axis='y', alpha=0.3)
    
    plt.suptitle('Box Plots - Spotting Outliers', fontsize=13, y=1.00)
    plt.tight_layout()
    plt.show()
    
    # Create enhanced features
    df_enhanced = df.copy()
    
    print("\nCreating new columns...\n")
    
    # 1. How old is the vehicle?
    df_enhanced['Vehicle_Age'] = 2025 - df_enhanced['Year']
    
    # 2. Group prices into categories
    df_enhanced['Price_Category'] = pd.cut(
        df_enhanced['Price_USD'],
        bins=[0, 50000, 80000, 110000, float('inf')],
        labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
    )
    
    # 3. Mileage categories
    df_enhanced['Mileage_Category'] = pd.cut(
        df_enhanced['Mileage_KM'],
        bins=[0, 50000, 100000, 150000, float('inf')],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # 4. Model categories (by series number)
    df_enhanced['Model_Category'] = df_enhanced['Model'].str.extract('(\d)')[0].astype(int)
    df_enhanced['Model_Category'] = pd.cut(
        df_enhanced['Model_Category'],
        bins=[0, 3, 5, 7, 10],
        labels=['Compact', 'Mid-Size', 'Full-Size', 'Luxury']
    )
    
    # 5. Age groups
    df_enhanced['Age_Group'] = pd.cut(
        df_enhanced['Vehicle_Age'],
        bins=[0, 3, 7, 15],
        labels=['New', 'Recent', 'Older']
    )
    
    # 6. Sales efficiency
    df_enhanced['Sales_per_Price'] = (df_enhanced['Sales_Volume'] / df_enhanced['Price_USD'] * 1000).round(2)
    
    # 7. Electric flag
    df_enhanced['Is_Electric'] = (df_enhanced['Fuel_Type'] == 'Electric').astype(int)
    
    print(f"Created {df_enhanced.shape[1] - df.shape[1]} new features")
    
    # Display sample of enhanced dataset
    print("\nSample of enhanced dataset with new features:")
    print(df_enhanced[['Model', 'Year', 'Price_USD', 'Vehicle_Age', 'Price_Category', 
                       'Mileage_Category', 'Model_Category', 'Age_Group']].head(10))
    
    # Quick check of new features
    print("\nNew features summary:\n")
    new_categorical = ['Price_Category', 'Mileage_Category', 'Model_Category', 'Age_Group']
    
    for col in new_categorical:
        print(f"{col}: {df_enhanced[col].value_counts().to_dict()}")
    
    # Data type verification
    print("\nData types after cleaning:")
    print(df_enhanced.dtypes)
    
    # Final summary
    print("\nCLEANED DATASET SUMMARY\n")
    
    print(f"Original features: {df.shape[1]}")
    print(f"New features added: {df_enhanced.shape[1] - df.shape[1]}")
    print(f"Total features now: {df_enhanced.shape[1]}")
    print(f"Missing values: {df_enhanced.isnull().sum().sum()}")
    
    new_features = [col for col in df_enhanced.columns if col not in df.columns]
    print(f"\nNew features: {', '.join(new_features)}")
    
    print("\nDataset ready for analysis")
    
    # Save the enhanced dataset
    output_path = '../data/BMW_sales_data_cleaned.csv'
    df_enhanced.to_csv(output_path, index=False)
    
    print(f"\nCleaned dataset saved to: {output_path}")
    print(f"  Rows: {len(df_enhanced):,}")
    print(f"  Columns: {len(df_enhanced.columns)}")


if __name__ == "__main__":
    main()
