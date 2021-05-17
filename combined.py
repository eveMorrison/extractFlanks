"""Parse a FASTA file."""

from pprint import pprint
import re

fasta_file = "test.fasta"

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


for entry in parse_fasta(fasta_file):
    #pprint(entry)
    num = re.search('^.+[|(](\d+)[.]+(\d+)',entry[0],0)
    flankBegin = int(num.group(1))
    flankEnd = int(num.group(2))
    pprint(flankBegin)
    pprint(flankEnd)