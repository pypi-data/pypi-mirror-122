include { import_sequences } from './import_sequences_sh.nf'
include { demultiplexing_illumina } from './demultiplexing_illumina.nf'
include { export_sequences } from './export_sequences.nf'


workflow demultiplexing_illumina_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
        input_channel
    main:
        input_channel \
            | import_sequences \
            | demultiplexing_illumina \
            // | join_reads \
            | export_sequences
    emit:
        // export_sequences and join_reads has publishDir
        // tuple val(meta), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST')
        export_sequences.out
}
