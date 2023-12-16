import unittest
from py2neo import Graph
from OGM_CURD import PrescriptionService

class TestPrescriptionService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 连接到您的Neo4j数据库

        cls.graph = Graph("bolt://localhost:7687", auth=("neo4j", "xyt020122"))
        cls.service = PrescriptionService(cls.graph)

    def test_prescription_workflow(self):
        # 测试创建处方
        created_prescription = self.service.create_prescription(
            123, 456, "2023-01-01", "2023-01-10", "Antibiotic", "Amoxicillin",
            "2", "500mg", "mg", "500", "mg", "Oral"
        )
        self.assertIsNotNone(created_prescription)
        self.assertEqual(created_prescription['subject_id'], 123)
        self.assertEqual(created_prescription['hadm_id'], 456)

        # 测试查询处方
        queried_prescription = self.service.query_prescription(123, 456)
        self.assertIsNotNone(queried_prescription)
        self.assertEqual(queried_prescription['subject_id'], 123)
        self.assertEqual(queried_prescription['hadm_id'], 456)

        # 测试更新处方
        updated_prescription = self.service.update_prescription(
            123, 456, "2023-01-02", None, "Analgesic", "Paracetamol", None, None, None, None, None, None
        )
        self.assertIsNotNone(updated_prescription)
        self.assertEqual(updated_prescription['drug_type'], "Analgesic")
        self.assertEqual(updated_prescription['drug'], "Paracetamol")

        # 测试删除处方
        self.service.remove_prescription(123, 456)
        deleted_prescription = self.service.query_prescription(123, 456)
        self.assertIsNone(deleted_prescription)

if __name__ == '__main__':
    unittest.main()
