from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv

load_dotenv()


template = ChatPromptTemplate([
    ('system',
     """
     Translate the given English phrase into {language}.
     
     Provide output in EXACTLY this format:
     
     English: [original English phrase]
     {language}: [translation written in {language} script]
     {language} in English words: [write the Malayalam translation using English alphabet - same meaning but spelled in English letters, NOT the English translation]
     
     IMPORTANT: The third line should have the {language} words written in English letters, NOT the English meaning. Write how the {language} words are spelled/written using the English alphabet.
     """),
    ('user', '{input}')
])

llm = ChatGroq(model='llama-3.1-8b-instant')

outputParser = StrOutputParser()


chain = template | llm | outputParser

app = FastAPI(title="Fast API with Groq", version="0.1.0")

add_routes(app=app, runnable=chain, path='/translate')

uvicorn.run(app=app, port=8001, host="localhost")



