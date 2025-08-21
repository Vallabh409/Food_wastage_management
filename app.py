import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Function to connect to the database and run a query
def run_query(query, params=None):
    with sqlite3.connect('food_wastage.db') as conn:
        if params:
            conn.execute(query, params)
        else:
            return pd.read_sql_query(query, conn)

st.set_page_config(layout="wide")
st.title("Local Food Wastage Management System")
st.sidebar.header("Filter & Manage Data")

# --- Data Filtering Section ---
st.header("Available Food Listings")
st.sidebar.subheader("Filter Food Listings")

# Get unique cities for a dropdown filter
cities_query = "SELECT DISTINCT Location FROM food_listings ORDER BY Location"
cities_df = run_query(cities_query)
selected_city = st.sidebar.selectbox("Select City", ["All"] + cities_df['Location'].tolist())

# Dynamically build the query based on the filter
query = "SELECT * FROM food_listings"
if selected_city != "All":
    query += f" WHERE Location = '{selected_city}'"

food_listings_df = run_query(query)
st.dataframe(food_listings_df)

# --- CRUD Operations Section ---
st.sidebar.header("Manage Food Listings")

# --- CREATE (Add New Listing) ---
with st.sidebar.form("add_listing_form"):
    st.subheader("Add New Food Listing")
    add_food_name = st.text_input("Food Name", key="add_food_name")
    add_quantity = st.number_input("Quantity", min_value=1, key="add_quantity")
    add_provider_id = st.number_input("Provider ID", min_value=1, key="add_provider_id")
    add_provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket", "Catering Service"], key="add_provider_type")
    add_location = st.text_input("Location", key="add_location")
    add_food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"], key="add_food_type")
    add_meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"], key="add_meal_type")
    
    submitted = st.form_submit_button("Add Listing")
    if submitted:
        insert_query = """
            INSERT INTO food_listings (Food_Name, Quantity, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        run_query(insert_query, (add_food_name, add_quantity, add_provider_id, add_provider_type, add_location, add_food_type, add_meal_type))
        st.success(f"Added {add_food_name} successfully!")

# --- UPDATE (Update a Listing) ---
st.sidebar.markdown("---")
with st.sidebar.form("update_listing_form"):
    st.subheader("Update Existing Listing")
    food_id_list = run_query("SELECT Food_ID FROM food_listings")['Food_ID'].tolist()
    if food_id_list:
        update_food_id = st.selectbox("Select Food ID to Update", food_id_list, key="update_food_id")
        update_quantity = st.number_input("New Quantity", min_value=1, key="update_quantity")
        update_submitted = st.form_submit_button("Update Listing")
        
        if update_submitted:
            update_query = """
                UPDATE food_listings SET Quantity = ? WHERE Food_ID = ?
            """
            run_query(update_query, (update_quantity, update_food_id))
            st.success(f"Listing with Food ID {update_food_id} updated successfully!")
    else:
        st.info("No listings available to update.")

# --- DELETE (Delete a Listing) ---
st.sidebar.markdown("---")
with st.sidebar.form("delete_listing_form"):
    st.subheader("Delete Listing")
    food_id_list_del = run_query("SELECT Food_ID FROM food_listings")['Food_ID'].tolist()
    if food_id_list_del:
        delete_food_id = st.selectbox("Select Food ID to Delete", food_id_list_del, key="delete_food_id")
        delete_submitted = st.form_submit_button("Delete Listing")
        
        if delete_submitted:
            delete_query = "DELETE FROM food_listings WHERE Food_ID = ?"
            run_query(delete_query, (delete_food_id,))
            st.success(f"Listing with Food ID {delete_food_id} deleted successfully!")
    else:
        st.info("No listings available to delete.")


# --- SQL Query Analysis Section ---
st.header("SQL-Powered Analysis & Insights")

# 1. How many food providers and receivers are there in each city?
st.subheader("1. Providers and Receivers by City")
query_1 = """
SELECT
  p.City,
  COUNT(DISTINCT p.Provider_ID) AS Number_of_Providers,
  COUNT(DISTINCT r.Receiver_ID) AS Number_of_Receivers
FROM providers AS p
LEFT JOIN receivers AS r
  ON p.City = r.City
GROUP BY
  p.City
ORDER BY
  p.City;
"""
st.dataframe(run_query(query_1))

# 2. Which type of food provider contributes the most food?
st.subheader("2. Top Food Provider Types by Contribution")
query_2 = """
SELECT
  p.Type AS Provider_Type,
  COUNT(f.Food_ID) AS Number_of_Listings
FROM providers AS p
JOIN food_listings AS f
  ON p.Provider_ID = f.Provider_ID
GROUP BY
  p.Type
ORDER BY
  Number_of_Listings DESC;
"""
st.dataframe(run_query(query_2))

# 3. What is the contact information of food providers in a specific city?
st.subheader("3. Contact Information of Providers in 'East Aaron'")
query_3 = """
SELECT
  Name,
  Contact
FROM providers
WHERE
  City = 'East Aaron';
"""
st.dataframe(run_query(query_3))

# 4. Which receivers have claimed the most food?
st.subheader("4. Top 10 Receivers by Number of Claims")
query_4 = """
SELECT
  r.Name AS Receiver_Name,
  COUNT(c.Claim_ID) AS Total_Claims
FROM receivers AS r
JOIN claims AS c
  ON r.Receiver_ID = c.Receiver_ID
GROUP BY
  r.Name
ORDER BY
  Total_Claims DESC
LIMIT 10;
"""
st.dataframe(run_query(query_4))

# 5. What is the total quantity of food available from all providers?
st.subheader("5. Total Quantity of All Available Food")
query_5 = """
SELECT
  SUM(Quantity) AS Total_Food_Quantity
FROM food_listings;
"""
st.dataframe(run_query(query_5))

# 6. Which city has the highest number of food listings?
st.subheader("6. Top 5 Cities with the Most Food Listings")
query_6 = """
SELECT
  Location AS City,
  COUNT(Food_ID) AS Number_of_Listings
FROM food_listings
GROUP BY
  City
ORDER BY
  Number_of_Listings DESC
LIMIT 5;
"""
st.dataframe(run_query(query_6))

# 7. What are the most commonly available food types?
st.subheader("7. Top 10 Most Common Food Types")
query_7 = """
SELECT
  Food_Name,
  COUNT(Food_ID) AS Number_of_Listings
FROM food_listings
GROUP BY
  Food_Name
ORDER BY
  Number_of_Listings DESC
LIMIT 10;
"""
st.dataframe(run_query(query_7))

# 8. How many food claims have been made for each food item?
st.subheader("8. Top 10 Food Items by Claims")
query_8 = """
SELECT
  Food_ID,
  COUNT(Claim_ID) AS Number_of_Claims
FROM claims
GROUP BY
  Food_ID
ORDER BY
  Number_of_Claims DESC
LIMIT 10;
"""
st.dataframe(run_query(query_8))

# 9. Which provider has had the highest number of successful food claims?
st.subheader("9. Top 10 Providers by Successful Claims")
query_9 = """
SELECT
  p.Name AS Provider_Name,
  COUNT(c.Claim_ID) AS Successful_Claims
FROM claims AS c
JOIN food_listings AS fl
  ON c.Food_ID = fl.Food_ID
JOIN providers AS p
  ON fl.Provider_ID = p.Provider_ID
WHERE
  c.Status = 'Completed'
GROUP BY
  p.Name
ORDER BY
  Successful_Claims DESC
LIMIT 10;
"""
st.dataframe(run_query(query_9))

# 10. What percentage of food claims are completed vs. pending vs. canceled?
st.subheader("10. Percentage of Claims by Status")
query_10 = """
SELECT
  Status,
  COUNT(Claim_ID) AS Total_Claims,
  CAST(COUNT(Claim_ID) AS REAL) * 100 / (
    SELECT
      COUNT(Claim_ID)
    FROM claims
  ) AS Percentage
FROM claims
GROUP BY
  Status;
"""
st.dataframe(run_query(query_10))

# 11. What is the average quantity of food claimed per receiver?
st.subheader("11. Average Food Quantity Claimed per Receiver")
query_11 = """
SELECT
  AVG(Total_Quantity) AS Average_Quantity_per_Receiver
FROM (
  SELECT
    c.Receiver_ID,
    SUM(fl.Quantity) AS Total_Quantity
  FROM claims AS c
  JOIN food_listings AS fl
    ON c.Food_ID = fl.Food_ID
  GROUP BY
    c.Receiver_ID
);
"""
st.dataframe(run_query(query_11))

# 12. Which meal type is claimed the most?
st.subheader("12. Most Claimed Meal Type")
query_12 = """
SELECT
  fl.Meal_Type,
  COUNT(c.Claim_ID) AS Number_of_Claims
FROM claims AS c
JOIN food_listings AS fl
  ON c.Food_ID = fl.Food_ID
GROUP BY
  fl.Meal_Type
ORDER BY
  Number_of_Claims DESC;
"""
st.dataframe(run_query(query_12))

# 13. What is the total quantity of food donated by each provider?
st.subheader("13. Top 10 Providers by Total Donated Quantity")
query_13 = """
SELECT
  p.Name AS Provider_Name,
  SUM(fl.Quantity) AS Total_Donated_Quantity
FROM providers AS p
JOIN food_listings AS fl
  ON p.Provider_ID = fl.Provider_ID
GROUP BY
  p.Name
ORDER BY
  Total_Donated_Quantity DESC
LIMIT 10;
"""
st.dataframe(run_query(query_13))

# 14. Which food items have expired but not been claimed?
st.subheader("14. Unclaimed Expired Food Items")
query_14 = f"""
SELECT
  fl.Food_ID,
  fl.Food_Name,
  fl.Expiry_Date,
  fl.Location
FROM food_listings AS fl
LEFT JOIN claims AS c
  ON fl.Food_ID = c.Food_ID
WHERE
  fl.Expiry_Date < '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' AND c.Food_ID IS NULL;
"""
st.dataframe(run_query(query_14))

# 15. What are the top 5 cities with the highest number of pending claims?
st.subheader("15. Top 5 Cities with Pending Claims")
query_15 = """
SELECT
  fl.Location AS City,
  COUNT(c.Claim_ID) AS Pending_Claims_Count
FROM claims AS c
JOIN food_listings AS fl
  ON c.Food_ID = fl.Food_ID
WHERE
  c.Status = 'Pending'
GROUP BY
  fl.Location
ORDER BY
  Pending_Claims_Count DESC
LIMIT 5;
"""
st.dataframe(run_query(query_15))

# --- Additional Queries ---

# 16. How many total claims have been made each month?
st.subheader("16. Monthly Claim Trends")
query_16 = """
SELECT
  STRFTIME('%Y-%m', Timestamp) AS Claim_Month,
  COUNT(Claim_ID) AS Total_Claims
FROM claims
GROUP BY
  Claim_Month
ORDER BY
  Claim_Month;
"""
st.dataframe(run_query(query_16))

# 17. What is the total quantity of food donated by each provider type?
st.subheader("17. Total Quantity Donated by Provider Type")
query_17 = """
SELECT
  Provider_Type,
  SUM(Quantity) AS Total_Donated_Quantity
FROM food_listings
GROUP BY
  Provider_Type
ORDER BY
  Total_Donated_Quantity DESC;
"""
st.dataframe(run_query(query_17))

# 18. What is the average quantity of food per listing for each Food_Type?
st.subheader("18. Average Quantity per Food Type Listing")
query_18 = """
SELECT
  Food_Type,
  AVG(Quantity) AS Average_Quantity
FROM food_listings
GROUP BY
  Food_Type;
"""
st.dataframe(run_query(query_18))

# 19. Which food providers have no active or completed claims?
st.subheader("19. Providers with No Claims")
query_19 = """
SELECT
  p.Name,
  p.City
FROM providers AS p
LEFT JOIN food_listings AS fl
  ON p.Provider_ID = fl.Provider_ID
LEFT JOIN claims AS c
  ON fl.Food_ID = c.Food_ID
WHERE
  c.Claim_ID IS NULL
GROUP BY
  p.Name,
  p.City
ORDER BY
  p.Name;
"""
st.dataframe(run_query(query_19))

# 20. What is the most claimed Food_Name in each city?
st.subheader("20. Most Claimed Food Item by City")
query_20 = """
WITH RankedClaims AS (
  SELECT
    fl.Location,
    fl.Food_Name,
    COUNT(c.Claim_ID) AS Total_Claims,
    ROW_NUMBER() OVER (PARTITION BY fl.Location ORDER BY COUNT(c.Claim_ID) DESC) AS rn
  FROM claims AS c
  JOIN food_listings AS fl
    ON c.Food_ID = fl.Food_ID
  GROUP BY
    fl.Location,
    fl.Food_Name
)
SELECT
  Location,
  Food_Name,
  Total_Claims
FROM RankedClaims
WHERE
  rn = 1;
"""
st.dataframe(run_query(query_20))

# 21. What is the total quantity of food claimed by each Receiver_Type?
st.subheader("21. Total Quantity Claimed by Receiver Type")
query_21 = """
SELECT
  r.Type AS Receiver_Type,
  SUM(fl.Quantity) AS Total_Claimed_Quantity
FROM claims AS c
JOIN food_listings AS fl
  ON c.Food_ID = fl.Food_ID
JOIN receivers AS r
  ON c.Receiver_ID = r.Receiver_ID
GROUP BY
  r.Type
ORDER BY
  Total_Claimed_Quantity DESC;
"""
st.dataframe(run_query(query_21))

# 22. Which Meal_Type has the highest number of listings?
st.subheader("22. Most Listed Meal Type")
query_22 = """
SELECT
  Meal_Type,
  COUNT(Food_ID) AS Number_of_Listings
FROM food_listings
GROUP BY
  Meal_Type
ORDER BY
  Number_of_Listings DESC;
"""
st.dataframe(run_query(query_22))

# 23. How many providers are in each Provider_Type?
st.subheader("23. Provider Count by Provider Type")
query_23 = """
SELECT
  Type AS Provider_Type,
  COUNT(Provider_ID) AS Number_of_Providers
FROM providers
GROUP BY
  Type
ORDER BY
  Number_of_Providers DESC;
"""
st.dataframe(run_query(query_23))

# 24. What is the total quantity of food that has expired without being claimed, by provider?
st.subheader("24. Top 10 Providers with Expired Unclaimed Food")
query_24 = f"""
SELECT
  p.Name AS Provider_Name,
  SUM(fl.Quantity) AS Total_Expired_Unclaimed_Quantity
FROM food_listings AS fl
JOIN providers AS p
  ON fl.Provider_ID = p.Provider_ID
LEFT JOIN claims AS c
  ON fl.Food_ID = c.Food_ID
WHERE
  fl.Expiry_Date < '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' AND c.Food_ID IS NULL
GROUP BY
  p.Name
ORDER BY
  Total_Expired_Unclaimed_Quantity DESC
LIMIT 10;
"""
st.dataframe(run_query(query_24))

# 25. Which receivers have claimed a specific type of food (e.g., 'Non-Vegetarian')?
st.subheader("25. Receivers Who Claimed 'Non-Vegetarian' Food")
query_25 = """
SELECT
  DISTINCT r.Name AS Receiver_Name,
  r.Contact
FROM receivers AS r
JOIN claims AS c
  ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings AS fl
  ON c.Food_ID = fl.Food_ID
WHERE
  fl.Food_Type = 'Non-Vegetarian';
"""
st.dataframe(run_query(query_25))