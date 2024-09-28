from sqlalchemy import create_engine, text
import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import scipy.stats as stats
import warnings

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


messages = []


# Missing Values
def check_missing_values(df, messages):
    messages.append("<h2>Handling Missing Values...</h2>")

    # Missing values before handling
    missing_before = df.isnull().sum()
    messages.append("<h3>Missing Values Before Handling:</h3>")
    messages.append(missing_before.to_frame().to_html())

    # Handle missing values for 'DelayMinutes'
    df["DelayMinutes"] = df["DelayMinutes"].fillna(0)

    # Missing values after handling
    missing_after = df.isnull().sum()
    messages.append("<h3>Missing Values After Handling:</h3>")
    messages.append(missing_after.to_frame().to_html())

    return df


# Check for duplicates
def check_duplicates(df, messages):
    messages.append("<h2>Checking for Duplicates...</h2>")

    # Count duplicate entries
    duplicate_count = df.duplicated(
        subset=[
            "FlightNumber",
            "DepartureDate",
            "DepartureTime",
            "ArrivalDate",
            "ArrivalTime",
            "Airline",
            "DelayMinutes",
        ]
    ).sum()
    messages.append(
        f"<p><strong>Number of duplicate entries:</strong> {duplicate_count}</p>"
    )

    # Remove duplicates
    df = df.drop_duplicates(
        subset=[
            "FlightNumber",
            "DepartureDate",
            "DepartureTime",
            "ArrivalDate",
            "ArrivalTime",
            "Airline",
            "DelayMinutes",
        ]
    )

    messages.append(
        f"<p><strong>Number of entries after removing duplicates:</strong> {df.shape[0]}</p>"
    )
    return df


# Convert 12-hour time format to 24-hour
def convert_to_24hr(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")


# Check for inconsistent time entries
def check_inconsistent_time_entries(df, messages):
    messages.append("<h2>Checking for Inconsistent Time Entries...</h2>")

    # Inconsistent time entries
    inconsistent_time_entries = df[df["DepartureTime"] > df["ArrivalTime"]]
    messages.append(
        f"<p><strong>Number of inconsistent time entries:</strong> {inconsistent_time_entries.shape[0]}</p>"
    )

    # Remove inconsistent time entries
    df = df[df["DepartureTime"] <= df["ArrivalTime"]]
    messages.append(
        f"<p><strong>Number of entries after removing inconsistent time entries:</strong> {df.shape[0]}</p>"
    )

    # Convert DepartureTime and ArrivalTime to 24-hour format
    df["DepartureTime_24"] = df["DepartureTime"].apply(convert_to_24hr)
    df["ArrivalTime_24"] = df["ArrivalTime"].apply(convert_to_24hr)

    # Combine DepartureDate and DepartureTime into a single datetime
    df["DepartureDateTime"] = pd.to_datetime(
        df["DepartureDate"] + " " + df["DepartureTime"], format="%m/%d/%Y %I:%M %p"
    )
    df["ArrivalDateTime"] = pd.to_datetime(
        df["ArrivalDate"] + " " + df["ArrivalTime"], format="%m/%d/%Y %I:%M %p"
    )

    return df


# Normalize Data
def normalize_data(df, messages):
    messages.append("<h2>Normalizing Data...</h2>")

    # Convert DepartureDate and ArrivalDate to datetime and format as YYYY-MM-DD
    df["DepartureDate"] = pd.to_datetime(
        df["DepartureDate"], format="%m/%d/%Y"
    ).dt.strftime("%Y-%m-%d")
    df["ArrivalDate"] = pd.to_datetime(
        df["ArrivalDate"], format="%m/%d/%Y"
    ).dt.strftime("%Y-%m-%d")

    messages.append(
        "<p>Converted DepartureDate and ArrivalDate to YYYY-MM-DD format.</p>"
    )

    # Replace the original time columns with 24-hour format
    df["DepartureTime"] = df["DepartureTime_24"]
    df["ArrivalTime"] = df["ArrivalTime_24"]

    # Drop the temporary 24-hour columns
    df = df.drop(["DepartureTime_24", "ArrivalTime_24"], axis=1)
    messages.append(
        "<p>Replaced original time columns with 24-hour format and removed temporary columns.</p>"
    )

    # Calculate FlightDuration in minutes
    df["FlightDuration"] = (
        df["ArrivalDateTime"] - df["DepartureDateTime"]
    ).dt.total_seconds() / 60
    messages.append("<p>Calculated FlightDuration in minutes.</p>")

    return df


def insert_data(df, messages):
    messages.append("<h2>Inserting Data into MySQL...</h2>")

    # Create connection
    connection_string = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    try:
        engine = create_engine(connection_string)
        # create table
        create_table_query = text(
            """
        CREATE TABLE IF NOT EXISTS aviation_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            FlightNumber TEXT,
            DepartureDate TEXT,
            DepartureTime TEXT,
            ArrivalDate TEXT,
            ArrivalTime TEXT,
            Airline TEXT,
            DelayMinutes FLOAT
        )"""
        )

        with engine.connect() as connection:
            connection.execute(create_table_query)

        # insert data
        df.to_sql("aviation_data", engine, if_exists="append", index=False)
        messages.append("<p>Data inserted into MySQL successfully.</p>")

        # fetch data
        df_fetched = pd.read_sql("SELECT * FROM aviation_data", engine)
        messages.append("<p>Data fetched from MySQL successfully.</p>")
        print(df_fetched.head())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        engine.dispose()

    return df_fetched


def generate_report(messages):
    # Start HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aviation Data Report</title>
        <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            line-height: 1.6;
        }
        h1, h2, h3 { 
            color: #2E4053; 
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px;
        }
        h2 {
            margin-top: 30px;
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-bottom: 20px; 
            font-size: 14px;
        }
        table, th, td { 
            border: 1px solid #ddd; 
        }
        th, td { 
            padding: 10px; 
            text-align: left; 
        }
        th { 
            background-color: #f2f2f2; 
        }
        tr:nth-child(even) { 
            background-color: #f9f9f9; 
        }
        tr:hover { 
            background-color: #f1f1f1; 
        }
        a { 
            text-decoration: none; 
            color: #2980B9; 
        }
        a:hover { 
            text-decoration: underline; 
            color: #1A5276;
        }
        img { 
            max-width: 100%; 
            height: auto; 
            display: block;
            margin-top: 10px;
            margin-bottom: 20px;
        }
    </style>
    </head>
    <body>
        <h1>Aviation Data Report</h1>
    """

    # Add all messages
    for message in messages:
        html_content += message

    # Close HTML content
    html_content += """
    </body>
    </html>
    """

    # Write to HTML file
    if not os.path.exists("reports"):
        os.makedirs("reports")

    with open("reports/aviation_report.html", "w") as report_file:
        report_file.write(html_content)

    print("HTML report generated and saved as 'reports/aviation_report.html'.")


def data_analysis(df, messages):
    messages.append("<h2>Performing Data Analysis...</h2>")

    # Summary statistics of DelayMinutes
    delay_summary = df["DelayMinutes"].describe()
    messages.append("<h3>Delay Minutes Summary:</h3>")
    messages.append(delay_summary.to_frame().to_html())

    # Plot distribution of delays
    plt.figure(figsize=(8, 5))
    sns.histplot(df["DelayMinutes"], bins=10, kde=True)
    plt.title("Distribution of Flight Delays")
    plt.xlabel("Delay Minutes")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig("reports/delay_distribution.png")
    plt.close()
    messages.append(
        "<p>Saved plot: <a href='delay_distribution.png' target='_blank'>Distribution of Flight Delays</a></p><br/> <img src='delay_distribution.png'>"
    )

    # Average delay per airline
    average_delay_airline = df.groupby("Airline")["DelayMinutes"].mean().reset_index()
    messages.append("<h3>Average Delay per Airline:</h3>")
    messages.append(average_delay_airline.to_html(index=False))

    # Plot average delay per airline
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=average_delay_airline,
        x="Airline",
        y="DelayMinutes",
        palette="viridis",
        hue="Airline",
    )
    plt.title("Average Delay by Airline")
    plt.xlabel("Airline")
    plt.ylabel("Average Delay (Minutes)")
    plt.tight_layout()
    plt.savefig("reports/average_delay_airline.png")
    plt.close()
    messages.append(
        "<p>Saved plot: <a href='average_delay_airline.png' target='_blank'>Average Delay by Airline</a></p><br/><img src='average_delay_airline.png'>"
    )

    # Extract hour from DepartureTime
    df["DepartureHour"] = pd.to_datetime(df["DepartureTime"], format="%H:%M").dt.hour

    # Scatter plot of DepartureHour vs DelayMinutes
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df, x="DepartureHour", y="DelayMinutes", hue="Airline", alpha=0.6
    )
    plt.title("Flight Delays vs Departure Time")
    plt.xlabel("Departure Hour")
    plt.ylabel("Delay Minutes")
    plt.legend(title="Airline", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("reports/departure_vs_delay.png")
    plt.close()
    messages.append(
        "<p>Saved plot: <a href='departure_vs_delay.png' target='_blank'>Flight Delays vs Departure Time</a></p> <br/><img src='departure_vs_delay.png'>"
    )

    # Analyze average delay by departure hour
    average_delay_hour = (
        df.groupby("DepartureHour")["DelayMinutes"].mean().reset_index()
    )

    plt.figure(figsize=(8, 5))
    sns.lineplot(
        data=average_delay_hour, x="DepartureHour", y="DelayMinutes", marker="o"
    )
    plt.title("Average Delay by Departure Hour")
    plt.xlabel("Departure Hour")
    plt.ylabel("Average Delay (Minutes)")
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.savefig("reports/average_delay_hour.png")
    plt.close()
    messages.append(
        "<p>Saved plot: <a href='average_delay_hour.png' target='_blank'>Average Delay by Departure Hour</a></p> <br/><img src='average_delay_hour.png'>"
    )

    # Perform one-way ANOVA
    airline_delays = [
        group["DelayMinutes"].values for name, group in df.groupby("Airline")
    ]

    anova_result = stats.f_oneway(*airline_delays)

    messages.append("<h3>ANOVA Result:</h3>")
    messages.append(
        f"<p>F-statistic: {anova_result.statistic:.4f}, p-value: {anova_result.pvalue:.4f}</p>"
    )

    # Interpretation
    if anova_result.pvalue < 0.05:
        interpretation = "<p>There is a <strong>significant difference</strong> in delays between airlines.</p>"
    else:
        interpretation = "<p>There is <strong>no significant difference</strong> in delays between airlines.</p>"
    messages.append("<h3>Interpretation:</h3>")
    messages.append(interpretation)

    return delay_summary, average_delay_airline


def main():
    messages = []

    # create a new folder called reports if not exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Read data from CSV
    messages.append("<h2>Reading Data...</h2>")
    df = read_data_csv()
    messages.append(
        f"<p>Loaded dataset with {df.shape[0]} records and {df.shape[1]} columns.</p>"
    )
    messages.append("<h3>Sample Data:</h3>")
    messages.append(df.head().to_html())

    # Insert data into MySQL and fetch back
    df = insert_data(df, messages)

    # Handle missing values
    df = check_missing_values(df, messages)

    # Check for duplicates
    df = check_duplicates(df, messages)

    # Check for inconsistent time entries
    df = check_inconsistent_time_entries(df, messages)

    # Normalize the data
    df_normalized = normalize_data(df, messages)
    df_normalized.to_csv("normalized_data.csv", index=False)
    messages.append(
        "<p>Normalized data saved as <a href='reports/normalized_data.csv' target='_blank'>normalized_data.csv</a>.</p>"
    )

    #

    # Perform data analysis
    delay_summary, average_delay_airline = data_analysis(df_normalized, messages)

    # Save cleaned data to CSV
    df.to_csv("aviation_data_cleaned.csv", index=False)

    # Generate report
    generate_report(messages)


if __name__ == "__main__":
    main()
