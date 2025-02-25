

# this translates the names as they appear in the downloaded fasta to cleaner names
# and it also associates contigs from the same organism to the same name
otus_clean_names = {
    'BS.pilon.polished.v3.ST170922' : 'bsubtilis',
    'Escherichia_coli_plasmid' : 'ecoli',
    'Escherichia_coli_chromosome' : 'ecoli',
    'Listeria_monocytogenes_complete_genome' : 'lmonocytogenes',
    'Pseudomonas_aeruginosa_complete_genome' : 'paeruginosa',
}

# this is a dict that just contains the chromosomes, no plasmids
# used for mapping against
otus_no_plasmids = {k: v for k, v in otus_clean_names.items() if 'plasmid' not in k}


# genome sizes used to calculate mean coverage
genome_sizes = {
    'bsubtilis': 4045709,
    'ecoli': 4765464,
    'lmonocytogenes': 2992383,
    'paeruginosa': 6792371,
}


