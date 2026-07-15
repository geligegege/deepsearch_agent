from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
import os

# 加载环境变量
load_dotenv(find_dotenv())#find_dotenv()会自动查找当前目录及父目录的.env文件，并加载环境变量

model = init_chat_model(
    model=os.getenv("LLM_xiaomi"),  # 从环境变量读取模型名称
    model_provider="openai"          # 指定模型提供商
)