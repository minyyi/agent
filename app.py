import os
import streamlit as st

from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate


st.set_page_config(
    page_title="tax bot",
    page_icon=":guardsman", #이모지 아이콘
    layout="wide",  #레이아웃
    initial_sidebar_state="expanded",   #사이드바 초기상태
)

st.title("Stream 기본예제")
st.caption("소득세에 관련된 모든 것을 답변해드립니다 :)")

load_dotenv()

index_name = 'tax-index'
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)
if "message_list" not in st.session_state:
    st.session_state.message_list = []
    
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def get_ai_message(user_message):
    
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embedding,
    )

    llm = ChatOpenAI(model='gpt-4o')
    prompt = hub.pull("rlm/rag-prompt")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

#dictionary prompt

    dictionary = ["사람을 나타내는 표현 -> 거주자"]

    prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경할 필요가 없다고 판단 된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        그런 경우에는 질문만 리턴해주세요
        사전: {dictionary}
        질문: {{question}}
        """)

    dictionary_chain = prompt | llm | StrOutputParser()
    #내 질문을 그대로 변경하지 않고 보낼지, 거주자로 변경해서 보낼지 판단하게됨.  outparser에게 전달
    #그 데이터 값이 dictionary_chain

    tax_chain = {"query": dictionary_chain} | qa_chain

    ai_message = tax_chain.invoke({"question": user_message})

    return ai_message['result']

# print(f"before == {st.session_state.message_list}")

if user_question := st.chat_input(placeholder="소득세에 관련하여 궁금한 내용을 말씀해주세요"):
    # pass
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    with st.spinner("답변을 생성하는 중입니다."):
        ai_message = get_ai_message(user_question)
        with st.chat_message("ai"):
            st.write(ai_message)
        st.session_state.message_list.append({"role": "ai", "content": ai_message})
    

# print(f"after == { st.session_state.message_list}")