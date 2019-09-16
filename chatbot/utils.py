# UTILS MODULE

def convertArrayToLinesWithBreaks( arr ):
    retval = ""
    for a in arr:
        retval += a
        if not a.endswith("\n"):
            retval += "\n"
    return retval

# Loads the given file into an array, one element per line. Ignore emtpy lines and lines starting with #
def loadFileIntoArray( filenameandpath ):
    file = open( filenameandpath ,'r',errors = 'ignore')
    lines = []
    for line in file.readlines():
        if line.strip() != "" and line[0] != "#":
            lines.append(line)
    return lines