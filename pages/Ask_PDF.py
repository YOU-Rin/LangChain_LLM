from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from utils import PLATFORMS, get_llm_models, get_chatllm, get_img_base64


CHAT_PAGE_INTRODUCTION = "你好，我是你的 KK_chat 智能助手，当前页面为`对话模式`，可以直接与大模型对话，有什么可以帮助你的吗？"


def display_chat_history():
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"], avatar=get_img_base64("stitch.png") if message["role"] == "assistant" else None):
            st.write(message["content"])

# 清空历史对话信息
"""
清空当前会话状态中的聊天历史
重新添加欢迎消息作为对话起点
"""
def clear_chat_history():
    st.session_state["chat_history"] = [
            {"role": "assistant", "content": CHAT_PAGE_INTRODUCTION}
        ]


def clear_chat_history():
    st.session_state["chat_history"] = [
            {"role": "assistant", "content": CHAT_PAGE_INTRODUCTION}
        ]
    

def main():
    load_dotenv()
    #st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")

    with st._bottom:
        cols = st.columns([1.2, 10, 1])  # 使用三列布局；配置按钮(1.2)、输入框(10)、清空按钮(1)
        with cols[0].popover(":gear:", use_container_width=True, help="配置模型"):
            platform = st.selectbox("请选择要使用的模型加载方式", PLATFORMS)
            llm_models = get_llm_models(platform)
            model = st.selectbox("请选择要使用的模型", llm_models)
            temperature = st.slider("请选择模型 Temperature", 0.1, 1., 0.1)
            history_len = st.slider("请选择历史消息长度", 1, 10, 5)
        user_question = cols[1].chat_input("请输入您的问题")  # 输入框
        cols[2].button(":wastebasket:", help="清空对话", on_click=clear_chat_history)  # 清空按钮

    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    # extract the text
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
        
      # split into chunks
      text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
      )
      chunks = text_splitter.split_text(text)
      
      # create embeddings
      embeddings = OpenAIEmbeddings()
      knowledge_base = FAISS.from_texts(chunks, embeddings)
      st.write("PDF Upload Sucessful")
      
      # show user input
      #user_question = st.text_input("Ask a question about your PDF:")
      if user_question:
        with st.chat_message("user"):
           st.write(user_question)

        docs = knowledge_base.similarity_search(user_question)
        llm = get_chatllm(platform, model, temperature=temperature)
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          print(cb)
        
        with st.chat_message("assistant"):
           answer = st.write(response)
        st.session_state["chat_history"] += [{'role': 'assistent', 'content': answer}]
    

# if __name__ == '__main__':
#     main()