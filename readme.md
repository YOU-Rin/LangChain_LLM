LLM 对话系统

## 功能
base_chat.py    提供基础的大语言模型对话功能，基于OpenAI的模型
Ask_PDF.py      提供PDF阅读功能，您可以上传您的PDF文件，并对其进行提问

## 环境创建
conda create -n LLM python=3.10 -y
conda activate LLM

## 安装依赖
pip install -r requirements.txt

## 添加自己的API_KEY
在 .env文件中添加自己的API_KEY才可以访问模型

## 运行

运行main.py文件
streamlit run main.py 