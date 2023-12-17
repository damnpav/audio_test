from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


llm = ChatOpenAI(openai_api_key='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')

text = 'Tell me what do you know about Tableau?'
#messages = [HumanMessage(content=text)

llm.invoke(text)
