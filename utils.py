import os
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout
import base64
from io import BytesIO
import streamlit as st


PLATFORMS = ["OpenAI","ZhipuAI","vLLM"] # ["fastchat"] ,

def get_llm_models(platform_type: Literal[tuple(PLATFORMS)], base_url: str="", api_key: str="EMPTY"):
    if platform_type == "ZhipuAI":
        return [
            'glm-4-alltools',
            'glm-4-plus',
            'glm-4-0520',
            'glm-4',
            'glm-4-air',
            'glm-4-airx',
            'glm-4-long',
            'glm-4-flashx',
            'glm-4-flash'
        ]
    elif platform_type == "OpenAI":
        return [
            'gpt-4.1',
            'gpt-4o',
            'gpt-4.1-mini',
            'gpt-4o-mini',
            'gpt-3.5-turbo'
        ]
    # elif platform_type == "vLLM":
    #     return [
    #         'qwen',
    #         'baichuan',
    #         'chatglm'
    #     ]


def get_chatllm(
        platfrom_type: Literal[tuple(PLATFORMS)],
        model: str,
        base_url: str = "",
        api_key: str = "",
        temperature: float = 0.1
):
    if platfrom_type == "ZhipuAI":
        if not base_url:
            base_url = "https://open.bigmodel.cn/api/paas/v4"
        if not api_key:
            api_key = os.getenv('ZHIPUAI_API_KEY')
    elif platfrom_type == "OpenAI":
        if not base_url:
            base_url = os.getenv('OPENAI_BASE_URL')
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
    
    return ChatOpenAI(
        temperature=temperature,
        model_name=model,
        streaming=True,
        base_url=base_url,
        api_key=api_key,
    )

def get_img_base64(file_name: str) -> str:
    image_path = os.path.join(os.path.dirname(__file__),"img", file_name)
    with open(image_path, "rb") as f:
        buffer = BytesIO(f.read())
        base_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{base_str}"







































