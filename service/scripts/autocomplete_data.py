from octopus.core import app, initialise
from octopus.modules.romeo import client
from octopus.lib import clcsv

import os, codecs
from service import models

if __name__ == "__main__":
    initialise()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="source file to import")
    args = parser.parse_args()

    source = args.source
    if not source:
        source = "romeo.csv"

    if not os.path.exists(source) and source != "romeo.csv":
        # a file has been specified that does not exist and is not the default.  Error.
        print "please specify an existing file with the -s option or leave the option blank to fetch from RoMEO"
        exit()
    elif not os.path.exists(source):
        # the romeo.csv file requested does not exist - get it from the API
        print "downloading data from RoMEO - this could take some time"
        c = client.RomeoClient()
        c.download("romeo.csv")
        print "file downloaded"

    # by this point the source exists, so we can read it in
    with codecs.open(source, "rb", "utf8") as f:
        reader = clcsv.UnicodeReader(f)
        first = True
        for row in reader:
            if first:
                first = False
                continue

            j = models.JournalAutocomplete()
            j.journal = row[0]

            issn = row[1]
            eissn = row[2]
            issns = []
            if issn is not None and issn != "":
                issns.append(issn)
            if eissn is not None and eissn != "":
                issns.append(eissn)
            j.issn = issns

            j.save()
