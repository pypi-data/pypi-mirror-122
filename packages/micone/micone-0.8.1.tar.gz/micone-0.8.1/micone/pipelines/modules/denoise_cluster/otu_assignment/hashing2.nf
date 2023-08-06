include { getHierarchy } from '../../../functions/functions.nf'

// Step3: Replace the ids with the hashes of the sequences
process hashing2 {
    label 'qiime1'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/hashed_output/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(unhashed_otu_table), file(unhashed_rep_seqs), file(log)
    output:
        tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/otu_assignment/hashing2.py'
}
