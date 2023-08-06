#! python3


class fasta:
    def __init__(self, file):
        self.file = file
        self.name = file.name
        self.seq = file.read()
