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


def insert_data(connection, df):

    cursor = connection.cursor()

    # drop table if exists
    cursor.execute("DROP TABLE IF EXISTS flights")
    connection.commit()

    # Creating table with primary key
    create_table_query = """
    CREATE TABLE IF NOT EXISTS flights (
        ID INT AUTO_INCREMENT PRIMARY KEY,  
        FlightNumber VARCHAR(255),
        DepartureDate DATE,
        DepartureTime TIME,
        ArrivalDate DATE,
        ArrivalTime TIME,
        Airline VARCHAR(255),
        DelayMinutes FLOAT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()

    # Insert data
    insert_query = """
    INSERT INTO flights (
        FlightNumber, DepartureDate, DepartureTime, ArrivalDate, ArrivalTime, Airline, DelayMinutes
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each row from the DataFrame
    for _, row in df.iterrows():
        cursor.execute(
            insert_query,
            (
                row["FlightNumber"],
                row["DepartureDate"],
                row["DepartureTime"],
                row["ArrivalDate"],
                row["ArrivalTime"],
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


def connectiom_close(connection):
    connection.close()
    print("Connection closed")
