import unittest
from py2neo import Graph
from OGM_CURD import diagnoseDetail_service

class TestDiagnoseDetailService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 连接到您的Neo4j数据库
        cls.graph = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))
        cls.service = diagnoseDetail_service(cls.graph)

    def test_diagnoseDetail_workflow(self):
        # 测试创建诊断详情
        created_diagnoseDetail = self.service.create_diagnoseDetail("ICD10", 10, "Sample Description")
        self.assertIsNotNone(created_diagnoseDetail)
        self.assertEqual(created_diagnoseDetail['icd_code'], "ICD10")

        # 测试查询诊断详情
        queried_diagnoseDetail = self.service.query_diagnoseDetail("ICD10")
        self.assertIsNotNone(queried_diagnoseDetail)
        self.assertEqual(queried_diagnoseDetail['icd_code'], "ICD10")

        # 测试更新诊断详情
        updated_diagnoseDetail = self.service.update_diagnoseDetail("ICD10", 11, "Updated Description")
        self.assertIsNotNone(updated_diagnoseDetail)
        self.assertEqual(updated_diagnoseDetail['icd_version'], 11)
        self.assertEqual(updated_diagnoseDetail['long_title'], "Updated Description")

        # 测试删除诊断详情
        self.service.remove_diagnoseDetail("ICD10")
        deleted_diagnoseDetail = self.service.query_diagnoseDetail("ICD10")
        self.assertIsNone(deleted_diagnoseDetail)

if __name__ == '__main__':
    unittest.main()
