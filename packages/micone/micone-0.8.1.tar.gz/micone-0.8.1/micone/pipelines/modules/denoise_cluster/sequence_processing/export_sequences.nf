include { getHierarchy } from '../../../functions/functions.nf'

// Export the sequences and fix the manifest file
process export_sequences {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/demultiplexed_sequences/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(demux_artifact)
    output:
        tuple val(meta), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/sequence_processing/export_sequences.py'
}
