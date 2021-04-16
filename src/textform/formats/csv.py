import csv

Reader = csv.reader
DictReader = csv.DictReader

class Writer(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = csv.writer(outfile, lineterminator="")

    def writerow(self, values):
        self.writer.writerow(values)

class DictWriter(csv.DictWriter):

    def __init__(self, outfile, fieldnames, **config):
        super().__init__(outfile, fieldnames, lineterminator="\n")

    def writefooter(self):
        pass
