from portality.core import app

import csv
from service import models

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="source file to import")
    args = parser.parse_args()

    if not args.source:
        print "Please specify a csv with the -s option"
        exit()

    f = open(args.source, "r")
    reader = csv.reader(f)

    for row in reader:
        j = models.JournalAutocomplete()
        j.issn = row[0]
        j.journal = row[1]
        j.save()
