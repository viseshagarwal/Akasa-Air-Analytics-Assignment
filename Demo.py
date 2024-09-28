Demo.py
# # Interview Task – Data Engineering & Analytics
#

# %%
# imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import scipy.stats as stats
import warnings

warnings.filterwarnings("ignore")

# %% [markdown]
# ### Import the datasets
#

# %%
df = pd.read_csv("aviation_data.csv")
print(df.head())

# %% [markdown]
# ### Insert the datasets and fetch values from MySQL database
#

# %%
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve database credentials from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")


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

    # fetch data
    df_fetched = pd.read_sql("SELECT * FROM aviation_data", engine)

    print(df_fetched.head())

except Exception as e:
    print(f"Error: {e}")

finally:
    engine.dispose()

# %% [markdown]
# ## DATA CLEANING
#
# - a. Identify and handle any missing or inconsistent values in the dataset.
#

# %% [markdown]
# ##### Data Cleaning : Missing Values
#

# %%
df = df_fetched


# Missing Values
def check_missing_values(df):
    print("Missing values before handling:")
    print(df.isnull().sum())

    df["DelayMinutes"] = df["DelayMinutes"].fillna(0)

    print("\nMissing values after handling:")
    print(df.isnull().sum())
    return df


df = check_missing_values(df)

# %% [markdown]
# ##### Data Cleaning: Duplicate Values
#


# %%
# Check for duplicates
def check_duplicates(df):
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
    print(f"\nNumber of duplicate entries: {duplicate_count}")

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

    print(f"Number of entries after removing duplicates: {df.shape[0]}")
    return df


df = check_duplicates(df)

# %% [markdown]
# ##### Data Cleaning: Inconsistent Time Entries
#


# %%
def convert_to_24hr(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")


# Check for inconsistent time entries
def check_inconsistent_time_entries(df):
    inconsistent_time_entries = df[df["DepartureTime"] > df["ArrivalTime"]]
    print(f"Number of inconsistent time entries: {inconsistent_time_entries.shape[0]}")

    # Remove inconsistent time entries
    df = df[df["DepartureTime"] <= df["ArrivalTime"]]
    print(f"Number of entries after removing inconsistent time entries: {df.shape[0]}")

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
    print(df.head())
    return df


df = check_inconsistent_time_entries(df)
df.to_csv("aviation_data_cleaned.csv", index=False)

# %% [markdown]
# - b. Ensure all column data types are appropriate (e.g., dates as date types, times as time types).
#

# %%
# Ensure all column data types are appropriate (e.g., dates as date types, times as time types).
df["FlightNumber"] = df["FlightNumber"].astype(str)
df["DepartureDate"] = pd.to_datetime(df["DepartureDate"])
df["ArrivalDate"] = pd.to_datetime(df["ArrivalDate"])
df["DepartureTime"] = pd.to_datetime(df["DepartureTime"])
df["ArrivalTime"] = pd.to_datetime(df["ArrivalTime"])
df["DelayMinutes"] = df["DelayMinutes"].astype(int)
df["Airline"] = df["Airline"].astype(str)
print(df.dtypes)
print(df.head(5))

# %% [markdown]
# - Correct any inconsistencies or errors in times (e.g., arrival time should be later than departure
#   time).
#

# %%
# Correct any inconsistencies or errors in times (e.g., arrival time should be later than departure time).
df = df[df["DepartureDateTime"] <= df["ArrivalDateTime"]]
print(df.head())

# %% [markdown]
# ### Data Normalization
#
# - a. Convert DepartureDate and ArrivalDate columns to a standard YYYY-MM-DD format.
#

# %%
# Convert DepartureDate and ArrivalDate to datetime and format as YYYY-MM-DD
df["DepartureDate"] = pd.to_datetime(
    df["DepartureDate"], format="%m/%d/%Y"
).dt.strftime("%Y-%m-%d")
df["ArrivalDate"] = pd.to_datetime(df["ArrivalDate"], format="%m/%d/%Y").dt.strftime(
    "%Y-%m-%d"
)

# Verify the changes
df[["DepartureDate", "ArrivalDate"]].head()

# %% [markdown]
# - b. Convert DepartureTime and ArrivalTime columns to a 24-hour time format (e.g., "08:30" for 8:30 AM).
#

# %%
# Optionally, replace the original time columns with 24-hour format
df["DepartureTime"] = df["DepartureTime_24"]
df["ArrivalTime"] = df["ArrivalTime_24"]

# Drop the temporary 24-hour columns
df = df.drop(["DepartureTime_24", "ArrivalTime_24"], axis=1)

# Verify the changes
df[["DepartureTime", "ArrivalTime"]].head()

# %% [markdown]
# - c. Create a new column for FlightDuration by calculating the difference between DepartureTime and ArrivalTime on the same day.
#

# %%
# Calculate FlightDuration in minutes
df["FlightDuration"] = (
    df["ArrivalDateTime"] - df["DepartureDateTime"]
).dt.total_seconds() / 60

# If ArrivalDateTime is on the next day, FlightDuration will still be accurate

df[["FlightNumber", "DepartureDateTime", "ArrivalDateTime", "FlightDuration"]].head()

# %% [markdown]
# ## DATA ANALYSIS
#
# - Analyze the distribution of delays and identify any trends or patterns.
#

# %%
# Summary statistics of DelayMinutes
delay_summary = df["DelayMinutes"].describe()
print("Delay Minutes Summary:")
print(delay_summary)

# Plot distribution of delays
plt.figure(figsize=(8, 5))
sns.histplot(df["DelayMinutes"], bins=10, kde=True)
plt.title("Distribution of Flight Delays")
plt.xlabel("Delay Minutes")
plt.ylabel("Frequency")
plt.show()

# %% [markdown]
# - Calculate the average delay for each airline.
#

# %%
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

# %% [markdown]
# - Identify any relationships between flight delays and departure times (e.g., are flights departing later in the day more likely to be delayed?).
#

# %%
# Extract hour from DepartureTime
df["DepartureHour"] = pd.to_datetime(df["DepartureTime"], format="%H:%M").dt.hour

# Scatter plot of DepartureHour vs DelayMinutes
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="DepartureHour", y="DelayMinutes", hue="Airline", alpha=0.6)
plt.title("Flight Delays vs Departure Time")
plt.xlabel("Departure Hour (Time)")
plt.ylabel("Delay Minutes")
plt.legend(title="Airline")
plt.show()

# Alternatively, analyze average delay by departure hour
average_delay_hour = df.groupby("DepartureHour")["DelayMinutes"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.lineplot(data=average_delay_hour, x="DepartureHour", y="DelayMinutes", marker="o")
plt.title("Average Delay by Departure Hour")
plt.xlabel("Departure Hour(Time)")
plt.ylabel("Average Delay (Minutes)")
plt.xticks(range(0, 24))
plt.show()

# %% [markdown]
# - Determine if there is a significant difference in delays between different airlines.
#

# %%
# Prepare data for ANOVA
airline_delays = [group["DelayMinutes"].values for name, group in df.groupby("Airline")]

# Perform one-way ANOVA
anova_result = stats.f_oneway(*airline_delays)

print("ANOVA Result:")
print(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}")

# Interpretation
if anova_result.pvalue < 0.05:
    print("There is a significant difference in delays between airlines.")
else:
    print("There is no significant difference in delays between airlines.")

# %% [markdown]
# ## INSIGHTS:
#

# %% [markdown]
# ### a. Provide a summary of the key findings from the data.
#
# #### Key Findings
#
# 1. **Delay Distribution**: The majority of flights have delays less than 30 minutes, with a few flights experiencing significant delays.
# 2. **Average Delay by Airline**: [Insert specific findings based on `average_delay_airline`].
# 3. **Impact of Departure Time**: Flights departing later in the day tend to have higher average delays.
# 4. **Statistical Significance**: ANOVA results indicate that there is a significant difference in delays between different airlines.
#

# %% [markdown]
# ### b. Analyze the impact of departure times on delays.
#
