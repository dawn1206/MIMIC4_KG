
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from py2neo import Graph
from OGM_CURD import *

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 数据库连接信息
URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "xyt020122"

# 数据库驱动实例
db_driver = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))
class controller():
    def __init__(self, db_driver:Graph,service_type:str):
        self.service_list = {
            "patient":patient_service,
            "prescription":prescription_service,
            "medication":medication_service,
            "diagnose":diagnose_service,
            "diagnoseDetail":diagnoseDetail_service,
            "omr":omr_service
        }
        self.service_type = service_type
        self.service = self.service_list[service_type](db_driver)

    def query(self, **kwargs):
        method = getattr(self.service, "query_"+self.service_type, None)
        if method is None:
            return None
        ret = method(**kwargs)
        if ret:
            return ret
        else:
            return None

    def create(self, **kwargs):
        method = getattr(self.service, "create_"+self.service_type, None)
        print(method)
        if method is None:
            return None
        return method(**kwargs)

    def update(self, **kwargs):
        method = getattr(self.service, "update_"+self.service_type, None)
        if method is None:
            return None
        return method(**kwargs)

    def remove(self, **kwargs):
        method = getattr(self.service, "remove_"+self.service_type, None)
        if method is None:
            return None
        if method(**kwargs)=="success":
            return "success"
        else:
            return "fail delete"

@app.get("/")
async def main():
    return {"message": "Hello World"}

#query patient
@app.get("/{service_type}/query")
async def generic_query(service_type: str, request: Request):
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    controller_instance = controller(db_driver, service_type)
    response = controller_instance.query(**query_params)
    return response

#create patient
@app.get("/{service_type}/create")
async def generic_create(service_type: str, request: Request):
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    controller_instance = controller(db_driver, service_type)
    response = controller_instance.create(**query_params)
    return response

#update patient
@app.get("/{service_type}/update")
async def generic_update(service_type: str, request: Request):
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    controller_instance = controller(db_driver, service_type)
    response = controller_instance.update(**query_params)
    return response

#remove patient
@app.get("/{service_type}/remove")
async def generic_remove(service_type: str, request: Request):
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    controller_instance = controller(db_driver, service_type)
    response = controller_instance.remove(**query_params)
    return response
