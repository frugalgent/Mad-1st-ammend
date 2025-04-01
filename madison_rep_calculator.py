import requests
import sqlite3
import pandas as pd

# URL for census data (update if necessary)
CENSUS_API_URL = "https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=state:*&key=808d796f7763bc01ffaff601695c85e784eea615"

# SQLite Database
DB_NAME = "census_data.db"
TABLE_NAME = "state_population"

# Function to fetch census data
def fetch_census_data():
    response = requests.get(CENSUS_API_URL)

    # Print response details for debugging
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Content:", response.text)  # Print the raw response

    # Handle empty response
    if response.status_code != 200 or not response.text.strip():
        raise Exception("Error: Received an empty or invalid response from Census API.")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"JSON parsing error: {e}\nResponse Content: {response.text}")

    # Convert to DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])  # Use first row as column names
    df = df.rename(columns={"NAME": "state_name", "P1_001N": "population", "state": "state_fips"})
    df["population"] = df["population"].astype(int)

    return df

# Function to store data in SQLite
def store_data_in_db(df):
    conn = sqlite3.connect(DB_NAME)

    # Store using renamed column names
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

    conn.close()

# Function to calculate representatives based on Madison's 1st Amendment
def calculate_representatives(df):
    results = []
    for _, row in df.iterrows():
        state = row["state_name"]  # Changed from "state" to "state_name"
        population = row["population"]

        if population < 30000:
            reps = 1  # Ensure at least 1 representative
        elif population < 100 * 30000:  # First 100 reps
            reps = population // 30000
        elif population < 200 * 40000:  # Next 100 reps
            reps = max(100, population // 40000)
        else:  # Beyond 200 reps
            reps = max(200, population // 50000)

        results.append({"State": state, "Population": population, "Representatives": reps})

    return pd.DataFrame(results)

# Main execution
if __name__ == "__main__":
    print("Fetching census data...")
    census_df = fetch_census_data()

    print("Storing data in database...")
    store_data_in_db(census_df)

    print("Calculating representatives...")
    results_df = calculate_representatives(census_df)

    print("Results:")
    print(results_df)