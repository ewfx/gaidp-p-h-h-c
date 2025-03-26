import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "COMPLIANCE_DOC_FILE_PATH": os.path.join(CURRENT_DIR, "../documents", "regulatory_instructions.pdf"),
    "OUTPUT_PATH": os.path.join(CURRENT_DIR, "../documents", "extracted_text.txt"),
    "GENERATED_RULES_PATH": os.path.join(CURRENT_DIR, "../db", "generated_rules.txt"),
    "GENERATED_SQL_PATH": os.path.join(CURRENT_DIR, "../db", "generated_SQL.txt"),
    "LLM_MODEL": "gemini-1.5-pro",
    "DATA_FILE_PATH": os.path.join(CURRENT_DIR, "../documents", "reported_data.csv"),
    "DATA_DIR": os.path.join(CURRENT_DIR, "../documents"),
    "EXPORT_RESULTS_PATH": os.path.join(CURRENT_DIR, "../outputs", "flaggedTransactions.xlsx"),
    "RESULT_RULES_MAPPING_PATH": os.path.join(CURRENT_DIR, "../outputs", "rules_mapping.txt"),
    "GENERATED_RULES_REPORT_PATH": os.path.join(CURRENT_DIR, "../outputs", "generated_rules_report.txt"),
}