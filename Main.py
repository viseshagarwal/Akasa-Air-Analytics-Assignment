import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
from sql_connection import *
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")


def read_data_csv():
    df = pd.read_csv("aviation_data.csv")
    return df


def convert_to_24hr(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")


def clean_data(df):
    # Check for missing values
    print("Missing values before handling:")
    print(df.isnull().sum())

    # Option 1: Fill NaN with 0 (assuming no delay)
    df["DelayMinutes"] = df["DelayMinutes"].fillna(0)

    print("\nMissing values after handling:")
    print(df.isnull().sum())

    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    print(f"\nNumber of duplicate entries: {duplicate_count}")

    # Remove duplicates
    df = df.drop_duplicates()
    print(f"Number of entries after removing duplicates: {df.shape[0]}")

    # Convert DepartureTime and ArrivalTime to datetime.time
    df["DepartureTime_24"] = df["DepartureTime"].apply(convert_to_24hr)
    df["ArrivalTime_24"] = df["ArrivalTime"].apply(convert_to_24hr)

    # Combine DepartureDate and DepartureTime into a single datetime
    df["DepartureDateTime"] = pd.to_datetime(
        df["DepartureDate"] + " " + df["DepartureTime"], format="%m/%d/%Y %I:%M %p"
    )
    df["ArrivalDateTime"] = pd.to_datetime(
        df["ArrivalDate"] + " " + df["ArrivalTime"], format="%m/%d/%Y %I:%M %p"
    )

    # Identify inconsistent time entries
    inconsistent_times = df[df["ArrivalDateTime"] < df["DepartureDateTime"]]
    print(f"\nNumber of inconsistent time entries: {inconsistent_times.shape[0]}")

    # Option 1: Remove inconsistent entries
    df = df[df["ArrivalDateTime"] >= df["DepartureDateTime"]]

    return df


def normalize_data(df):
    # Convert DepartureDate and ArrivalDate to datetime and format as YYYY-MM-DD
    df["DepartureDate"] = pd.to_datetime(
        df["DepartureDate"], format="%m/%d/%Y"
    ).dt.strftime("%Y-%m-%d")
    df["ArrivalDate"] = pd.to_datetime(
        df["ArrivalDate"], format="%m/%d/%Y"
    ).dt.strftime("%Y-%m-%d")

    # Verify the changes
    df[["DepartureDate", "ArrivalDate"]].head()

    # Optionally, replace the original time columns with 24-hour format
    df["DepartureTime"] = df["DepartureTime_24"]
    df["ArrivalTime"] = df["ArrivalTime_24"]

    # Drop the temporary 24-hour columns
    df = df.drop(["DepartureTime_24", "ArrivalTime_24"], axis=1)

    # Verify the changes
    df[["DepartureTime", "ArrivalTime"]].head()

    # Calculate FlightDuration in minutes
    df["FlightDuration"] = (
        df["ArrivalDateTime"] - df["DepartureDateTime"]
    ).dt.total_seconds() / 60

    # If ArrivalDateTime is on the next day, FlightDuration will still be accurate
    # Verify FlightDuration
    df[
        ["FlightNumber", "DepartureDateTime", "ArrivalDateTime", "FlightDuration"]
    ].head()

    return df


def insert_data(connection, df):
    # Create connection
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_PORT)

    # Insert data into MySQL (df_cleaned is the cleaned dataset)
    insert_data(connection, df)

    # Fetch data back from MySQL
    df_fetched = fetch_data(connection)

    print("\nData fetched from MySQL:")

    return df_fetched


def data_analysis(df):
    # Summary statistics of DelayMinutes
    delay_summary = df["DelayMinutes"].describe()
    print("Delay Minutes Summary:")
    print(delay_summary)

    # Plot distribution of delays
    plt.figure(figsize=(10, 6))
    sns.histplot(df["DelayMinutes"], bins=30, kde=True)
    plt.title("Distribution of Flight Delays")
    plt.xlabel("Delay Minutes")
    plt.ylabel("Frequency")
    plt.show()

    # Average delay per airline
    average_delay_airline = df.groupby("Airline")["DelayMinutes"].mean().reset_index()

    # Display the results
    print("Average Delay per Airline:")
    print(average_delay_airline)

    # Plot average delay per airline
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=average_delay_airline, x="Airline", y="DelayMinutes", palette="viridis"
    )
    plt.title("Average Delay by Airline")
    plt.xlabel("Airline")
    plt.ylabel("Average Delay (Minutes)")
    plt.show()

    # Extract hour from DepartureTime
    df["DepartureHour"] = pd.to_datetime(df["DepartureTime"], format="%H:%M").dt.hour

    # Scatter plot of DepartureHour vs DelayMinutes
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        data=df, x="DepartureHour", y="DelayMinutes", hue="Airline", alpha=0.6
    )
    plt.title("Flight Delays vs Departure Time")
    plt.xlabel("Departure Hour")
    plt.ylabel("Delay Minutes")
    plt.legend(title="Airline")
    plt.show()

    # Alternatively, analyze average delay by departure hour
    average_delay_hour = (
        df.groupby("DepartureHour")["DelayMinutes"].mean().reset_index()
    )

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=average_delay_hour, x="DepartureHour", y="DelayMinutes", marker="o"
    )
    plt.title("Average Delay by Departure Hour")
    plt.xlabel("Departure Hour")
    plt.ylabel("Average Delay (Minutes)")
    plt.xticks(range(0, 24))
    plt.show()

    import scipy.stats as stats

    # Prepare data for ANOVA
    airline_delays = [
        group["DelayMinutes"].values for name, group in df.groupby("Airline")
    ]

    # Perform one-way ANOVA
    anova_result = stats.f_oneway(*airline_delays)

    print("ANOVA Result:")
    print(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}")

    # Interpretation
    if anova_result.pvalue < 0.05:
        print("There is a significant difference in delays between airlines.")
    else:
        print("There is no significant difference in delays between airlines.")


def main():
    # Read data from CSV
    df = read_data_csv()

    # Clean the data
    df_cleaned = clean_data(df)

    # Normalize the data
    df_normalized = normalize_data(df_cleaned)

    # # Insert data into MySQL and fetch back
    # df_fetched = insert_data(df_normalized)

    # Perform data analysis
    data_analysis(df_normalized)


if __name__ == "__main__":
    main()
