import sys
from readfq import readfq

'''
find which reads were rejected by relying on the fact that all rejected reads in simulations are exactly mu-sized
This script does not work on data from a live sequencing run, because rejected reads will not all have the same length
'''



def process_fq(fq: str, mu: int) -> str:
    '''
    Process a fastq file: get the total number of reads, the number of unblocked reads, and their ratio
    :param fq: path to fastq file
    :param mu: size of rejected reads in the simulation
    :return: resulting string with metadata and counts
    '''
    # get metadata from the filename
    meta = fq.split("/")[-1].split(".")[0].split('_')
    cond, time, otu = meta[0], meta[1], meta[2]
    total = 0
    unb = 0
    # open the fq file
    fh = open(fq, 'rt')
    # loop over all reads in the fastq file
    for desc, name, seq, qual in readfq(fh):
        total += 1
        if len(seq) == mu:
            unb += 1
    fh.close()
    # calculate the ratio of unblocked reads
    try:
        unb_ratio = unb / total
    except ZeroDivisionError:
        unb_ratio = 0
    # format the results
    output = f'{cond},{time},{otu},{total},{unb},{unb_ratio}'
    return output




if __name__ == "__main__":
    data = process_fq(fq=sys.argv[1], mu=int(sys.argv[2]))
    print(data)






