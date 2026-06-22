version 1.0

workflow SmooveSingle {
  input {
    File cram
    File ref_fasta
    File ref_fai
    File exclude_bed

    Int threads = 1
    String docker_image = "brentp/smoove"
  }

  call RunSmoove {
    input:
      cram = cram,
      ref_fasta = ref_fasta,
      ref_fai = ref_fai,
      exclude_bed = exclude_bed,
      threads = threads,
      docker_image = docker_image
  }

  output {
    File smoove_vcf = RunSmoove.vcf
    File smoove_vcf_index = RunSmoove.vcf_index
    File lumpy_command_script = RunSmoove.lumpy_cmd
  }
}

task RunSmoove {
  input {
    File cram
    File ref_fasta
    File ref_fai
    File exclude_bed
    Int threads
    String docker_image
  }

  String sample_id = basename(cram, ".cram")

  command <<<
    set -euo pipefail

    mkdir -p out

    smoove call \
      --outdir out \
      --exclude ~{exclude_bed} \
      --name ~{sample_id} \
      --fasta ~{ref_fasta} \
      -p ~{threads} \
      --genotype \
      ~{cram}

    rm -f out/*.disc.bam* out/*.split.bam* out/*.histo out/*.orig.bam*
  >>>

  output {
    File vcf = "out/~{sample_id}-smoove.genotyped.vcf.gz"
    File vcf_index = "out/~{sample_id}-smoove.genotyped.vcf.gz.csi"
    File lumpy_cmd = "out/~{sample_id}-lumpy-cmd.sh"
  }

  runtime {
    docker: docker_image
    cpu: threads
    memory: "8G"
    disks: "local-disk 100 HDD"
  }
}
