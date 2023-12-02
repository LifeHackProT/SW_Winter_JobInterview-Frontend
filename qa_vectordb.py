# 6_qa_vectordb.py by mentor Jeong
import dotenv
import os
# streamlit
import streamlit as st
# Pincone
import pinecone
# langchain
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
import chardet
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone


dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX="job"
PINECONE_ENVIRONMENT = "gcp-starter"

# open ai 임베딩
embeddings_model = OpenAIEmbeddings()

# text loading
DOC_PATH = "./overflow.txt"
loader = TextLoader(DOC_PATH, autodetect_encoding=True)
documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
# docs = text_splitter.split_documents(documents)
# st.write(docs[1])
# str1= ''.join(str(s) for s in docs)
# str2= str1.split('"')[1]
# st.write(str2)

# embeddings
embeddings = embeddings_model.embed_documents([documents[0].page_content])

# pinecone 설정
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
docsearch = Pinecone.from_documents(documents, embeddings_model, index_name=PINECONE_INDEX)


# Create OPENAI LLM instance
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
llm("give me a job interview question")
chain = load_qa_chain(llm, chain_type="stuff")


# query = how is overflow founded

def main():
    # Create a Streamlit app.
    st.title("Interview Practice App")

    # Prompt user to type their question
    query = st.text_input("Question: Type your question here. when you done, type quit:")

    st.markdown(reply(query))


def reply(query):
    if query:
        docs = docsearch.similarity_search(query)
        answer = chain.run(input_documents=docs, question=query)
        return answer


if __name__ == '__main__':
    main()