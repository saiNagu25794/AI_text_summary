import time

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
#
# headers = {
#     "authorization" : st.secrets["OPENAI_API_KEY"],
#     "content_type" : "application/json"
# }


from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


def summarize_with_options(input_text, num_words, format):
    chat_messages = [
        SystemMessage(content='You are an expert assistant with expertise in summarizing text'),
        HumanMessage(
            content=f'Please provide a {format} summary of the following speech in {num_words} words:\n TEXT: {input_text}')
    ]

    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-0125')
    summary = llm.invoke(chat_messages).content
    return summary


def get_pdf_text(pdf_docs):
    text = ""
    pdf_reader = PdfReader(pdf_docs)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def translate_text(text, target_language):
    generic_template = '''
    Translate the following text to {language}:

    {text}
    '''
    prompt = PromptTemplate(
        input_variables=['text', 'language'],
        template=generic_template
    )

    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    llm_chain = LLMChain(llm=llm, prompt=prompt)  # Use complete instead of run
    response = llm_chain.invoke({'text': text, 'language': target_language})
    return response


def stream_data(response_text):
    for word in response_text.split(" "):
        yield word + " "
        time.sleep(0.05)
