import os
import math

# variables name definition:
# G_ : global variables
# P_ : parameter varaibales
# L_ : local variables
# O_ : output variables

class Parallel:

    def __init__(self, P_file_name):
        try:
            global G_read_file
            global G_package_byte_dimension
            G_read_file = open(P_file_name, 'rb')
            G_package_byte_dimension = 128
        except:
            print("Error Parallel.Init.001 - i can't open file ", P_file_name)

    def GetReadPackage(self, P_package_number):
        #return package referred to package number received from the parameter
        G_read_file.seek(G_package_byte_dimension*P_package_number)
        O_pkg = G_read_file.read(G_package_byte_dimension)
        return O_pkg

    def FilePackageCount(self):
        #count how many packages will be create
        O_count = int(math.ceil(os.path.getsize(G_read_file.name)/G_package_byte_dimension))
        return O_count

    def TestFileExists(self, P_file_name):
        #check if file exists on path specified
        #under construction...
        return False

    # this is a test function
    def GetFileOutput(self, P_file_name):        
        L_count = self.FilePackageCount()
        i = 0
        out = []
        try:            
            while i < (L_count):
                for c in self.GetReadPackage(i):
                    out.append(c)
                i += 1
        finally:
            G_read_file.close()

        f = open(P_file_name,'wb')
        newFileByteArray = bytearray(out)
        f.write(newFileByteArray)
        f.close()
