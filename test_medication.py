import unittest
from py2neo import Graph
from OGM_CURD import medication_service  # 确保从正确的模块导入 medication_service 类

class TestMedicationService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 连接到您的 Neo4j 数据库
        cls.graph = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))  # 请替换为您的实际密码
        cls.service = medication_service(cls.graph)

    def test_medication_workflow(self):
        # 测试创建药物
        created_medication = self.service.create_medication("AmoxicillinT", "12345", "500mg", "Tablet")
        self.assertIsNotNone(created_medication)
        self.assertEqual(created_medication['drug'], "AmoxicillinT")

        # 测试查询药物
        queried_medication = self.service.query_medication("AmoxicillinT")
        self.assertIsNotNone(queried_medication)
        self.assertEqual(queried_medication['drug'], "AmoxicillinT")

        # 测试更新药物
        updated_medication = self.service.update_medication("AmoxicillinT", "67890", "250mg", "Capsule")
        self.assertIsNotNone(updated_medication)
        self.assertEqual(updated_medication['prod_strength'], "250mg")
        self.assertEqual(updated_medication['form_rx'], "Capsule")

        # 测试删除药物
        self.service.remove_medication("AmoxicillinT")
        deleted_medication = self.service.query_medication("AmoxicillinT")
        self.assertIsNone(deleted_medication)

if __name__ == '__main__':
    unittest.main()
