import streamlit as st
from utils import get_img_base64
from dotenv import load_dotenv, find_dotenv
from pages import chat_page, main

load_dotenv(find_dotenv())

if __name__ == "__main__":
    # with st.sidebar:
    #     st.logo(
    #         get_img_base64("logo.png"),
    #         size="large",
    #         icon_image=get_img_base64("stitch2.png"),
    #     )

    pg = st.navigation({
        "对话": [
            st.Page(chat_page, title="对话", icon=":material/chat_bubble:"),
            st.Page(main, title="PDF 阅读", icon=":material/chat:"),

        ],
    })
    pg.run()