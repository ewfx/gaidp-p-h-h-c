import os
from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import sys
from configuration.config import CONFIG
import time

# Force UTF-8 for printing
sys.stdout.reconfigure(encoding='utf-8')

def save_generated_rules(response):
    with open(CONFIG['GENERATED_RULES_PATH'], 'a', encoding='utf-8') as f:
        f.write(response)

def save_generated_sql( response):
    with open(CONFIG['GENERATED_SQL_PATH'], 'a', encoding='utf-8') as f:
        f.write(response)

def load_generated_rules():
    if os.path.exists(CONFIG['GENERATED_RULES_PATH']):
        with open(CONFIG['GENERATED_RULES_PATH'], 'r', encoding='utf-8') as f:
            return f.read()
    return ""

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def generate_sql_from_rules():
    generate_rules = load_generated_rules()

    query = "Generate executable SQL queries for the given rules in JSON format with two fields: rule, containing a clear description of the rule, and query, containing the corresponding SQL query. Assume all fields referenced in the rules belong to a single table, and use the exact field names provided. Ensure the SQL queries include standard SQL syntax for filtering, validation, and flagging transactions. Handle data type checks, range validations, format compliance, and missing/null value checks. Use logical operators such as AND, OR, and functions like IS NULL, LIKE, and BETWEEN appropriately. Write the queries in a consistent format for readability and execution, and return the full record when the condition is met using SELECT * or the relevant fields. The output should be a JSON array, with each object containing the rule and the corresponding query. If data point is not availaible don not post some random value, fill it with some relevant values"

    combined_input = (
        "Here are some documents that might help answer the question: "
        + query
        + f"\n\nGiven Rules:\n{generate_rules}"
    )
    # Define the messages for the model
    messages = [
        SystemMessage(content="You are a SQL expert."),
        HumanMessage(content=combined_input),
    ]
    result = llm.invoke(messages)
    save_generated_sql(result.content)


def generate_rules():
    # Define the directory containing the PDF file and the persistent directory
    file_path = CONFIG["COMPLIANCE_DOC_FILE_PATH"]

    pdf = PdfReader(file_path)
    # Generate the required page numbers
    PAGE_INTERVAL = 5
    PAGE_START = 166
    PAGE_END = 181
    pages_to_load = list(range(PAGE_START, PAGE_END, PAGE_INTERVAL))
    print(pages_to_load)

    # Ensure the PDF file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )

        # Read text from PDF
    for start_page_num in pages_to_load:
        raw_text = ""
        for page_num in range(start_page_num, min(start_page_num + PAGE_INTERVAL, PAGE_END)):
            content = pdf.pages[page_num].extract_text()
            if content:
                raw_text += f"\n{content}"


        query = "Generate data profiling rules for the Corporate Loan Data Schedule based on the fields, rule descriptions, and allowable values provided in the document. Create specific rules to flag transactions that violate data integrity, consistency, completeness, and accuracy standards. Ensure the rules account for data types (e.g., numeric, string, date validation), value ranges and limits (e.g., min/max amounts, valid date ranges), format validation (e.g., valid currency codes, date formats), null or missing values, and referential integrity (e.g., valid relationships between fields). Use clear and concise rule syntax that can be easily interpreted by an LLM or used in a profiling tool. Do not include explanations—only return the profiling rules. Provide the rules in json format."

        combined_input = (
            "Here are some documents that might help answer the question: "
            + query
            + "\n\nRelevant Documents:\n"
            + "\n\n".join([raw_text])
        )
        # Define the messages for the model
        messages = [
            SystemMessage(content="You are a financial risk expert working in a bank."),
            HumanMessage(content=combined_input),
        ]
        result = llm.invoke(messages)
        save_generated_rules(result.content)
        time.sleep(1.5)
        print(f"Request sent: {start_page_num} to {min(start_page_num + PAGE_INTERVAL, PAGE_END)}")

def model():
    generate_rules()
    generate_sql_from_rules()

# model()