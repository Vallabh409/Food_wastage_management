-- 1. How many food providers and receivers are there in each city?
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

-- 2. Which type of food provider contributes the most food?
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

-- 3. What is the contact information of food providers in a specific city?
SELECT
  Name,
  Contact
FROM providers
WHERE
  City = 'East Aaron';

-- 4. Which receivers have claimed the most food?
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

-- 5. What is the total quantity of food available from all providers?
SELECT
  SUM(Quantity) AS Total_Food_Quantity
FROM food_listings;

-- 6. Which city has the highest number of food listings?
SELECT
  Location AS City,
  COUNT(Food_ID) AS Number_of_Listings
FROM food_listings
GROUP BY
  City
ORDER BY
  Number_of_Listings DESC
LIMIT 5;

-- 7. What are the most commonly available food types?
SELECT
  Food_Name,
  COUNT(Food_ID) AS Number_of_Listings
FROM food_listings
GROUP BY
  Food_Name
ORDER BY
  Number_of_Listings DESC
LIMIT 10;

-- 8. How many food claims have been made for each food item?
SELECT
  Food_ID,
  COUNT(Claim_ID) AS Number_of_Claims
FROM claims
GROUP BY
  Food_ID
ORDER BY
  Number_of_Claims DESC
LIMIT 10;

-- 9. Which provider has had the highest number of successful food claims?
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

-- 10. What percentage of food claims are completed vs. pending vs. canceled?
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

-- 11. What is the average quantity of food claimed per receiver?
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

-- 12. Which meal type is claimed the most?
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

-- 13. What is the total quantity of food donated by each provider?
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

-- 14. Which food items have expired but not been claimed?
SELECT
  fl.Food_ID,
  fl.Food_Name,
  fl.Expiry_Date,
  fl.Location
FROM food_listings AS fl
LEFT JOIN claims AS c
  ON fl.Food_ID = c.Food_ID
WHERE
  fl.Expiry_Date < '2025-08-21 19:42:16' AND c.Food_ID IS NULL;

-- 15. What are the top 5 cities with the highest number of pending claims?
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

-- 16. How many total claims have been made each month?
SELECT
  STRFTIME('%Y-%m', Timestamp) AS Claim_Month,
  COUNT(Claim_ID) AS Total_Claims
FROM claims
GROUP BY
  Claim_Month
ORDER BY
  Claim_Month;

-- 17. What is the total quantity of food donated by each provider type?
SELECT
  Provider_Type,
  SUM(Quantity) AS Total_Donated_Quantity
FROM food_listings
GROUP BY
  Provider_Type
ORDER BY
  Total_Donated_Quantity DESC;

-- 18. What is the average quantity of food per listing for each `Food_Type`?
SELECT
  Food_Type,
  AVG(Quantity) AS Average_Quantity
FROM food_listings
GROUP BY
  Food_Type;

-- 19. Which food providers have no active or completed claims?
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

-- 20. What is the most claimed `Food_Name` in each city?
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

-- 21. What is the total quantity of food claimed by each `Receiver_Type`?
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

-- 22. Which `Meal_Type` has the highest number of listings?
SELECT
  Meal_Type,
  COUNT(Food_ID) AS Number_of_Listings
FROM food_listings
GROUP BY
  Meal_Type
ORDER BY
  Number_of_Listings DESC;

-- 23. How many providers are in each `Provider_Type`?
SELECT
  Type AS Provider_Type,
  COUNT(Provider_ID) AS Number_of_Providers
FROM providers
GROUP BY
  Type
ORDER BY
  Number_of_Providers DESC;

-- 24. What is the total quantity of food that has expired without being claimed, by provider?
SELECT
  p.Name AS Provider_Name,
  SUM(fl.Quantity) AS Total_Expired_Unclaimed_Quantity
FROM food_listings AS fl
JOIN providers AS p
  ON fl.Provider_ID = p.Provider_ID
LEFT JOIN claims AS c
  ON fl.Food_ID = c.Food_ID
WHERE
  fl.Expiry_Date < '2025-08-21 19:42:58' AND c.Food_ID IS NULL
GROUP BY
  p.Name
ORDER BY
  Total_Expired_Unclaimed_Quantity DESC
LIMIT 10;

-- 25. Which receivers have claimed a specific type of food (e.g., 'Non-Vegetarian')?
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