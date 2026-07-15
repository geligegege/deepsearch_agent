#对chat聊天助手和对应的会话处理
import os

from sympy import pager_print

from ragflow.rag_config import _load_ragflow_env
from ragflow_sdk import RAGFlow

#创建一个ragflow客户端
api_key, base_url = _load_ragflow_env()
ragflow_client = RAGFlow(api_key=api_key, base_url=base_url)

#1、查询知识库中有哪些聊天助手和对应的信息（rag分别对应的数据）
def get_assisstant_list():
    #1、创建客户端
    #2、查询所有聊天助手
    chat_list=ragflow_client.list_chats()
    #3、查询聊天助手的知识库信息
    count_chat_info=""
    for chat in chat_list:
        dataset_names = []
        dataset_list=chat.datasets#查询聊天助手对应的知识库信息
        if dataset_list and isinstance(dataset_list,list):
            for dataset in dataset_list:
                print(dataset)
                dataset_names.append(dataset['name'])#将一个助手所有知识库的名字加入到列表中
        #拼接当前助手信息和知识库信息    
        count_chat_info+=f"助手名称：{chat.name},功能介绍：{chat.description},对应的知识库有：{','.join(dataset_names)}\n"    
    #4、拼接助手和知识库信息，返回供模型参考
    return count_chat_info
#2、创建会话提问再删除对话
def ask_question(chat_name,question):
    """
    向某个助手发起提问：1、创建会话 2、提问 3、关闭会话
    :param chat_name:助手的名字
    :param question:本次提问的问题
    :return 返回提问的结果
    """
    #1、创建客户端
    #2、查询对应name的chat
    chats=ragflow_client.list_chats(name=chat_name)
    use_chat=chats[0]
    #3、创建会话
    session=use_chat.create_session(name=f"{chat_name}_session")
    #4、提问
    response=session.ask(question,stream=True)#流式返回结果，边生成边返回，适合长文本的回答

    result=""
    for item in response:
        #数据存在对象中的content中
        result=item.content
    #5、关闭会话
    use_chat.delete_sessions(ids=[session.id])
    #6、返回提问结果
    return result

if __name__ == "__main__":
    #1、查询当前有哪些助手和对应的知识库信息
    chat_info=get_assisstant_list()
    print(chat_info)
    #2、向某个助手提问
    question_result=ask_question("法律援助助手","杀人犯法吗")
    print(question_result)
