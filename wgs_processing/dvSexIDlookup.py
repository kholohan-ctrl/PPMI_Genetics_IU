import pandas as pd

# Load files
# batch = "dv_AN00027509"
# batch = "dv_SS02"
#batch = "dv_AN00027984-second"
# batch = "dv_20260429merged1"
# batch = "dv_20260429NOTmerged1"
# batch = 'cram20260429merged3'
dir = "C:/Users/jbmchls/Indiana University/Nudelman, Kelly Nicole Holohan - Jessie_Projects/PPMI/WGS_processing/"
invdir = "C:/Users/jbmchls/Indiana University/Nudelman, Kelly Nicole Holohan - PPMI_Genetics_IUTeam/Current_Samples_WGS_GWAS_Trackers/"
batch = 'cram20260817_test1'
batch_dir = 'ngdpr_20260817'
csv_df = pd.read_csv(f"{dir}{batch_dir}/dv_{batch}_filled.csv")        # contains DeepVariant.sample_name
# csv_df = pd.read_csv("C:/Users/mz22/OneDrive - Indiana University/dv_AN00024381.csv")        # contains DeepVariant.sample_name
# csv_df = pd.read_csv("C:/Users/mz22/OneDrive - Indiana University/dv_AN00024273.csv")        # contains DeepVariant.sample_name
# excel_df = pd.read_excel("C:/Users/mz22/OneDrive - Indiana University/PPMI/query770sexPPMIID.xlsx")   # contains GP2ID, biological_sex, clinical_id
excel_file = f"{invdir}WGS_NeuroX_Samples Shipped_Barcode_20250509_20260605.xlsx"
ship_df = pd.read_excel(excel_file)
# ship_df = pd.read_excel("C:/Users/mz22/OneDrive - Indiana University/PPMI/WGS_NeuroX_Samples Shipped_Barcode_20250509_20260323.xlsx")
# master_df = pd.read_excel("C:/Users/mz22/OneDrive - Indiana University/PPMI/release10_PPMI-N_master_key_n3033.xlsx")   # contains GP2ID, biological_sex, clinical_id
# master_df = pd.read_excel("C:/Users/mz22/OneDrive - Indiana University/PPMI/release10_PPMI-G_master_key_n621.xlsx")   # contains GP2ID, biological_sex, clinical_id
# if batch=="dv_AN00027984-first140":
#     ship_df['Sex '] = ship_df['Sex '].map({
#         0: 'female',
#         1: 'male'
#     })
#     merged_df = csv_df.merge(
#         ship_df[['PPMI ID (PATNO)', 'Sex ']],
#         left_on='clinical_id',
#         right_on='PPMI ID (PATNO)',
#         how='left'
#     )
#     # merged_df['biological_sex_for_qc'] = merged_df['biological_sex_for_qc'].str.lower()
#
#     # Optional: drop GP2ID if redundant
#     # merged_df = merged_df.drop(columns=['GP2ID'])
#
#     # Save result
#     merged_df.to_csv(f"C:/Users/mz22/OneDrive - Indiana University/PPMI/{batch}merged.csv", index=False)

if True:
    ship_df['Sex '] = ship_df['Sex '].map({
        0: 'female',
        1: 'male'
    })
    merged_df = csv_df.merge(
        ship_df[['PPMI ID (PATNO)', 'Sex ']],
        left_on='DeepVariant.sample_name',
        right_on='PPMI ID (PATNO)',
        how='left'
    )
    merged_df['DeepVariant.sex'] = merged_df['Sex ']
    # merged_df['biological_sex_for_qc'] = merged_df['biological_sex_for_qc'].str.lower()

    # Optional: drop GP2ID if redundant
    # merged_df = merged_df.drop(columns=['GP2ID'])

    # Save result
    merged_df.to_csv(f"{dir}{batch_dir}/dv_{batch}_filledwSex.csv", index=False)
#
# elif "AN" in batch:
#     # Merge (left join keeps all CSV rows)
#     merged_df = csv_df.merge(
#         excel_df[['GP2ID', 'biological_sex_for_qc', 'clinical_id']],
#         left_on='DeepVariant.sample_name',
#         right_on='GP2ID',
#         how='left'
#     )
#     merged_df['biological_sex_for_qc'] = merged_df['biological_sex_for_qc'].str.lower()
#
#     # Optional: drop GP2ID if redundant
#     merged_df = merged_df.drop(columns=['GP2ID'])
#
#     # Save result
#     merged_df.to_csv(f"C:/Users/mz22/OneDrive - Indiana University/PPMI/{batch}merged.csv", index=False)
#
# else:
#     merged_df = csv_df.merge(
#         master_df[['clinical_idPPMISI', 'biological_sex_for_qc']],
#         left_on='DeepVariant.sample_name',
#         right_on='clinical_idPPMISI',
#         how='left'
#     )
#     merged_df['biological_sex_for_qc'] = merged_df['biological_sex_for_qc'].str.lower()
#
#     # Optional: drop GP2ID if redundant
#     # merged_df = merged_df.drop(columns=['GP2ID'])
#
#     # Save result
#     merged_df.to_csv(f"C:/Users/mz22/OneDrive - Indiana University/PPMI/{batch}merged.csv", index=False)


print(merged_df)