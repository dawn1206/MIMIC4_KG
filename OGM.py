from py2neo import Node
from py2neo.ogm import GraphObject, Property

def typechecked_attribute(expected_type):
    def decorator(f):
        def wrapper(self, value):
            if not isinstance(value, expected_type):
                raise TypeError(f"Expected {expected_type}, got {type(value)}")
            f(self, value)
        return wrapper
    return decorator

class Patient:
    def __init__(self, subject_id=None, anchor_age=None, anchor_year=None, gender=None):
        self.node = Node("Patient")
        self.subject_id = subject_id
        self.anchor_age = anchor_age
        self.anchor_year = anchor_year
        self.gender = gender

class Prescription:
    def __init__(self, subject_id=None, hadm_id=None, starttime=None, stoptime=None, drug_type=None, drug=None, doses_per_24_hrs=None, form_val_disp=None, dose_unit_rx=None, dose_val_rx=None, form_unit_disp=None, route=None):
        self.node = Node("Prescription")
        self.subject_id = subject_id
        self.hadm_id = hadm_id
        self.starttime = starttime
        self.stoptime = stoptime
        self.drug_type = drug_type
        self.drug = drug
        self.doses_per_24_hrs = doses_per_24_hrs
        self.form_val_disp = form_val_disp
        self.dose_unit_rx = dose_unit_rx
        self.dose_val_rx = dose_val_rx
        self.form_unit_disp = form_unit_disp
        self.route = route

class Medication:
    def __init__(self, drug=None, prod_strength=None, gsn=None, form_rx=None):
        self.node = Node("Medication")
        self.drug = drug
        self.prod_strength = prod_strength
        self.gsn = gsn
        self.form_rx = form_rx

    # 对应的 getter 和 setter 方法，使用适当的数据类型进行类型检查
    # 例如，drug 和 prod_strength 可能是字符串类型

class Diagnose:
    def __init__(self, icd_code=None, subject_id=None, seq_num=None, hadm_id=None, icd_version=None):
        self.node = Node("Diagnose")
        self.icd_code = icd_code
        self.subject_id = subject_id
        self.seq_num = seq_num
        self.hadm_id = hadm_id
        self.icd_version = icd_version

    # 对应的 getter 和 setter 方法，使用适当的数据类型进行类型检查
    # 例如，subject_id 和 hadm_id 可能是整数类型
class DiagnoseDetail:
    def __init__(self, icd_code=None, icd_version=None, long_title=None):
        self.node = Node("DiagnoseDetail")
        self.icd_code = icd_code
        self.icd_version = icd_version
        self.long_title = long_title

class Omr:
    def __init__(self, result_name=None, seq_num=None, chartdate=None, subject_id=None, result_value=None):
        self.node = Node("Omr")
        self.result_name = result_name
        self.seq_num = seq_num
        self.chartdate = chartdate
        self.subject_id = subject_id
        self.result_value = result_value

    # 对应的 getter 和 setter 方法，使用适当的数据类型进行类型检查
    # 例如，seq_num 和 subject_id 可能是整数类型
