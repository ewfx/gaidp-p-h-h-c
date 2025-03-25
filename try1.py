import re

# Read the content from the file
file_path = "a1.txt"
with open(file_path, "r") as file:
    content = file.read()

# Regex pattern to extract SQL queries
sql_pattern = r"(SELECT\b.*?;)"
queries = re.findall(sql_pattern, content, re.DOTALL | re.IGNORECASE)

# Display the extracted SQL queries
# print("\n--- Extracted SQL Queries ---\n")
print(queries)
for i, query in enumerate(queries, 1):
    print(f"{query}")
