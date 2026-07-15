# 定义一个网络搜索的工具！
# ======================== 导入核心依赖 ========================
# 类型注解：增强代码提示和静态检查能力
from typing import  Literal
# LangChain 工具装饰器：将普通函数转为 Agent 可调用的工具
from langchain_core.tools import tool
# Tavily 官方客户端：实现网络搜索核心功能
from tavily import TavilyClient

# 系统/第三方依赖
import os  # 系统路径/环境变量处理
from dotenv import load_dotenv  # 加载 .env 文件中的环境变量

# 自定义模块：工具调用埋点监控（需确保 api 模块可导入）
from api.monitor import monitor

# ======================== 初始化配置 ========================
# 加载项目根目录的 .env 文件，读取环境变量（如 TAVILY_API_KEY）
load_dotenv()

# 步骤1： 定义一个TavilyClient对象
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#步骤2：定义一个工具函数，使用 @tool 装饰器暴露给 Agent 调用
@tool
def internet_search(
    query: str,
    search_type: Literal["general", "news", "academic"] = "general",
    max_results: int = 5,
    include_raw_content: bool = False
):
    """
    互联网搜索工具，基于 Tavily API 实现网络信息检索。
    注意：主要搜索公开的网络信息！如果指定查询数据库或者rag不能使用此工具!
    :param query: 搜索关键词
    :param search_type: 搜索类型，默认为 "general"，可选 "news" 或 "academic"
    :param max_results: 返回的最大结果数量，默认为 5
    :param include_raw_content: 是否包含原始内容，默认为 False（仅返回摘要）
    :return: 搜索结果字符串
    """
    # 埋点监控：记录工具调用日志（可选）
    monitor.report_tool(
        tool_name="internet_search",
        parameters={
            "query": query,
            "search_type": search_type,
            "max_results": max_results,
            "include_raw_content": include_raw_content
        }
    )
    
    # 调用 Tavily 客户端执行搜索，并返回结果
    return tavily_client.search(
        query=query,
        topic=search_type,
        num_results=max_results,
        include_raw_content=include_raw_content
    )