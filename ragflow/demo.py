import os

from sympy import pager_print

from ragflow.rag_config import _load_ragflow_env
from ragflow_sdk import RAGFlow

#创建一个ragflow客户端
api_key, base_url = _load_ragflow_env()
ragflow_client = RAGFlow(api_key=api_key, base_url=base_url)

#代码创建知识库
def create_knowledge_base(kb_name: str,description:str="") -> str:
    """
    创建一个知识库,传入名字和描述
    :param kb_name: 知识库名称
    :param description: 知识库描述
    :return: 创建结果
    """
    try:
        response = ragflow_client.create_dataset(
            name=kb_name,
            description=description,
            embedding_model="text-embedding-v3@Tongyi-Qianwen",  # 必须指定嵌入模型
        )
        return f"知识库'{kb_name}'创建成功！ID: {response.id}"
    except Exception as e:
        return f"创建知识库出现异常：{str(e)}"

#上传文件到知识库
def upload_file_to_kb(kb_id: str, file_paths: str) -> str:
    """
    上传文件到指定知识库
    :param kb_id: 知识库ID
    :param file_path: 文件路径
    :return: 上传结果
    """
    #获取传入文件的知识库对象
    datasets = ragflow_client.list_datasets(id=kb_id, page=1, page_size=10) 
    dataset=datasets[0]
    #文件包装成对应的上传dict模式
    document_list = []
    for file_path in file_paths:
        file_name=os.path.basename(file_path)
        with open(file_path, "rb", encoding="utf-8") as f:
            blob = f.read()
            document_list.append({
                "display_name": file_name,
                "name": file_name,
                "blob": blob
            })
    dataset.upload_documents(document_list)        

if __name__ == "__main__":
    #1、创建知识库
    kb_result=create_knowledge_base("测试知识库","这是一个测试用的知识库")
    print(kb_result)
    
    