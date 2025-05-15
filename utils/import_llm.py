from dotenv import load_dotenv
load_dotenv()

from langchain_nvidia_ai_endpoints import ChatNVIDIA



llm = ChatNVIDIA(model="mistralai/mixtral-8x7b-instruct-v0.1")

# result = llm.invoke("Write a ballad about LangChain.")
# print(result.content)