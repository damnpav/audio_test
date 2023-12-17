from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


llm = ChatOpenAI(openai_api_key='')

text = 'Tell me what do you know about Tableau?'
#messages = [HumanMessage(content=text)

llm.invoke(text)
