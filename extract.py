"""Parse a FASTA file."""

from pprint import pprint
import re

fasta_file = "test.fasta"
repMask_file = "test.fa.out"

def parse_fasta(fname):
    with open(fname, "r") as fh:

        # Create variables for storing the identifiers and the sequence.
        identifier = None
        sequence = []

        for line in fh:
            line = line.strip()  # Remove trailing newline characters.
            if line.startswith(">"):
                # Then reinitialise the identifier and sequence
                # variables to build up a new record.
                identifier = line
                sequence = [] 
            else:
                # This happens every time a sequence line is encountered.
                sequence.append(line)
                # Start by yielding the entry that has been built up.
                yield identifier, sequence        


def find_fa_seq(fname,leftFlank,rightFlank):
    with open(fname, "r") as fh:

        # Create variables for storing the identifiers and the sequence.
        identifier = None
        sequence = []
        left_flank_begin = '\0'
        right_flank_end = '\0'

        for line in fh:
            line = line.strip()  # Remove trailing newline characters.
            if line.startswith(">"):
                # Then reinitialise the identifier and sequence
                # variables to build up a new record.
                identifier = line
                num = re.search('^.+[|(](\d+)[.]+(\d+)',identifier,0)
                left_flank_begin = int(num.group(1))
                right_flank_end = int(num.group(2))
                sequence = [] 
            else:
                # This happens every time a sequence line is encountered.
                sequence.append(line)
                if(left_flank_begin < leftFlank and right_flank_end > rightFlank):
                    # Start by yielding the entry that has been built up.
                    yield identifier, sequence

def parse_repMask(fname):
    with open(fname, "r") as fh:

        for line in fh:
            line = line.strip()
            if re.search('^.+\d',line,0):
                values = line.split()
                id = values[14]
                te_start = values[5]
                te_end = values[6]
                yield id, te_start, te_end

for entry in parse_fasta(fasta_file):
    #pprint(entry)
    num = re.search('^.+[|(](\d+)[.]+(\d+)',entry[0],0)
    left_flank_begin = int(num.group(1))
    right_flank_end = int(num.group(2))
    #pprint(left_flank_begin)
    #pprint(right_flank_end)


for entry in parse_repMask(repMask_file):
    te_id = entry[0]
    left_flank_end = int(entry[1])
    right_flank_begin = int(entry[2])
    #print("ID: " + te_id)
    #print("Left flank end: " + left_flank_end)
    #print("Right flank start: " + right_flank_begin)
    for coordinate in find_fa_seq(fasta_file,left_flank_end,right_flank_begin):
        num = re.search('^.+[|(](\d+)[.]+(\d+)',coordinate[0],0)
        left_flank_begin = int(num.group(1))
        right_flank_end = int(num.group(2))

        #find where transposon sits in sequence
        te_start = left_flank_end - left_flank_begin
        te_length = right_flank_begin - left_flank_end
        te_end = te_start + te_length

        #find flank lengths
        left_flank_length = left_flank_end - left_flank_begin
        right_flank_length = right_flank_end - right_flank_begin

        #pprint(coordinate)

        #extract the flanking sequences
        transposon = coordinate[1][0][te_start : te_end+1]
        f = open("transposon.fasta", "a")
        f.write(">" + te_id + "\n")
        f.write(transposon + "\n")
        f.close()
        flankLeft = coordinate[1][0][ : te_start]
        f = open("leftFlanks.fasta", "a")
        f.write(">" + te_id + "\n")
        f.write(flankLeft + "\n")
        f.close()
        flankRight = coordinate[1][0][te_end+1: ]
        f = open("rightFlanks.fasta", "a")
        f.write(">" + te_id + "\n")
        f.write(flankRight + "\n")
        f.close()

        