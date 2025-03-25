import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from configuration.config import CONFIG

def save_chat_history(user_input, response):
    with open(CONFIG['CHAT_HISTORY_PATH'], 'a', encoding='utf-8') as f:
        f.write(f"User: {user_input}\nAI: {response}\n\n")

def load_chat_history():
    if os.path.exists(CONFIG['CHAT_HISTORY_PATH']):
        with open(CONFIG['CHAT_HISTORY_PATH'], 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def clear_chat_history():
    if os.path.exists(CONFIG['CHAT_HISTORY_PATH']):
        open(CONFIG['CHAT_HISTORY_PATH'], 'w', encoding='utf-8').close()
        print("Chat history cleared.")
    else:
        print("No chat history found.")

def query_llm(model_name, query, relevant_docs):
    llm = ChatGoogleGenerativeAI(model=model_name)
    chat_history = load_chat_history()

    combined_input = (
        "Here are some documents that might help answer the question: "
        + query
        + "\n\nRelevant Documents:\n"
        + "\n\n".join([doc.page_content for doc in relevant_docs])
        + f"\n\nChat History:\n{chat_history}"
    )

    messages = [
        SystemMessage(content="You are a financial risk expert working in a bank."),
        HumanMessage(content=combined_input),
    ]
    result = llm.invoke(messages)
    print(result.content)
    save_chat_history(query, result.content)
    return result.content
