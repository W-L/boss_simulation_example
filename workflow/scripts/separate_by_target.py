import sys
from os import path
PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(PARENT_DIR)

import numpy as np

from config.otu_info import otus_clean_names   # noqa
from readfq import readfq


"""
this script is used to separate a fq file into multiple fqs given the mappings in a paf or sam file 
- input: fq & paf/sam
- output: multiple fqs
"""


def parse_aln(aln_path: str, target_dict: dict) -> dict:
    '''
    parse the paf or sam file and return a dictionary with read ids and their target organism
    :param aln_path: path to alignment file
    :param target_dict: dictionary with target reference sequences
    :return: dict of read ids and their target sequences
    '''
    # open the paf and record the source for each mapped read
    read_targets = {}
    rid_aln_scores = {}

    ext = aln_path.split('.')[-1]
    if ext == "paf":
        tpos = 5
    elif ext == "sam":
        tpos = 2
    else:
        print("unknown extension, exit")
        sys.exit()

    with open(aln_path, 'r') as aln:
        for line in aln:
            if line.startswith('@'):
                continue
            ll = line.split('\t')
            rid = ll[0]
            target = ll[tpos]
            aln_score = int(ll[14].split(':')[-1])
            # if the rid is not recorded yet, just add it
            if rid not in read_targets.keys():
                read_targets[rid] = target_dict[target]
                rid_aln_scores[rid] = aln_score
            else:
                # if the rid is already recorded, check whether this one has higher aln score
                # and only overwrite if its higher
                if aln_score > rid_aln_scores[rid]:
                    read_targets[rid] = target_dict[target]
    return read_targets


def write_target_reads(read_targets: dict, fq: str, target_dict: dict) -> None:
    '''
    open a fq file and write reads to individual files based on the target
    :param read_targets: dict of targets for each read
    :param fq: file with the read data
    :param target_dict: dict of names for output files
    :return: None
    '''
    # open a fq file for each target
    targets = np.unique(list(target_dict.values()))

    fq_base = fq.split('/')[-1].split('.')[0]

    # open a file for each target
    target_files = dict()
    for t in targets:
        target_files[t] = open(f'{fq_base}_{t}.fq', 'w')

    # iterate over file and write the fq into the correct file
    with open(fq, 'r') as fastq:
        for desc, name, seq, qual in readfq(fastq):
            # check which target the read comes from
            try:
                t = read_targets[name]
            except KeyError:
                continue

            # write to file
            if not qual:
                qual = 'z' * len(seq)
            target_files[t].write(f'@{desc}\n{seq}\n+\n{qual}\n')

    # close all files
    for tf in target_files.values():
        tf.close()



if __name__ == "__main__":
    # load a dictionary with targets and read ids
    read_targets = parse_aln(aln_path=sys.argv[1], target_dict=otus_clean_names)
    # open the fastq, iterate through it and write reads to individual files
    write_target_reads(read_targets=read_targets, fq=sys.argv[2], target_dict=otus_clean_names)


