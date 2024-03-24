import os
import streamlit as st
from langchain_community.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders.excel import UnstructuredExcelLoader

load_dotenv()

def load_document():
    loader = UnstructuredExcelLoader("base/base.xlsx")
    return loader.load()

def retrieve_similar_responses(db, query, k=3):
    similar_responses = db.similarity_search(query, k=k)
    return [doc.page_content for doc in similar_responses]

def initialize_llm(openai_api_key):
    return ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo-16k-0613", temperature=0)

def generate_response(llm, message, best_practice):
    response = llm.predict(message=message, best_practice=best_practice)
    return response

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("Chave de API do OpenAI não configurada. Por favor, configure a variável de ambiente OPENAI_API_KEY.")
        return

    document = load_document()
    if not document:
        st.error("Erro ao carregar o documento base.")
        return

    embedes = OpenAIEmbeddings()
    db = FAISS.from_documents(document, embedes)

    llm = initialize_llm(openai_api_key)

    template = """
    Você é um assistente virtual que trabalha no setor de suporte ao cliente de um
    software ERP chamado Simples Varejo.

    Aqui está a mensagem com dúvida do cliente:
    {message}

    Aqui está uma documentação para se basear na resposta:
    {best_practice}

    Caso a resposta não seja encontrada na documentação passada, peça o cliente para entrar em contato com o suporte por telefone ou email.

    Responda em português a melhor resposta para o cliente.
    """
    prompt = PromptTemplate(
        input_variables=["message", "best_practice"],
        template=template,
    )

    chain = LLMChain(
        llm=llm, prompt=prompt
    )

    user_question = input("Olá, qual é a sua dúvida? ")
    best_practice = retrieve_similar_responses(db, user_question)
    response = generate_response(chain, user_question, best_practice)

    print("-" * 100)
    print(response)
    print("-" * 100)

if __name__ == "__main__":
    main()