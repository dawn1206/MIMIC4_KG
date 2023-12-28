from datetime import datetime, timedelta

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from graphdatascience import GraphDataScience
from py2neo import Graph
from OGM_CURD import *
from bert_classifier import BertClassifier
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
db_driver = Graph(URI, auth=(USERNAME, PASSWORD))
gds = GraphDataScience(URI,auth=(USERNAME, PASSWORD))
BertClassifier = BertClassifier(r'C:\Users\12064\PycharmProjects\mimic\utils\results\best', r'C:\Users\12064\PycharmProjects\mimic\bert', r"C:\Users\12064\PycharmProjects\mimic\utils\label_encoder.pkl")
class controller():
    def __init__(self, db_driver:Graph,service_type:str):
        self.service_list = {
            "patient":patient_service,
            "prescription":prescription_service,
            "medication":medication_service,
            "diagnose":diagnose_service,
            "diagnoseDetail":diagnoseDetail_service,
            "omr":omr_service,
            "cypher":cypher_service
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

    def cypher(self, cypher_query:str):
        method = getattr(self.service, "cypher_"+self.service_type, None)
        if method is None:
            return None
        return method(cypher_query)

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

@app.get("/query/prescription_patient")
async def run_query(request: Request):
    '''
    患者所有处方记录
    :param request: subject_id
    :return: Json
    '''
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])

    # 参数化查询
    cypher_query = "MATCH (p:Patient)-[r]->(pp:Prescription) WHERE p.subject_id=$subject_id RETURN p, r, pp limit 10"
    response = db_driver.run(cypher_query, subject_id=subject_id).data()
    return response

#患者检查项目记录
@app.get("/query/omr_patient")
async def run_query(request: Request):
    '''
    患者所有检查项目记录
    :param request:     subject_id
    :return:        Json
    '''
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])

    # 参数化查询
    cypher_query = "MATCH (p:Patient)-[r]->(o:Omr) WHERE p.subject_id=$subject_id RETURN p, r, o limit 10"
    response = db_driver.run(cypher_query, subject_id=subject_id).data()
    return response

#按照时间查找患者检查项目记录
@app.get("/query/omr_patient_by_date")
async def run_query(request: Request):
    '''
    患者所有检查项目记录
    :param request: subject_id,chartdate
    :return: Json
    '''
    # 获取查询参数作为字典 chartdate: 2180-05-07
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])
    chartdate = query_params["chartdate"]
    print(chartdate)
    print(type(chartdate))
    # 参数化查询
    cypher_query = "MATCH (p:Patient)-[r]->(o:Omr) \
                    WHERE p.subject_id=$subject_id and o.chartdate=$chartdate\
                    RETURN p, r, o \
                    limit 10"
    response = db_driver.run(cypher_query, subject_id=subject_id,chartdate=chartdate).data()
    return response

#患者历史疾病信息
@app.get("/query/issue_patient")
async def run_query(request: Request):
    '''
    患者所有疾病信息
    :param request: subject_id
    :return: JSON
    '''

    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])

    # 参数化查询
    cypher_query = "MATCH (p:Patient)-[r:HAS_DIAGNOSE]->(o:Diagnose)\
                                     -[r2:HAS_DETAIL]->(dd:DiagnoseDetail)\
                    WHERE p.subject_id=$subject_id \
                    RETURN p.subject_id,o.hadm_id,dd.long_title \
                    limit 10"
    response = db_driver.run(cypher_query, subject_id=subject_id).data()
    return response

@app.get("/query/omr_patient")
async def run_query(request: Request):
    '''
    患者所有检查项目记录
    :param request: subject_id
    :return: JSON
    '''
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])

    # 参数化查询
    cypher_query = "MATCH (p:Patient)-[r]->(o:Omr) WHERE p.subject_id=$subject_id RETURN p, r, o limit 10"
    response = db_driver.run(cypher_query, subject_id=subject_id).data()
    return response

#患者用药历史记录
@app.get("/query/medHistory_patient")
async def run_query(request: Request):
    '''
    患者所有用药历史记录
    :param request: subject_id
    :return: JSON
    '''

    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])

    # 参数化查询
    cypher_query = "MATCH (p:Patient)-[r]->(pp:Prescription), \
                   (d:Medication)-[r2]->(pp)\
                   WHERE p.subject_id=$subject_id  \
                   RETURN p AS patient, pp.starttime AS starttime, pp.stoptime AS stoptime,d as Medication\
                   limit 10"
    response = db_driver.run(cypher_query, subject_id=subject_id).data()
    return response

@app.get("/query/info_patient_by_date")
async def run_query(request: Request):
    '''
    患者所有处方、诊断、检查记录
    :param request: subject_id,chartdate
    :return: JSON
    '''
    # 获取查询参数作为字典
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])
    chartdate = query_params["chartdate"]

    # 计算日期范围
    chartdate_obj = datetime.strptime(chartdate, "%Y-%m-%d")
    start_date = (chartdate_obj - timedelta(days=3)).strftime("%Y-%m-%d")
    end_date = (chartdate_obj + timedelta(days=3)).strftime("%Y-%m-%d")
    print(start_date)
    print(end_date)

    # 参数化查询
    cypher_query = """
    MATCH (p:Patient)-[r]->(o:Omr),(p)-[r2]->(pp:Prescription)-[r3]->(d:Diagnose)-[r4]->(dd:DiagnoseDetail)
    WHERE p.subject_id=$subject_id 
      AND o.chartdate >= $start_date AND o.chartdate <= $end_date 
    RETURN p AS patient, pp AS prescription, o AS omr, dd.long_title 
    LIMIT 10
    """
    response = db_driver.run(cypher_query, subject_id=subject_id, start_date=start_date, end_date=end_date).data()
    pre_list = list()
    omr_list = list()
    diagnose_list = list()
    for r in response:
        pre_list.append(r["prescription"])
        omr_list.append(r["omr"])
        diagnose_list.append(r["dd.long_title"])
    return {"patient":response[0]["patient"],
            "prescription":pre_list,
            "omr":omr_list,
            "diagnose":diagnose_list} if response else None

# 连接到Neo4j数据库
@app.get("/query/med_diagnose")
async def run_query(request: Request):
    # 获取查询参数
    query_params = dict(request.query_params)
    icd_version = int(query_params["icd_version"])
    icd_code = query_params["icd_code"]
    # 检查子图是否存在
    graph_exists = gds.graph.exists("subGraphofdia")

    if not graph_exists.any():
        # 创建子图的Cypher查询
        # 定义Cypher查询
        cypher_query = """
        MATCH (d:DiagnoseDetail)<-[:PRE_OF_DIA]-(p:Prescription), (m:Medication)-[:USED_IN]->(p)
        WHERE d.icd_code = $icd_code AND d.icd_version = $icd_version
        RETURN gds.graph.project(
            $graph_name,
            {
                DiagnoseDetail: { label: 'DiagnoseDetail', properties: {} },
                Prescription: { label: 'Prescription', properties: {} },
                Medication: { label: 'Medication', properties: {} }
            },
            {
                PRE_OF_DIA: { type: 'PRE_OF_DIA', orientation: 'UNDIRECTED' },
                USED_IN: { type: 'USED_IN', orientation: 'UNDIRECTED' }
            }
        )
        """

        # 执行Cypher查询并创建子图
        G, result = gds.graph.cypher.project(
            cypher_query,
            database="neo4j",
            graph_name="subGraphofdia",
            icd_code="00845",  # 示例: "00845"
            icd_version=9,  # 示例: 9
        )


    if graph_exists.any():
        print("subGraphofdia exists")

        # 运行degree centrality算法
        degree_centrality_query = """
        CALL gds.degree.stream('subGraphofdia')
        YIELD nodeId, score
        WHERE 'Medication' IN labels(gds.util.asNode(nodeId))
        RETURN gds.util.asNode(nodeId).drug AS medicationDrug, score
        ORDER BY score DESC limit 20
        """
        results = gds.run_cypher(degree_centrality_query)
        diag = db_driver.run("Match (d:DiagnoseDetail) Where d.icd_code=$icd_code and d.icd_version=$icd_version return d", icd_code=icd_code, icd_version=icd_version).data()
        return [diag,results["medicationDrug"]]
    else:
        return None


@app.get("/analysis_omr")
async def analysis_omr(request: Request):
    query_params = dict(request.query_params)
    subject_id = int(query_params["subject_id"])
    chartdate = query_params["chartdate"]

    # 参数化查询
    cypher_query = "MATCH (o:Omr) WHERE o.subject_id=$subject_id and o.chartdate=date($chartdate) RETURN o"
    response = db_driver.run(cypher_query, subject_id=subject_id,chartdate=chartdate).data()

    bert_input = ""
    for i in response:
        bert_input += i["o"]["result_name"] + " " + i["o"]["result_value"] + " "
    out = BertClassifier.predict(bert_input)[0].split("_")
    print(out)
    output = {
        "icd_code":out[0].strip("\""),
        "icd_version":int(out[1])
              }

    return output
    # BertClassifier.predict()
    # medication_list = list()
    # for i in response:
    #     medication_list.append(i["medication"])
    # return {"diagnose":response[0]["diagnose"],
    #         "medication":medication_list} if response else None
