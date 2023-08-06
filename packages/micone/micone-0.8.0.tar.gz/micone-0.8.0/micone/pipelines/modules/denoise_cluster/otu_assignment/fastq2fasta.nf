// Convert fastq to fasta and merge
process fastq2fasta {
    label 'qiime1'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file("*.fasta")
    script:
        template 'denoise_cluster/otu_assignment/fastq2fasta.py'
}
