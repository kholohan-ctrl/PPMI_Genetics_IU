version 1.0

workflow DellyCNV {
  input {
    String sample
    File cram
    File cram_index
    File sites_bcf

    String memory = "8G"
    Int disk_gb = 100
  }

  call RunDellyCNV {
    input:
      sample = sample,
      cram = cram,
      cram_index = cram_index,
      sites_bcf = sites_bcf,
      memory = memory, 
      disk_gb = disk_gb
  }

  output {
    File delly_cnv_bcf = RunDellyCNV.bcf
    File delly_cnv_bcf_index = RunDellyCNV.bcf_index
  }
}

task RunDellyCNV {
  input {
    String sample
    File cram
    File cram_index
    File sites_bcf

    String memory
    Int disk_gb

    File ref_fasta = "gs://intermed-files-wb-strong-apple-3019/resources/Homo_sapiens_assembly38.fasta"
    File ref_fai = "gs://intermed-files-wb-strong-apple-3019/resources/Homo_sapiens_assembly38.fasta.fai"
    File blacklist = "gs://intermed-files-wb-strong-apple-3019/resources/Homo_sapiens.GRCh38.dna.primary_assembly.fa.r101.s501.blacklist.gz"
  }

  command <<<
    set -euo pipefail

    mkdir -p out

    delly cnv \
      -o out/~{sample}.delly.cnv.bcf \
      -m ~{blacklist} \
      -g ~{ref_fasta} \
      -l ~{sites_bcf} \
      ~{cram}

  >>>

  output {
    File bcf = "out/~{sample}.delly.cnv.bcf"
    File bcf_index = "out/~{sample}.delly.cnv.bcf.csi"
  }

  runtime {
    docker: "dellytools/delly:v2.1.0"
    cpu: 1
    memory: memory
    disks: "local-disk " + disk_gb + " HDD"
  }
}
