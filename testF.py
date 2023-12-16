from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

# 数据库驱动实例
db_driver = None

# 数据库连接信息
URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "xyt020122"

@app.on_event("startup")
async def startup_event():
    global db_driver
    db_driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

@app.on_event("shutdown")
async def shutdown_event():
    db_driver.close()

@app.get("/query")
async def run_query():
    with db_driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 10")
        return [record["n"] for record in result]
