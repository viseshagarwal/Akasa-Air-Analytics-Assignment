import mysql.connector
from mysql.connector import Error
import pandas as pd


# MySQL connection setup
def create_connection(host_name, user_name, user_password, db_name, db_port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=db_port,
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# Insert data into MySQL
def insert_data(connection, df):
    cursor = connection.cursor()

    # Creating table with primary key
    create_table_query = """
    CREATE TABLE IF NOT EXISTS flights (
        ID INT AUTO_INCREMENT PRIMARY KEY,  -- Auto-incrementing ID as primary key
        FlightNumber VARCHAR(255),
        DepartureDateTime DATETIME,
        ArrivalDateTime DATETIME,
        FlightDuration TIME,
        Airline VARCHAR(255),
        DelayMinutes FLOAT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()

    # Insert data
    insert_query = """
    INSERT INTO flights (
        FlightNumber, DepartureDateTime, ArrivalDateTime, FlightDuration, Airline, DelayMinutes
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    # Insert each row from the DataFrame
    for _, row in df.iterrows():
        # Convert Timedelta to HH:MM:SS
        total_seconds = int(row["FlightDuration"].total_seconds())
        flight_duration_str = f"{total_seconds // 3600:02}:{(total_seconds // 60) % 60:02}:{total_seconds % 60:02}"  # Format as HH:MM:SS

        cursor.execute(
            insert_query,
            (
                row["FlightNumber"],
                row["DepartureDateTime"],
                row["ArrivalDateTime"],
                flight_duration_str,  # Use the formatted duration
                row["Airline"],
                row["DelayMinutes"],
            ),
        )
    connection.commit()
    print("Data inserted successfully")


# Fetch data from MySQL
def fetch_data(connection):
    cursor = connection.cursor()
    fetch_query = "SELECT * FROM flights"
    cursor.execute(fetch_query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Convert to DataFrame
    df_fetched = pd.DataFrame(result, columns=columns)
    return df_fetched
