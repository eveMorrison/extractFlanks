"""Parse a FASTA file."""

from pprint import pprint
import re

fasta_file = "test.fasta"
repMask_file = "test.fa.out"


#find the corresponding fasta sequence to the repeatmasker output
#One code to find them all is not sorted
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
                #corresponding found transposon will be within one code to find them all positions
                if(left_flank_begin <= leftFlank and right_flank_end >= rightFlank):
                    # Start by yielding the entry that has been built up.
                    yield identifier, sequence


#find every line containing transposon information
def parse_repMask(fname):
    with open(fname, "r") as fh:

        for line in fh:
            line = line.strip()
            #lines begin with smith-waterman score
            #look to see if the line begins with a number
            #if line begins with number find the Repeat Masker ID number and transposon locations
            if re.search('^.+\d',line,0):
                values = line.split()
                id = values[14]
                te_start = values[5]
                te_end = values[6]
                te = values[9]
                query_seq = values[4]

                #return the Repeat Masker ID, transposon start position and transposon end position
                yield id, te_start, te_end, te, query_seq

#open the repeat masker file 
#for every found transposon
#then search for corresponding One Code to Find Them All fasta sequence
#finally print the found sequences for the trasnposon and the flanks to their corresponding files
for entry in parse_repMask(repMask_file):
    te_id = entry[0]
    te = entry[3]
    query_sequence = entry[4]
    left_flank_end = int(entry[1])
    right_flank_begin = int(entry[2])

    #find the corresponding One Code to Find Them All sequence
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


        #extract the flanking sequences

        #append transposon to TE fasta file
        transposon = coordinate[1][0][te_start : te_end+1]
        f = open("transposon.fasta", "a")
        f.write(">" + te_id + "|" + query_sequence + "|" + te + "\n")
        f.write(transposon + "\n")
        f.close()

        #append flanking sequence to left flank fasta file
        #get sequence from beginning of string to beginning of transposon
        flankLeft = coordinate[1][0][ : te_start]
        f = open("leftFlanks.fasta", "a")
        f.write(">" + te_id + "|" + query_sequence + "|" + te + "\n")
        f.write(flankLeft + "\n")
        f.close()

        #append flanking sequence to right flank fasta file
        #get sequence from beginning of transposon to end of the string
        flankRight = coordinate[1][0][te_end+1: ]
        f = open("rightFlanks.fasta", "a")
        f.write(">" + te_id + "|" + query_sequence + "|" + te + "\n")
        f.write(flankRight + "\n")
        f.close()

        