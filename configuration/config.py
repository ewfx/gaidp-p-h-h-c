import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "COMPLIANCE_DOC_FILE_PATH": os.path.join(CURRENT_DIR, "../documents", "finra.pdf"),
    "OUTPUT_PATH": os.path.join(CURRENT_DIR, "../documents", "extracted_text.txt"),
    "GENERATED_RULES_PATH": os.path.join(CURRENT_DIR, "../db", "generated_rules.txt"),
    "GENERATED_SQL_PATH": os.path.join(CURRENT_DIR, "../db", "generated_SQL.txt"),
    "LLM_MODEL": "gemini-1.5-pro",
    "DATA_FILE_PATH": os.path.join(CURRENT_DIR, "../documents", "reporting_data.csv"),
    "DATA_DIR": os.path.join(CURRENT_DIR, "../documents"),
}