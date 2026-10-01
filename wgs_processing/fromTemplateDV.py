import csv
from pathlib import PurePosixPath

dir = "C:/Users/jbmchls/Indiana University/Nudelman, Kelly Nicole Holohan - Jessie_Projects/PPMI/WGS_processing/"
batchname = 'cram20260817_test1'
batch_dir = 'ngdpr_20260817'
# batchname = 'cram20260429merged3'
csv_in = f"{dir}mz_scripts/dv_template.csv"
txt_in = f"{dir}{batch_dir}/{batchname}.txt"
csv_out = f"{dir}{batch_dir}/dv_{batchname}_filled.csv"

# Read the template CSV
with open(csv_in, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    template_rows = list(reader)

if not fieldnames:
    raise ValueError("CSV has no header row.")

if not template_rows:
    raise ValueError("CSV has no data row to use as the template.")

template = template_rows[0]

# Read URIs from the text file
with open(txt_in, encoding="utf-8") as f:
    uris = [line.strip() for line in f if line.strip()]

# Build output rows
output_rows = []
for uri in uris:
    row = dict(template)  # copy all other columns from first data row

    row["DeepVariant.input_cram_or_bam"] = uri
    row["DeepVariant.input_cram_or_bam_index"] = uri + ".crai"
    filename = PurePosixPath(uri).name
    # sample_name = filename.removesuffix(".cram")
    if filename.endswith(".cram"):
        sample_name = filename[:-5]
    else:
        sample_name = filename
    row["DeepVariant.sample_name"] = sample_name

    output_rows.append(row)

# Write populated CSV
with open(csv_out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Wrote {len(output_rows)} rows to {csv_out}")