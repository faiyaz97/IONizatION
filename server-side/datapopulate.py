import mysql.connector
import csv

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",        # Replace with your host, e.g., 'localhost'
    user="root",             # Replace with your MySQL username
    password="Kunmannay@3",  # Replace with your MySQL password
    database="ionization"    # Replace with your database name
)

cursor = db.cursor()

# Step 1: Create a table in the database
table_creation_query = """
CREATE TABLE IF NOT EXISTS tabledata (
    issuerid VARCHAR(100) PRIMARY KEY,
    iva_industry VARCHAR(100),
    gics_sub_ind VARCHAR(100),
    controv_src_score DECIMAL(10,2),
    environmental_pillar_score DECIMAL(10,2),
    governance_pillar_score DECIMAL(10,2),
    social_pillar_score DECIMAL(10,2),
    climate_change_theme_score DECIMAL(10,2),
    industry_adjusted_score DECIMAL(10,2),
    business_ethics_theme_score DECIMAL(10,2),
    iva_company_rating_scaled DECIMAL(10,2)
)
"""

cursor.execute(table_creation_query)
print("Table created successfully.")

# Step 2: Populate the database from a CSV file
# Specify the path to your CSV file
csv_file_path = r"C:\Users\nayan.verma\Downloads\outputFile.csv"  # Use raw string to avoid escape sequences in Windows paths

# Open the CSV file with a specified encoding
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    # Read the CSV file
    csv_reader = csv.DictReader(file)
    
    # Insert data into the table for each row in the CSV file
    for row in csv_reader:
        # Prepare the data for insertion
        data = (
            row['issuerid'], 
            row['iva_industry'], 
            row['gics_sub_ind'], 
            float(row['controv_src_score']), 
            float(row['environmental_pillar_score']),
            float(row['governance_pillar_score']),
            float(row['social_pillar_score']),
            float(row['climate_change_theme_score']),
            float(row['industry_adjusted_score']),
            float(row['business_ethics_theme_score']),
            float(row['iva_company_rating_scaled'])
        )
        
        # Insert data into the table
        insert_query = """
        INSERT INTO tabledata (
            issuerid, iva_industry, gics_sub_ind, controv_src_score, 
            environmental_pillar_score, governance_pillar_score, 
            social_pillar_score, climate_change_theme_score, 
            industry_adjusted_score, business_ethics_theme_score, 
            iva_company_rating_scaled
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, data)
        
    # Commit the changes
    db.commit()
    print(f"{cursor.rowcount} rows inserted.")

# Close the cursor and database connection
cursor.close()
db.close()
