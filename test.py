import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

result = llm.invoke('how ai is really cool')

print(result.content)