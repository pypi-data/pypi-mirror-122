// Import the sequences to qiime2 artifacts
process import_sequences {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file('*_sequences.qza')
    script:
        template 'denoise_cluster/sequence_processing/import_sequences.py'
}

