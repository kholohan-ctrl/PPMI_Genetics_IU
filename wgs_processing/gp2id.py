import pandas as pd
import re

# Input files
batchname = '20260817n'
dir = "C:/Users/jbmchls/Indiana University/Nudelman, Kelly Nicole Holohan - Jessie_Projects/PPMI/WGS_processing/ngdpr_20260817/"
invdir = "C:/Users/jbmchls/Indiana University/Nudelman, Kelly Nicole Holohan - PPMI_Genetics_IUTeam/Current_Samples_WGS_GWAS_Trackers/"
# csv_file = f"{dir}multiInputs_20260429merged1.csv"
# csv_file = f"{dir}multiInputs_20260429NOTmerged1.csv"
# csv_file = f"{dir}multiInputs_20260429NOTmerged1.csv"
# filename = 'multiinputs-5firstpart-path'
filename = f'multiinputs-{batchname}-path'
csv_file = f"{dir}{filename}.csv"

#excel_file = f"{dir}wgs20260429_pg2IDs_with_PPMI_IDs_Date_Shipped.xlsx"
excel_file = f"{invdir}WGS_NeuroX_Samples Shipped_Barcode_20250509_20260605.xlsx"
# Output file
# output_file = f"{dir}multiInputs_20260429NOTmerged1_filled.csv"
output_file = f"{dir}{filename}-ppmi.csv"

# Read files
csv_df = pd.read_csv(csv_file)
excel_df = pd.read_excel(excel_file)

# Build mapping: GP2 ID -> PPMI ID
mapping = dict(zip(excel_df["GP2 ID"], excel_df["PPMI ID (PATNO)"]))

# Function to extract GP2 ID from fastq_R2 path
def extract_gp2_id(path):
    """
    Example input:
    gs://.../PPMI-G_001351_merged_R2.fastq.gz

    Returns:
    PPMI-G_001351
    """
    match = re.search(r"(PPMI-G_\d+)", str(path))
    if match:
        return match.group(1)
    else:
        match = re.search(r"(PPMI-N_\d+)", str(path))
        if match:
            return match.group(1)
    return None

# Fill sample_name column
def map_sample_name(path):
    gp2_id = extract_gp2_id(path)
    if gp2_id in mapping:
        return mapping[gp2_id]
    return None

csv_df["fastq_to_cram.sample_name"] = csv_df[
    "fastq_to_cram.fastq_R1"
].apply(map_sample_name)

csv_df["fastq_to_cram.datatablefile.library_name"] = csv_df["fastq_to_cram.sample_name"]

# Save updated CSV
csv_df.to_csv(output_file, index=False)

print(f"Updated file saved as: {output_file}")