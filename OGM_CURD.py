from connection import init_neo4j_graph
from OGM import *
from py2neo import Node, NodeMatcher
from py2neo.matching import *

class patient_service():
    def __init__(self, graph):
        self.graph = graph
        self.matcher = NodeMatcher(graph)

    def query_patient(self, subject_id):
        try:
            return self.matcher.match("Patient", subject_id=subject_id).first()
        except Exception as e:
            print(f"query patient failed: {e}")

    def create_patient(self, subject_id, anchor_age, anchor_year, gender):
        try:
            patient = Node("Patient", subject_id=subject_id, anchor_age=anchor_age, anchor_year=anchor_year, gender=gender)
            self.graph.create(patient)
            return patient
        except Exception as e:
            print(f"create patient failed: {e}")

    def update_patient(self, subject_id, anchor_age=None, anchor_year=None, gender=None):
        try:
            patient = self.query_patient(subject_id)
            if patient:
                if anchor_age is not None:
                    patient['anchor_age'] = anchor_age
                if anchor_year is not None:
                    patient['anchor_year'] = anchor_year
                if gender is not None:
                    patient['gender'] = gender
                self.graph.push(patient)
            return patient
        except Exception as e:
            print(f"update patient failed: {e}")

    def remove_patient(self, subject_id):
        try:
            patient = self.query_patient(subject_id)
            if patient:
                self.graph.delete(patient)
        except Exception as e:
            print(f"remove patient failed: {e}")

class PrescriptionService:
    def __init__(self, graph):
        self.graph = graph
        self.matcher = NodeMatcher(graph)

    def query_prescription(self, subject_id, hadm_id):
        prescription = None
        try:
            prescription = self.matcher.match("Prescription", subject_id=subject_id).first()
        except:
            print("query prescription failed")
        return prescription

    def create_prescription(self, subject_id, hadm_id, starttime, stoptime, drug_type, drug, doses_per_24_hrs, form_val_disp, dose_unit_rx, dose_val_rx, form_unit_disp, route):
        try:
            prescription = Node("Prescription", subject_id=subject_id, hadm_id=hadm_id, starttime=starttime, stoptime=stoptime, drug_type=drug_type, drug=drug, doses_per_24_hrs=doses_per_24_hrs, form_val_disp=form_val_disp, dose_unit_rx=dose_unit_rx, dose_val_rx=dose_val_rx, form_unit_disp=form_unit_disp, route=route)
            self.graph.create(prescription)
            return prescription
        except:
            print("create prescription failed")


    def update_prescription(self, subject_id, hadm_id, starttime=None, stoptime=None, drug_type=None, drug=None, doses_per_24_hrs=None, form_val_disp=None, dose_unit_rx=None, dose_val_rx=None, form_unit_disp=None, route=None):
        prescription= self.query_prescription(subject_id, hadm_id)
        if prescription:
            # 更新 prescription 的属性
            if starttime: prescription["starttime"] = starttime
            if stoptime: prescription["stoptime"] = stoptime
            if drug_type: prescription["drug_type"] = drug_type
            if drug: prescription["drug"] = drug
            if doses_per_24_hrs: prescription["doses_per_24_hrs"] = doses_per_24_hrs
            if form_val_disp: prescription["form_val_disp"] = form_val_disp
            if dose_unit_rx: prescription["dose_unit_rx"] = dose_unit_rx
            if dose_val_rx: prescription["dose_val_rx"] = dose_val_rx
            if form_unit_disp: prescription["form_unit_disp"] = form_unit_disp
            if route: prescription["route"] = route


            try:
                self.graph.push(prescription)
                return prescription
            except:
                print("update prescription failed")


    def remove_prescription(self, subject_id, hadm_id):
        prescription = self.query_prescription(subject_id, hadm_id)
        if prescription:
            try:
                self.graph.delete(prescription)
            except:
                print("remove prescription failed")
class medication_service():
    def __init__(self, graph):
        self.graph = graph
        self.matcher = NodeMatcher(graph)

    def query_medication(self, drug):
        try:
            medication_node = self.matcher.match("Medication", drug=drug).first()
            return medication_node
        except Exception as e:
            print(f"Query medication failed: {e}")
            return None

    def create_medication(self, drug, gsn, prod_strength, form_rx):
        medication_node = Node("Medication", drug=drug, gsn=gsn, prod_strength=prod_strength, form_rx=form_rx)
        try:
            self.graph.create(medication_node)
            return medication_node
        except Exception as e:
            print(f"Create medication failed: {e}")
            return None

    def update_medication(self, drug, gsn=None, prod_strength=None, form_rx=None):
        medication_node = self.query_medication(drug)
        if medication_node:
            if gsn is not None:
                medication_node['gsn'] = gsn
            if prod_strength is not None:
                medication_node['prod_strength'] = prod_strength
            if form_rx is not None:
                medication_node['form_rx'] = form_rx
            try:
                self.graph.push(medication_node)
                return medication_node
            except Exception as e:
                print(f"Update medication failed: {e}")
        return None

    def remove_medication(self, drug):
        medication_node = self.query_medication(drug)
        if medication_node:
            try:
                self.graph.delete(medication_node)
            except Exception as e:
                print(f"Remove medication failed: {e}")
        return None

class diagnose_service:
    def __init__(self, graph):
        self.graph = graph
        self.matcher = NodeMatcher(graph)

    def query_diagnose(self, subject_id, hadm_id, seq_num):
        diagnose_node = self.matcher.match("Diagnose", subject_id=subject_id, hadm_id=hadm_id, seq_num=seq_num).first()
        return diagnose_node

    def create_diagnose(self, subject_id, hadm_id, seq_num, icd_code, icd_version):
        diagnose = Node("Diagnose", subject_id=subject_id, hadm_id=hadm_id, seq_num=seq_num, icd_code=icd_code, icd_version=icd_version)
        self.graph.create(diagnose)
        return diagnose

    def update_diagnose(self, subject_id, hadm_id, seq_num=None, icd_code=None, icd_version=None):
        diagnose_node = self.matcher.match("Diagnose", subject_id=subject_id, hadm_id=hadm_id).first()
        if diagnose_node:
            if seq_num is not None:
                diagnose_node["seq_num"] = seq_num
            if icd_code is not None:
                diagnose_node["icd_code"] = icd_code
            if icd_version is not None:
                diagnose_node["icd_version"] = icd_version
            self.graph.push(diagnose_node)
            return diagnose_node
        else:
            return None

    def remove_diagnose(self, subject_id, hadm_id):
        diagnose_node = self.matcher.match("Diagnose", subject_id=subject_id, hadm_id=hadm_id).first()
        if diagnose_node:
            self.graph.delete(diagnose_node)


class diagnoseDetail_service:
    def __init__(self, graph):
        self.graph = graph
        self.matcher = NodeMatcher(graph)

    def query_diagnoseDetail(self, icd_code):
        diagnoseDetail_node = self.matcher.match("DiagnoseDetail", icd_code=icd_code).first()
        return diagnoseDetail_node

    def create_diagnoseDetail(self, icd_code, icd_version, long_title):
        diagnoseDetail = Node("DiagnoseDetail", icd_code=icd_code, icd_version=icd_version, long_title=long_title)
        self.graph.create(diagnoseDetail)
        return diagnoseDetail

    def update_diagnoseDetail(self, icd_code, icd_version=None, long_title=None):
        diagnoseDetail_node = self.matcher.match("DiagnoseDetail", icd_code=icd_code).first()
        if diagnoseDetail_node:
            if icd_version is not None:
                diagnoseDetail_node["icd_version"] = icd_version
            if long_title is not None:
                diagnoseDetail_node["long_title"] = long_title
            self.graph.push(diagnoseDetail_node)
            return diagnoseDetail_node
        else:
            return None

    def remove_diagnoseDetail(self, icd_code):
        diagnoseDetail_node = self.matcher.match("DiagnoseDetail", icd_code=icd_code).first()
        if diagnoseDetail_node:
            self.graph.delete(diagnoseDetail_node)

class OmrService:
    def __init__(self, graph):
        self.graph = graph
        self.matcher = NodeMatcher(graph)

    def query_omr(self, subject_id, seq_num):
        omr_node = self.matcher.match("Omr", subject_id=subject_id, seq_num=seq_num).first()
        return omr_node

    def create_omr(self, subject_id, seq_num, chartdate, result_name, result_value):
        omr = Node("Omr", subject_id=subject_id, seq_num=seq_num, chartdate=chartdate, result_name=result_name, result_value=result_value)
        self.graph.create(omr)
        return omr

    def update_omr(self, subject_id, seq_num, chartdate=None, result_name=None, result_value=None):
        omr_node = self.matcher.match("Omr", subject_id=subject_id, seq_num=seq_num).first()
        if omr_node:
            if chartdate is not None:
                omr_node["chartdate"] = chartdate
            if result_name is not None:
                omr_node["result_name"] = result_name
            if result_value is not None:
                omr_node["result_value"] = result_value
            self.graph.push(omr_node)
            return omr_node
        else:
            return None

    def remove_omr(self, subject_id, seq_num):
        omr_node = self.matcher.match("Omr", subject_id=subject_id, seq_num=seq_num).first()
        if omr_node:
            self.graph.delete(omr_node)
