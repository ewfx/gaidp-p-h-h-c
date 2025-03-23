from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def initialize_vector_store(output_path, persistent_directory, embedding_model):
    print("Initializing vector store...")
    loader = TextLoader(output_path, encoding='utf-8')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=3000,
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(documents)
    print(f"Number of document chunks: {len(docs)}")

    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
    print("Vector store created and persisted.")
    return db

def load_vector_store(persistent_directory, embedding_model):
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    return Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

def retrieve_documents(db, query, k=3):
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return retriever.invoke(query)