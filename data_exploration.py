from pymongo import MongoClient
import pandas as pd

# Create a client connection to your MongoDB instance
client = MongoClient('mongodb://root:password@localhost:27017')

# Connect to your database
db = client['proc-rec-db']

# Connect to your collection
collection = db['yourCollectionName']

# Convert entire collection to Pandas dataframe
data = pd.DataFrame(list(collection.find()))

# 1. Check for missing values
print("\nMissing values for each column:")
print(data.isnull().sum())

# 2. Identify unique values
print("\nNumber of unique values for each column:")
print(data.nunique())

# 3. Distribution of 'selling_price'
print("\nDistribution of selling_price:")
print(data['selling_price'].describe())

# 4. Top 5 most common products
print("\nTop 5 most common product names:")
print(data['productname'].value_counts().head(5))

# 5. Distribution of 'manufacturer'
print("\nDistribution of manufacturers:")
print(data['manufacturer'].value_counts())

# 6. Relationship between 'selling_price' and 'manufacturer'
print("\nAverage selling_price for each manufacturer:")
print(data.groupby('manufacturer')['selling_price'].mean())

# 7. Number of products per 'customername'
print("\nNumber of products purchased by each customer:")
print(data['customername'].value_counts())

# 8. Distribution of 'appearanceext' and 'boxedext'
print("\nDistribution of appearanceext:")
print(data['appearanceext'].value_counts())
print("\nDistribution of boxedext:")
print(data['boxedext'].value_counts())

# 9. Correlation between numerical variables
print("\nCorrelation between numerical variables:")
print(data.corr())

# 10. Relationship between 'manufacturer' and 'itemgroupname'
print("\nNumber of item groups per manufacturer:")
print(data.groupby('manufacturer')['itemgroupname'].nunique())

