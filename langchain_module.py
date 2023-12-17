from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

with open('openai_key.txt', 'r') as keyfile:
    api_key = keyfile.read()

llm = ChatOpenAI(openai_api_key=api_key)

text = 'What could be question about Tableau at Data Analyst job interview?'
#messages = [HumanMessage(content=text)

response = llm.invoke(text)
print(response.content)
