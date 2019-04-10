# distutils: language=c++
# cython: language_level=3
from libcpp.string cimport string
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.unordered_map cimport unordered_map
from libcpp.utility cimport pair

ctypedef unsigned short int matrix
ctypedef unsigned short int value

cdef extern from "include/transitMatrix.h" namespace "lmnoel" :

    cdef cppclass transitMatrix[string,string]:

        transitMatrix(bool, bool, unsigned int, unsigned int) except +
        transitMatrix() except +

        void prepareGraphWithVertices(int V) except +
        void addToUserSourceDataContainer(unsigned int, string, unsigned short int) except +
        void addToUserDestDataContainer(unsigned int, string, unsigned short int) except +
        void addEdgeToGraph(int, int, int, bool) except +
        void addToCategoryMap(string, string) except +

        void compute(int) except +
        vector[pair[string, value]] getValuesByDest(string, bool) except +
        vector[pair[string, value]] getValuesBySource(string, bool) except +
        unordered_map[string, vector[string]] getDestsInRange(unsigned int, unsigned int) except +
        unordered_map[string, vector[string]] getSourcesInRange(unsigned int, unsigned int) except +
        unsigned short int timeToNearestDestPerCategory(string, string) except +
        unsigned short int countDestsInRangePerCategory(string, string, unsigned short int) except +
        unsigned short int timeToNearestDest(string) except +
        unsigned short int countDestsInRange(string, unsigned short int) except +

        void writeCSV(string) except +
        void writeTMX(string) except +
        void readTMX(string) except +
        void printDataFrame() except +



cdef class pyTransitMatrix:
    cdef transitMatrix *thisptr

    def __cinit__(self, bool isCompressible=False, bool isSymmetric=False, unsigned int rows=0, unsigned int columns=0):
        if rows == 0 and columns == 0:
            self.thisptr = new transitMatrix()
        else:
            self.thisptr = new transitMatrix(isCompressible, isSymmetric, rows, columns)


    def __dealloc__(self):
        if self.thisptr is not NULL:
            del self.thisptr
            self.thisptr = NULL

    def prepareGraphWithVertices(self, vertices):
        self.thisptr.prepareGraphWithVertices(vertices)

    def getDestsInRange(self, range_, numThreads):
        cdef unordered_map[string, vector[string]] py_res = self.thisptr.getDestsInRange(range_, numThreads)
        rv = {}
        for key, value in py_res:
            rv_key = []
            for element in value:
                rv_key.append(element.decode())
            rv[key.decode()] = rv_key
        return rv


    def getSourcesInRange(self, range_, numThreads):
        cdef unordered_map[string, vector[string]] py_res = self.thisptr.getSourcesInRange(range_, numThreads)
        rv = {}
        for key, value in py_res:
            rv_key = []
            for element in value:
                rv_key.append(element.decode())
            rv[key.decode()] = rv_key
        return rv

    def getValuesBySource(self, source_id, sort):
        cdef string source_id_string = str.encode(source_id)
        cdef vector[pair[string, value]] cpp_result = self.thisptr.getValuesBySource(source_id_string, sort)
        rv = []
        for a, b in cpp_result:
            rv.append((a.decode(), b))
        return rv

    def getValuesByDest(self, dest_id, sort):
        cdef string dest_id_string = str.encode(dest_id)
        cdef vector[pair[string, value]] cpp_result = self.thisptr.getValuesByDest(dest_id_string, sort)
        rv = []
        for a, b in cpp_result:
            rv.append((a.decode(), b))
        return rv

    def addToUserSourceDataContainer(self, networkNodeId, source_id, lastMileDistance):
        cdef string source_id_string = str.encode(source_id)
        self.thisptr.addToUserSourceDataContainer(networkNodeId, source_id_string, lastMileDistance)

    def addToUserDestDataContainer(self, networkNodeId, dest_id, lastMileDistance):
        cdef string dest_id_string = str.encode(dest_id)
        self.thisptr.addToUserDestDataContainer(networkNodeId, dest_id_string, lastMileDistance)


    def addEdgeToGraph(self, src, dst, weight, isBidirectional):
        self.thisptr.addEdgeToGraph(src, dst, weight, isBidirectional)

    def compute(self, numThreads):
        self.thisptr.compute(numThreads)

    def writeCSV(self, outfile):
        cdef string outfile_string = str.encode(outfile)
        return self.thisptr.writeCSV(outfile_string)

    def writeTMX(self, outfile):
        cdef string outfile_string = str.encode(outfile)
        self.thisptr.writeTMX(outfile_string)

    def readTMX(self, infile):
        cdef string infile_string = str.encode(infile)
        self.thisptr.readTMX(infile_string)

    def printDataFrame(self):
        self.thisptr.printDataFrame()

    def addToCategoryMap(self, dest_id, category):
        cdef string string_dest_id = str.encode(dest_id)
        cdef string string_category = str.encode(category)
        self.thisptr.addToCategoryMap(string_dest_id, string_category)

    def timeToNearestDestPerCategory(self, source_id, category):
        cdef string string_source_id = str.encode(source_id)
        cdef string string_category = str.encode(category)
        return self.thisptr.timeToNearestDestPerCategory(string_source_id, string_category)

    def countDestsInRangePerCategory(self, source_id, category, range):
        cdef string string_source_id = str.encode(source_id)
        cdef string string_category = str.encode(category)
        return self.thisptr.countDestsInRangePerCategory(string_source_id, string_category, range)

    def timeToNearestDest(self, source_id):
        cdef string string_source_id = str.encode(source_id)
        return self.thisptr.timeToNearestDest(string_source_id)

    def countDestsInRange(self, source_id, range):
        cdef string string_source_id = str.encode(source_id)
        return self.thisptr.countDestsInRange(string_source_id, range)
