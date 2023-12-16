import pandas as pd


def filter_omr_by_patients(patients_file, omr_file, output_file=None):
    # Load the datasets
    patients = pd.read_csv(patients_file)
    omr = pd.read_csv(omr_file)

    # Filter the OMR data to only include records where subject_id exists in the patients dataframe
    filtered_omr = omr[omr['subject_id'].isin(patients['subject_id'])]

    # If an output file is specified, save the filtered data
    if output_file:
        filtered_omr.to_csv(output_file, index=False)

    return filtered_omr

def drop(csv_file,dst_file):
    df = pd.read_csv(csv_file)
    # 删除不需要的列
    columns_to_drop = ['pharmacy_id', 'poe_id', 'poe_seq', 'order_provider_id', 'formulary_drug_cd', 'ndc']
    df.drop(columns=columns_to_drop, inplace=True)

    # 如果需要，将修改后的数据帧保存回 CSV 文件
    df.to_csv(dst_file, index=False)

if __name__ == "__main__":
    patients_csv = r".\kg_patients.csv"
    omr_csv = r".\filtered_diagnoses_icd.csv"
    filtered_omr_csv = r".\filtered_diagnoses_icd.csv"
    # patients = pd.read_csv(patients_csv)[:3000]
    # patients.to_csv(patients_csv)
    # Filter the OMR records and save to a new CSV file
    new_omr = filter_omr_by_patients(patients_csv, omr_csv, filtered_omr_csv)
    # print(new_omr.head())
    # prescriptions = "./filtered_prescriptions.csv "
    # drop(prescriptions,"filtered_prescriptions.csv")