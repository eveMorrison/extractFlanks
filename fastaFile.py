"""Parse a FASTA file."""

from pprint import pprint

fasta_file = "test.fasta"

def parse_fasta(fname):
    with open(fname, "r") as fh:

        # Create variables for storing the identifiers and the sequence.
        identifier = None
        sequence = []

        for line in fh:
            line = line.strip()  # Remove trailing newline characters.
            if line.startswith(">"):
                if identifier is None:
                    # This only happens when the first line of the
                    # FASTA file is parsed.
                    identifier = line
                else:
                    # This happens every time a new FASTA record is
                    # encountered.

                    # Start by yielding the entry that has been built up.
                    yield identifier, sequence

                    # Then reinitialise the identifier and sequence
                    # variables to build up a new record.
                    identifier = line
                    sequence = []
            else:
                # This happens every time a sequence line is encountered.
                sequence.append(line)

for entry in parse_fasta(fasta_file):
    pprint(entry)