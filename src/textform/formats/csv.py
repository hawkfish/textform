import csv

Reader = csv.DictReader

class Writer(csv.DictWriter):

    def __init__(self, outfile, fieldnames, **config):
        super().__init__(outfile, fieldnames, lineterminator="\n")

    def writefooter(self):
        pass

Nester = Writer
Unnester = Reader
