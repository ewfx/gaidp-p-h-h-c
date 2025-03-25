import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import sys
from configuration.config import CONFIG

# Force UTF-8 for printing
sys.stdout.reconfigure(encoding='utf-8')

def save_chat_history(user_input, response):
    with open(CONFIG['CHAT_HISTORY_PATH'], 'a', encoding='utf-8') as f:
        f.write(f"User: {user_input}\nAI: {response}\n\n")

def load_chat_history():
    if os.path.exists(CONFIG['CHAT_HISTORY_PATH']):
        with open(CONFIG['CHAT_HISTORY_PATH'], 'r', encoding='utf-8') as f:
            return f.read()
    return ""

load_dotenv()

# Define the directory containing the PDF file and the persistent directory
file_path = "documents/finra.pdf"
output_path = "documents/extracted_text.txt"
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

pdf = PdfReader(file_path)
# Generate the required page numbers
pages_to_load = list(range(165,170))

# Ensure the PDF file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"The file {file_path} does not exist. Please check the path."
    )

    # Read text from PDF
raw_text = ""
for page_num in pages_to_load:
    content = pdf.pages[page_num].extract_text()
    if content:
        # Fix broken words by removing line breaks followed by non-space characters
        raw_text += f"\n--- Page {page_num + 1} ---\n{content}"

        # embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        # embeddings = embeddings_model.embed_documents(output_path)

query = "Generate data profiling rules for Corporate Loan Data Schedule based on fields provided as per regulatory standard considering the rule description and allowable values provided in the document Generate RULES that can be used to flag transactions, just return a json containing two field in first field is rule and second is the coresponding sql query without explanation "

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
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
save_chat_history(query, result.content)

# Check if the Chroma vector store already exists


# if not os.path.exists(persistent_directory):
#     print("Persistent directory does not exist. Initializing vector store...")

#     print("\n--- Creating embeddings model ---")
    
# # Load the extracted text using UTF-8 encoding
#     loader = TextLoader(output_path, encoding='utf-8')
#     documents = loader.load()

#     # Configure a reliable text splitter
#     text_splitter = CharacterTextSplitter(
#         separator=" ",  
#         chunk_size=3000,    
#         chunk_overlap=100
#     )
#     docs = text_splitter.split_documents(documents)

#     # Debug output
#     print(f"Number of document chunks: {len(docs)}")

#     # Create the vector store and persist it automatically
#     print("\n--- Creating vector store ---")
#     db = Chroma.from_documents(
#         docs, embeddings, persist_directory=persistent_directory)

# else:
#     print("Vector store already exists. No need to initialize.")


# # Load the existing vector store with the embedding function
# db = Chroma(persist_directory=persistent_directory,
#             embedding_function=embeddings)
# #Define the user's question
# # query = "Generate data profiling rules for Corporate Loan Data Schedule based on field number 1 to 5 as per regulatory standard considering the rule description and allowable values provided in the document Generate only rules that can be used to flag transactions without explanation."
# # query = "Now generate the sql query for each rule"
# query = "can you generate mapping of the rule to sql query in form of json, Only return the json"
# # Retrieve relevant documents based on the query
# retriever = db.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3},
# )
# relevant_docs = retriever.invoke(query)

# # print("\n--- Relevant Documents ---")
# # for i, doc in enumerate(relevant_docs, 1):
# #     print(f"Document {i}:\n{doc.page_content}\n")


# # Combine the query and the relevant document contents
# combined_input = (
#     "Here are some documents that might help answer the question: "
#     + query
#     + "\n\nRelevant Documents:\n"
#     + "\n\n".join([doc.page_content for doc in relevant_docs])
#     + "\n\nPlease provide a answer based the provided documents.'."
# )

# # Create a Chat model
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
# chat_history = load_chat_history()

# combined_input = (
#     "Here are some documents that might help answer the question: "
#     + query
#     + "\n\nRelevant Documents:\n"
#     + "\n\n".join([doc.page_content for doc in relevant_docs])
#     + f"\n\nChat History:\n{chat_history}"
# )
# # Define the messages for the model
# messages = [
#     SystemMessage(content="You are a financial risk expert working in a bank."),
#     HumanMessage(content=combined_input),
# ]
# result = llm.invoke(messages)
# print(result.content)
# save_chat_history(query, result.content)

# print(result.content)