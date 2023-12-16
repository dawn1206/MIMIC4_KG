import unittest
from py2neo import Graph, NodeMatcher
from OGM_CURD import diagnose_service  # 请确保导入正确

class TestDiagnoseService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))  # 替换为您的认证信息
        cls.service = diagnose_service(cls.graph)

    def test_diagnose_workflow(self):
        # 测试删除诊断
        self.service.remove_diagnose(123, 456)
        # 测试创建诊断
        created_diagnose = self.service.create_diagnose(123, 456, 1, "ICD9_123", "Sample Description")
        self.assertIsNotNone(created_diagnose)

        # 测试查询诊断
        queried_diagnose = self.service.query_diagnose(123, 456, 1)
        self.assertIsNotNone(queried_diagnose)
        self.assertEqual(queried_diagnose["icd_code"], "ICD9_123")

        # 测试更新诊断
        updated_diagnose = self.service.update_diagnose(123, 456, 1, "ICD9_456", "Updated Description")
        self.assertIsNotNone(updated_diagnose)
        self.assertEqual(updated_diagnose["icd_code"], "ICD9_456")

        # 测试删除诊断
        self.service.remove_diagnose(123, 456)
        deleted_diagnose = self.service.query_diagnose(123, 456, 1)
        self.assertIsNone(deleted_diagnose)

if __name__ == '__main__':
    unittest.main()
