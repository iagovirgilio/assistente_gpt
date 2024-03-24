import os
import streamlit as st
from langchain_community.vectorstores.faiss import FAISS
# from langchain.vectorstores import FAISS
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
# from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader

load_dotenv()

# Obtém a chave de API do ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

loader = UnstructuredExcelLoader("base/base.xlsx")
# loader = UnstructuredWordDocumentLoader("base/base.docx", mode="elements", strategy="fast")
document = loader.load()
embedes = OpenAIEmbeddings()
db = FAISS.from_documents(document, embedes)


def retrieve_query(query):
    similar_responses = db.similarity_search(query, k=3)
    return [doc.page_content for doc in similar_responses]

llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo-16k-0613", temperature=1.1)

template = """
Você é um assistente virtual que trabalha no setor de suporte ao cliente de um
software ERP chamado Simples Varejo.

Aqui está a mensagem do cliente:
{message}

Aqui está uma documentação para basear a resposta:
{best_pratice}

Caso a resposta não seja encontrada peça o cliente para entrar em conato com o suporte por telefone ou email.

Responda em portugues a melhor resposta para o cliente.
"""
prompt = PromptTemplate(
    input_variables=["message", "best_pratice"],
    template=template,
)

chain = LLMChain(
    llm=llm, prompt=prompt
)

def generate_response(message):
    best_pratice = retrieve_query(message)
    response = chain.predict(message=message, best_pratice=best_pratice)
    return response

resposta = generate_response(input("Olá qual sua dúvida?: "))

print("-" * 100)
print(resposta)
print("-" * 100)
