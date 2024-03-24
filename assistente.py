import os
import streamlit as st
from langchain_community.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders.excel import UnstructuredExcelLoader

load_dotenv()

class Assistente:
    def __init__(self, message):
        self.message = message
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.document = self.load_document()
        self.embedes = OpenAIEmbeddings()
        self.db = FAISS.from_documents(self.document, self.embedes)
        self.llm = self.initialize_llm(self.openai_api_key)

    def load_document(self):
        loader = UnstructuredExcelLoader("base/base.xlsx")
        return loader.load()

    def retrieve_similar_responses(self, query, k=3):
        similar_responses = self.db.similarity_search(query, k=k)
        return [doc.page_content for doc in similar_responses]

    def initialize_llm(self, openai_api_key):
        return ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo-16k-0613", temperature=0)

    def generate_response(self, message):
        context = self.retrieve_similar_responses(message)
        message_with_context = f"{message}\n\n{' '.join(context)}"
        response = self.llm.predict(text=message_with_context)
        return response

    def main(self):
        if not self.openai_api_key:
            st.error("Chave de API do OpenAI não configurada. Por favor, configure a variável de ambiente OPENAI_API_KEY.")
            return

        if not self.document:
            st.error("Erro ao carregar o documento base.")
            return

        template = """
        Você é um assistente virtual que trabalha no setor de suporte ao cliente de um
        software ERP chamado Simples Varejo.

        Aqui está a mensagem com dúvida do cliente:
        {message}

        Caso a resposta não seja encontrada na documentação passada, peça o cliente para entrar em contato com o suporte por telefone ou email.

        Responda em português a melhor resposta para o cliente.
        """
        prompt = PromptTemplate(
            input_variables=["message"],
            template=template,
        )

        chain = LLMChain(
            llm=self.llm, prompt=prompt
        )

        user_question = self.message
        response = self.generate_response(user_question)

        st.write(response)  # Escreve a resposta na interface Streamlit

if __name__ == "__main__":
    st.title("Assistente Virtual")
    user_question = st.text_input("Olá, qual é a sua dúvida?")
    if user_question:
        assistente = Assistente(user_question)
        assistente.main()
