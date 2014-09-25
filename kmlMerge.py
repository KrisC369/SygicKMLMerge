__author__ = 'kristofc'
from xml.etree import ElementTree as eT
import sys

OUTPUT_FILENAME = "MergedOutput.kml"
NAMESPACE = "http://earth.google.com/kml/2.0"


class XMLCombiner(object):
    def __init__(self, filenames):
        assert len(filenames) > 0, 'No filenames!'
        eT.register_namespace('', NAMESPACE)
        # save all the roots, in order, to be processed later
        self.trees = [eT.parse(f) for f in filenames]
        self.roots = [t.getroot() for t in self.trees]

    def combine(self):
        rootcoordinate = self.roots[0].findall(".//{http://earth.google.com/kml/2.0}coordinates")
        for r in self.trees[1:]:
            othercoordinate = r.findall(".//{http://earth.google.com/kml/2.0}coordinates")
            newcoordinate = str(rootcoordinate[0].text) + str(othercoordinate[0].text)
            filtered = "\n".join([ll.rstrip() for ll in newcoordinate.splitlines() if ll.strip()])
            rootcoordinate[0].text = str(filtered)
            self.trees[0].write(OUTPUT_FILENAME)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        XMLCombiner(sys.argv[1:]).combine()
    else:
        print("Supply the files you want to merge on the commandline in the right order.")