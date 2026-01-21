import csv
import random

# Configuration
FILENAME = "company_data.csv"
ROWS = 1000

# Sample Data Sources
industries = ["Technology", "Healthcare", "Finance", "Retail", "Energy", "Automotive", "Real Estate"]
cities = ["New York", "San Francisco", "London", "Berlin", "Tokyo", "Bangalore", "Sydney", "Toronto"]
countries = ["USA", "UK", "Germany", "Japan", "India", "Australia", "Canada"]
prefixes = ["Global", "Tech", "Smart", "Future", "Eco", "Prime", "Alpha", "Omega"]
suffixes = ["Corp", "Inc", "Ltd", "Solutions", "Systems", "Group", "Holdings"]

def generate_company_name():
    return f"{random.choice(prefixes)} {random.choice(suffixes)} {random.randint(1, 99)}"

# Open file and write data
print(f"Generating {ROWS} rows of data...")

with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write Header
    writer.writerow(["id", "company_name", "industry", "employees", "revenue_millions", "city", "country", "founded_year"])
    
    # Write Rows
    for i in range(1, ROWS + 1):
        writer.writerow([
            i,
            generate_company_name(),
            random.choice(industries),
            random.randint(10, 50000),         # Random employee count
            round(random.uniform(1.0, 500.0), 2), # Random revenue in millions
            random.choice(cities),
            random.choice(countries),
            random.randint(1950, 2023)
        ])

print(f"Data generation complete. File saved as {FILENAME}.")