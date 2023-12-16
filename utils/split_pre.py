import pandas as pd

# 读取原始 CSV 文件
df = pd.read_csv('../data_file/filtered_prescriptions.csv')

# 定义 Prescription 和 Medication 的列
prescription_columns = ['subject_id', 'hadm_id', 'starttime', 'stoptime', 'drug_type', 'drug', 'dose_val_rx', 'dose_unit_rx', 'form_val_disp', 'form_unit_disp', 'doses_per_24_hrs', 'route']
medication_columns = ['drug', 'gsn', 'prod_strength', 'form_rx']

# 创建 Prescription 和 Medication 的数据框
prescription_df = df[prescription_columns]
medication_df = df[medication_columns].drop_duplicates()

# 保存为新的 CSV 文件
prescription_df.to_csv('split_prescription.csv', index=False)
medication_df.to_csv('split_medication.csv', index=False)
