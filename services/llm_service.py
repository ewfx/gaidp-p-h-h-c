from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

def query_llm(model_name, query, relevant_docs):
    llm = ChatGoogleGenerativeAI(model=model_name)
    combined_input = (
        "Here are some documents that might help answer the question: "
        + query
        + "\n\nRelevant Documents:\n"
        + "\n\n".join([doc.page_content for doc in relevant_docs])
    )

    messages = [
        SystemMessage(content="You are a financial risk expert working in a bank."),
        HumanMessage(content=combined_input),
    ]
    result = llm.invoke(messages)
    return result
    # print(result.content)