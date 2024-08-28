import pandas as pd
import mysql.connector

def load_data():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your password here
        database="student_list"
    )
    
    # Load data into DataFrame from the correct table name
    query = "SELECT * FROM student_list"  # Update table name here
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df
