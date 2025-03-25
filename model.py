import os
import sys
from dotenv import load_dotenv
from services.extract import extract_pdf_text
from services.vector_store import initialize_vector_store, load_vector_store, retrieve_documents
from services.llm_service import query_llm, clear_chat_history
from configuration.config import CONFIG

sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

def main():
    print("1. Extract PDF and Process Data")
    print("2. Generate Query Results")
    print("3. Clear Chat History")
    choice = input("Choose an option: ")

    if choice == "1":
        # Step 1: Extract PDF text
        extract_pdf_text(CONFIG["FILE_PATH"], CONFIG["PAGES_TO_LOAD"], CONFIG["OUTPUT_PATH"])
        print("Extraction complete.")
    elif choice == "2":
        # Step 2: Initialize or load vector store
        if not os.path.exists(CONFIG["PERSISTENT_DIRECTORY"]):
            db = initialize_vector_store(CONFIG["OUTPUT_PATH"], CONFIG["PERSISTENT_DIRECTORY"], CONFIG["EMBEDDING_MODEL"])
        else:
            print("Vector store already exists. Loading existing data.")
            db = load_vector_store(CONFIG["PERSISTENT_DIRECTORY"], CONFIG["EMBEDDING_MODEL"])

        # Step 3: Perform document retrieval
        user_query = input("Enter your query: ")
        # user_query = "Generate data profiling rules for Schedule H-1 to flag the high risk transactions based on regulatory standards. Only provide the rules and do not provide the explanation, Generate atleast 30 rules but avoid redundancy"
        relevant_docs = retrieve_documents(db, user_query)

        # Step 4: Query the LLM
        query_llm(CONFIG["LLM_MODEL"], user_query, relevant_docs)
    elif choice == "3":
        # Step 5: Clear chat history
        clear_chat_history()
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    main()
