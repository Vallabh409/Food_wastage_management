import sqlite3
import pandas as pd

# Connect to a new database file named 'food_wastage.db'
conn = sqlite3.connect('food_wastage.db')
cursor = conn.cursor()

# Create the tables based on your project plan
cursor.execute('''
    CREATE TABLE IF NOT EXISTS providers (
        Provider_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receivers (
        Receiver_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_listings (
        Food_ID INTEGER PRIMARY KEY,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date TEXT,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT,
        Meal_Type TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS claims (
        Claim_ID INTEGER PRIMARY KEY,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp TEXT
    )
''')

# Load data from the CSV files into the tables
providers_df = pd.read_csv('providers_data.csv')
receivers_df = pd.read_csv('receivers_data.csv')
food_listings_df = pd.read_csv('food_listings_data.csv')
claims_df = pd.read_csv('claims_data.csv')

providers_df.to_sql('providers', conn, if_exists='replace', index=False)
receivers_df.to_sql('receivers', conn, if_exists='replace', index=False)
food_listings_df.to_sql('food_listings', conn, if_exists='replace', index=False)
claims_df.to_sql('claims', conn, if_exists='replace', index=False)

conn.close()

print("Database and tables created, and data loaded successfully!")