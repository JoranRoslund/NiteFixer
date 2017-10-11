#!/usr/bin/python

import os
import re

user = os.environ['USER']

def convertFile1(filename):
    with open(filename) as theFile:
        outfile = open('tmpfile2', 'w')
        content = theFile.readlines()
        processing = False

        # Patterns for finding stuff
        getCellWrapperPattern = re.compile("cell = self.__getCellWrapperOb")
        endPattern = re.compile("cellList.append")

        for line in content:
            outline = line
            
            match = getCellWrapperPattern.search(line)
            end = endPattern.search(line)
            if match:
                outfile.write(outline)
                # Insert extra check
                outline = "                    if cell is not None:\n"
                processing = True
            elif processing:
                # Indent subsequent lines
                outline = "    " + outline
                if end:
                    processing = False

            outfile.write(outline)


def convertFile2(filename):
    with open(filename) as theFile:
        outfile = open('tmpfile', 'w')
        content = theFile.readlines()
        defined = False

        # Patterns for finding stuff
        getSectorPattern = re.compile("API_getSector\(int\((\w+)\[1\]\)\)")
        definePositionPattern = re.compile("def AL_INT_cellFactory")

        for line in content:
            outline = line
            
            match = getSectorPattern.search(line)
            define = definePositionPattern.search(line)
            if match:

                # Wrap variable name in function call
                scVariableName = match.group(1)
                outline = line.replace("int(" + scVariableName + "[1])", "self.__getSectorNumberFromSC(" + scVariableName + ")")

            elif define and not defined:
                # Inject function definition before it's used
                outfile.write("    def __getSectorNumberFromSC(self, sc):\n")
                outfile.write("        if sc[2].isdigit():\n")
                outfile.write("            return int(sc[1:3])\n")
                outfile.write("        else:\n");
                outfile.write("            return int(sc[1])\n\n")
                defined = True
                
            outfile.write(outline)


convertFile1("/workspace/git/" + user + "/wrat/build/MJE_LMC/python_lib/iov/rbs/NITE/Rbs/rbs_db.py")
convertFile2("/workspace/git/" + user + "/wrat/build/MJE_LMC/python_lib/iov/rbs/NITE/Nbap/AL_RNC.py")

"""
For some reason, copying from inside python doesn't work. The files
become truncated. Copy the files manually to their right places:

cp tmpfile /workspace/git/$USER/wrat/build/MJE_LMC/python_lib/iov/rbs/NITE/Nbap/AL_RNC.py
cp tmpfile2 /workspace/git/$USER/wrat/build/MJE_LMC/python_lib/iov/rbs/NITE/Rbs/rbs_db.py
"""
