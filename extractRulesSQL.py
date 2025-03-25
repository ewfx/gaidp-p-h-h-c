import json
import duckdb
import re
import pandas as pd
from configuration.config import CONFIG

def extract_rules_sql():
    # File path
    file_path = CONFIG["GENERATED_SQL_PATH"]

    # Read the file and extract JSON content
    with open(file_path, "r") as file:
        content = file.read()

    # Find the JSON part by identifying the first and last square brackets
    start = content.find("[")
    end = content.rfind("]") + 1
    rules_sql = []
    # Extract and parse the JSON into a dictionary
    if start != -1 and end != -1:
        json_content = content[start:end]
        try:
            rules_sql = json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
    else:
        print("No valid JSON content found.")
    return rules_sql

def flagTransactions(rulesQueries = []):
    # Path to your CSV file
    csv_file = CONFIG["DATA_FILE_PATH"]
    df = pd.read_csv(csv_file)



    modified_queries = [query['query'].replace("your_table_name", f"df") for query in rulesQueries]
    results = []
    rules_linked = []
    for i in range(len(modified_queries)):
        try:
            res_df = duckdb.query(modified_queries[i]).df()
            if not res_df.empty:
                results.append(res_df)
                rules_linked.append(rulesQueries[i]["rule"])
        except Exception as e:
            continue

    # Display the result
    return results, rules_linked

