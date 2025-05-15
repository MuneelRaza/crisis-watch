from dotenv import load_dotenv
load_dotenv()

import time
from langchain_together import ChatTogether



llm = ChatTogether(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
)

