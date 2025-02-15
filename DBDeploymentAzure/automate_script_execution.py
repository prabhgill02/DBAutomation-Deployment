# import the connector as we have installed mysql-python-connector
import mysql.connector
import os

# # Database connection details for local setup
# DB_CONFIG = {
#     "host": "localhost",  
#     "user": "root",        # Your MySQL username
#     "password": "******",  # Your MySQL password
#     "database": "automateDB"  # Replace with your database name
# }

# Get database credentials from environment variables (GitHub Secrets)
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
# Read SQL script from file
# Pass the script file you want to execute
# SQL_FILE = "schemachanges_script.sql"
SQL_FILE = "add_departments.sql"

try:
    # Establish database connection
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Read SQL file
    with open(SQL_FILE, "r") as file:
        sql_script = file.read()

    # Execute each SQL statement separately
    for statement in sql_script.strip().split(";"):
        if statement.strip():  
            cursor.execute(statement)

    # Commit changes
    conn.commit()
    print("SQL script executed successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    conn.rollback()  # Rollback changes if error occurs

finally:
    # Close connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
