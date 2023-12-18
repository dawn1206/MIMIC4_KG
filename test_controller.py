from py2neo import Graph, Node, NodeMatcher
from controller import controller
# ... 包含 patient_service 和其他服务类的定义 ...

# 初始化数据库驱动
db_driver = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))

# 测试创建患者
def test_create_patient():
    controller_instance = controller(db_driver, "patient")
    patient = controller_instance.create(subject_id="11111", anchor_age=30, anchor_year=1990, gender="M")
    assert patient is not None
    assert patient["subject_id"] == "11111"
    print("Create patient test passed")

# 测试查询患者
def test_get_patient():
    controller_instance = controller(db_driver, "patient")
    patient = controller_instance.query(subject_id="11111")
    assert patient is not None
    assert patient["subject_id"] == "11111"
    print("Get patient test passed")

# 测试更新患者
def test_update_patient():
    controller_instance = controller(db_driver, "patient")
    patient = controller_instance.update(subject_id="11111", anchor_age=35)
    assert patient is not None
    assert patient["anchor_age"] == 35
    print("Update patient test passed")

# 测试删除患者
def test_remove_patient():
    controller_instance = controller(db_driver, "patient")
    result = controller_instance.remove(subject_id="11111")
    assert result == "success"
    print("Remove patient test passed")

# 运行测试
test_create_patient()
test_get_patient()
test_update_patient()
test_remove_patient()
