from langchain_together import ChatTogether
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()




llm = ChatNVIDIA(model="mistralai/mixtral-8x7b-instruct-v0.1")

# result = llm.invoke("Write a ballad about LangChain.")
# print(result.content)

llama = 'meta/llama-3.3-70b-instruct'

llama_model = ChatNVIDIA(model=llama)

