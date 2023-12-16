import unittest
from py2neo import Graph
from OGM_CURD import OmrService

class TestOmrService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 连接到 Neo4j 数据库
        cls.graph = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))
        cls.service = OmrService(cls.graph)

    def test_omr_workflow(self):
        # 测试创建 OMR 记录
        created_omr = self.service.create_omr(123, 1, "2023-01-01", "Blood Test", "Normal")
        self.assertIsNotNone(created_omr)
        self.assertEqual(created_omr['subject_id'], 123)
        self.assertEqual(created_omr['seq_num'], 1)

        # 测试查询 OMR 记录
        queried_omr = self.service.query_omr(123, 1)
        self.assertIsNotNone(queried_omr)
        self.assertEqual(queried_omr['result_name'], "Blood Test")

        # 测试更新 OMR 记录
        updated_omr = self.service.update_omr(123, 1, result_value="High")
        self.assertIsNotNone(updated_omr)
        self.assertEqual(updated_omr['result_value'], "High")

        # 测试删除 OMR 记录
        self.service.remove_omr(123, 1)
        deleted_omr = self.service.query_omr(123, 1)
        self.assertIsNone(deleted_omr)

if __name__ == '__main__':
    unittest.main()
