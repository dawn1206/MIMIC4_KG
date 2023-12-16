import unittest
from py2neo import Graph
from OGM_CURD import patient_service

class TestPatientService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 连接到您的Neo4j数据库
        cls.graph = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))
        cls.service = patient_service(cls.graph)

    def test_patient_workflow(self):
        # 测试创建病人
        created_patient = self.service.create_patient(123, 30, 2023, "M")
        self.assertIsNotNone(created_patient)
        self.assertEqual(created_patient['subject_id'], 123)

        # 测试查询病人
        queried_patient = self.service.query_patient(123)
        self.assertIsNotNone(queried_patient)
        self.assertEqual(queried_patient['subject_id'], 123)

        # 测试更新病人
        updated_patient = self.service.update_patient(123, 35, 2024, "F")
        self.assertIsNotNone(updated_patient)
        self.assertEqual(updated_patient['anchor_age'], 35)
        self.assertEqual(updated_patient['anchor_year'], 2024)
        self.assertEqual(updated_patient['gender'], "F")

        # 测试删除病人
        self.service.remove_patient(123)
        deleted_patient = self.service.query_patient(123)
        self.assertIsNone(deleted_patient)

if __name__ == '__main__':
    unittest.main()
