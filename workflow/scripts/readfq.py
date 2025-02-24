


def readfq(fp):
    """
    GENERATOR FUNCTION
    Read a fastq file and return the sequence
    Parameters
    ----------
    fp: _io.IO
        File handle for the fastq file.

    Yields
    -------
    desc: str
        The fastq read header
    name: str
        The read ID
    seq: str
        The sequence

    """
    last = None  # this is a buffer keeping the last unprocessed line
    while True:  # mimic closure; is it a bad idea?
        if not last:  # the first record or a record following a fastq
            for ll in fp:  # search for the start of the next record
                if ll[0] in ">@":  # fasta/q header line
                    last = ll[:-1]  # save this line
                    break
        if not last:
            break
        desc, name, seqs, last = last[1:], last[1:].partition(" ")[0], [], None
        for ll in fp:  # read the sequence
            if ll[0] in "@+>":
                last = ll[:-1]
                break
            seqs.append(ll[:-1])
        if not last or last[0] != "+":  # this is a fasta record
            yield desc, name, "".join(seqs), None  # yield a fasta record
            if not last:
                break
        else:  # this is a fastq record
            seq, leng, seqs = "".join(seqs), 0, []
            for ll in fp:  # read the quality
                seqs.append(ll[:-1])
                leng += len(ll) - 1
                if leng >= len(seq):  # have read enough quality
                    last = None
                    yield desc, name, seq, "".join(seqs)  # yield a fastq record
                    break
            if last:  # reach EOF before reading enough quality
                yield desc, name, seq, None  # yield a fasta record instead
                break

