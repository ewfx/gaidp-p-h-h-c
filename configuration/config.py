import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "COMPLIANCE_DOC_FILE_PATH": os.path.join(CURRENT_DIR, "../documents", "finra.pdf"),
    "OUTPUT_PATH": os.path.join(CURRENT_DIR, "../documents", "extracted_text.txt"),
    "PERSISTENT_DIRECTORY": os.path.join(CURRENT_DIR, "../db", "chroma_db"),
    "PAGES_TO_LOAD": list(range(4, 11)) + list(range(161, 255)),
    "EMBEDDING_MODEL": "models/text-embedding-004",
    "LLM_MODEL": "gemini-1.5-pro",
    "DATA_FILE_PATH": os.path.join(CURRENT_DIR, "../documents", "reporting_data.csv"),
    "DATA_DIR": os.path.join(CURRENT_DIR, "../documents"),
}