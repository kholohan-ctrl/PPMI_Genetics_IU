version 1.0

workflow SmooveSingle {
  input {
    String sample
    File cram
    File cram_index
  }

  call RunSmoove {
    input:
      sample = sample,
      cram = cram,
      cram_index = cram_index,
  }

  output {
    File smoove_vcf = RunSmoove.vcf
    File smoove_vcf_index = RunSmoove.vcf_index
    File lumpy_command_script = RunSmoove.lumpy_cmd
  }
}

task RunSmoove {
  input {
    String sample
    File cram
    File cram_index

    File ref_fasta = "gs://iu-share-loni-2/ref/Homo_sapiens_assembly38.fasta"
    File ref_fai = "gs://iu-share-loni-2/ref/Homo_sapiens_assembly38.fasta.fai"
    File exclude_bed = "gs://intermed-files-wb-strong-apple-3019/resources/exclude.cnvnator_100bp.GRCh38.20170403.bed"
  }

  command <<<
    set -euo pipefail

    mkdir -p out

    smoove call \
      --outdir out \
      --exclude ~{exclude_bed} \
      --name ~{sample} \
      --fasta ~{ref_fasta} \
      -p 1 \
      --genotype \
      ~{cram}

    rm -f out/*.disc.bam* out/*.split.bam* out/*.histo out/*.orig.bam*
  >>>

  output {
    File vcf = "out/~{sample}-smoove.genotyped.vcf.gz"
    File vcf_index = "out/~{sample}-smoove.genotyped.vcf.gz.csi"
    File lumpy_cmd = "out/~{sample}-lumpy-cmd.sh"
  }

  runtime {
    docker: "brentp/smoove"
    cpu: 1
    memory: "8G"
    disks: "local-disk 100 HDD"
  }
}
