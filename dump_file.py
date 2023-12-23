from py2neo import Graph
from OGM_CURD import *
import pandas as pd

# 数据库连接信息
URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "xyt020122"

# 数据库驱动实例
db_driver = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))

patient = pd.read_csv("./data_file/kg_patients.csv")
subject_id_list = patient["subject_id"].tolist()


    #run cypher
query = f"match (p:Patient) return p"
result = db_driver.run(query).data()
for i in query:
    if len(result) == 0:
        print(i)
        continue
    else:
        print(result[0]["p"]["subject_id"])
        continue