from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
# from split_1 import split_karo
# from split_2 import split_karo_2
import streamlit as st

load_dotenv()

st.title("API Documentation Assistant")

embeddings = OpenAIEmbeddings()
llm = ChatGroq(model='llama3-8b-8192')
llm = ChatOpenAI(model = 'gpt-4o')

vector_store = FAISS.load_local(
    "faiss_index_2", embeddings, allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5})

prompt = PromptTemplate.from_template("""
    You are an expert in the API of a company that provides data enrichment services. 
    You will be asked questions about the API and how to use it.
    Do not make up any answers. If you do not know the answer, say so.
    If you receive any urls in the context, you can mention them in your response as well. 
    Don't mention context in your response. Chat as if you are an HUMAN expert in the API. 
    Since you are an expert in the API Documentation, you never ask the user to refer to the documentation.
    Provide definite, concise answers.
    Answer in markdown format.
    
    Context: {context}
    Given the context, provide a response to the following question:
    Question: {input}
""")

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, combine_docs_chain)

user_question = st.text_area("Ask a question about the API:", height=100)

if st.button("Get Answer"):
    if user_question:
        with st.spinner("Generating response..."):
            response = chain.invoke({"input": user_question})
            st.markdown(response['answer'])
    else:
        st.warning("Please enter a question")
