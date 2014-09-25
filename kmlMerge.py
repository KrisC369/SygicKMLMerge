__author__ = 'kristofc'
from xml.etree import ElementTree as et
import sys

class XMLCombiner(object):
    def __init__(self, filenames):
        assert len(filenames) > 0, 'No filenames!'
        et.register_namespace('', "http://earth.google.com/kml/2.0")
        # save all the roots, in order, to be processed later
        self.trees = [et.parse(f) for f in filenames]
        self.roots = [t.getroot() for t in self.trees]

    def combine(self):
        rootCoord = self.roots[0].findall(".//{http://earth.google.com/kml/2.0}coordinates")
        for r in self.trees[1:]:
            otherCoord = r.findall(".//{http://earth.google.com/kml/2.0}coordinates")
            newc = str(rootCoord[0].text) + str(otherCoord[0].text)
            filtered = "\n".join([ll.rstrip() for ll in newc.splitlines() if ll.strip()])
            rootCoord[0].text = str(filtered)
            self.trees[0].write("MergedOutput.kml")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        XMLCombiner(sys.argv[1:]).combine()
    else:
        print("Supply the files you want to merge on the commandline in the right order.")

