#!/usr/bin/python3

import sys # for standard error outputs
import re # find recurring strings, and regex
import urllib.parse # parse percent encoded data

def err(errMsg):
    """
    Prints error code to screen and then exits with code 66
    """
    print(f"ERROR -- {errMsg}", file=sys.stderr)
    sys.exit(66)

def verify(input):
    """
    Checks for valid format of nosj input. If invalid input, exit program with error 66. 
    If valid input, return 0 for num, 1 for simple-string, 2 for complex string, 3 for map.
    """
    # https://www.w3schools.com/python/python_regex.asp
    # complex strings: https://rgxdb.com/r/48L3HPJP
    # non-capturing group: (?:<some group>)? --> doesnt capture

    # Check for num
    pattern = "^f-?\d+\.\d+f$"
    if re.match(pattern, input):
        return 0

    # check for simple string
    pattern = "^[a-zA-Z0-9 \t]+s$"
    if re.match(pattern, input):
        return 1

    # check for map
    pattern = "^ *<<(?:[a-z]:.*)?>> *$"
    if re.match(pattern, input):
        begin_map_points = [match.start() for match in re.finditer(re.escape("<<"), input)]
        end_map_points = [match.start() for match in re.finditer(re.escape(">>"), input)]
        if(len(begin_map_points) == len(end_map_points)): # if begin_map == end_map
            return 3
    
    # check for a complex string
    pattern = "^(?:[^%]|%[0-9A-Fa-f]{2})+$"
    if '%' in input and re.match(pattern, input):
        return 2

    err("Not a valid nosj data type")

def decodeNum(num):
    num = num[1:-1] # remove the f at beginning and end
    num = float(num)
    if num.is_integer():
        return int(num)
    else:
        return num

def decodeSimpleString(sstring):
    sstring = sstring[:-1]
    return sstring

def decodeComplexString(cstring):
    return urllib.parse.unquote(cstring)

def decodeSelector(dataType, value):
    """
    Chooses which decoder to use given the datatype
    """
    if dataType == 0: # if its a numchmod +x myscript.py
        value = decodeNum(value)
    if dataType == 1:
        value = decodeSimpleString(value)
    if dataType == 2:
        value = decodeComplexString(value)
    if dataType == 3: # if its a map
        value = decodeMap(value) # decode the map

    return value

def decodeMap(map):
    """
    Decodes a map data type by finding instances where keys take place,
    storing the key, and decoding the value based on its type. If the type
    is found to be invalid, exit with error 66.
    """

    map = map.strip() # ignore the white space at ends

    # find important places where characters exist
    begin_map_points = [match.start() for match in re.finditer(re.escape("<<"), map)] #  find index in map string where map begins
    end_map_points = [match.start() for match in re.finditer(re.escape(">>"), map)] # find index in map string where map ends
    end_key_points = [match.start() for match in re.finditer(re.escape(":"), map)] # find index in map string where key value ends
    end_value_points = [match.start() for match in re.finditer(re.escape(","), map)] # find index in map string where assigned value for a key ends

    i = 0
    print('begin-map')
    while(i < len(map)):
        
        
        # if we found an ':' char
        if i in end_key_points:
            
            # 1. FIND THE KEY BY SCANNING LEFT
            key = map[i-1] # store the key

            # 2. FIND THE VALUE BY SCANNING RIGHT
            j = i+1 # index of right scan
            value = "" # set value to nothing
            num_submaps = 0 # number of submaps found
            while(j < len(map)): # while stuff left to scan

                # 2.1 IF A SUBMAP
                if j in begin_map_points:
                    num_submaps += 1 # increase num submaps
                    while(num_submaps > 0): # while in submap
                        value += map[j] # store the value
                        j+=1 # step right
                        if j in begin_map_points:
                            num_submaps += 1
                        if j in end_map_points:
                            num_submaps -= 1
                    value += map[j:j+2]
                    j+=2 # move to end of submap
                    
                # 2.2 IF NOT A SUBMAP
                else:
                    if (j in end_value_points) or (j in end_map_points):
                        break
                    else:
                        value += map[j]
                        j += 1

            
            # 3. DONE SEARCHING FOR VALUE
            i = j # MOVE i to END OF SCAN POINT j
            dataTypeStrings = ['num', 'string', 'string', 'map']
            dataType = verify(value) # determine datatype of value
            if dataType == 3:
                print(f'{key} -- {dataTypeStrings[dataType]} -- ')
                decodeMap(value)
            else:
                value = decodeSelector(dataType, value) # store the decoded value
                print(f'{key} -- {dataTypeStrings[dataType]} -- {value}')
        i+=1
    
    print('end-map')

def main():

    # Check the input is of valid length
    if(len(sys.argv)!=2):
        errMsg = "You must pass a file name as an argument `./nosj.py <filename>`"
        print(f"ERROR -- {errMsg}", file=sys.stderr)
        sys.exit(66)

    # read the provided file
    filename = sys.argv[1] # get the filename from command arguments
    with open(filename, 'r') as file: # open the file with read
        contents = file.read() # store the file content
    contents = contents.replace('\n', '') # remove any new tab characters

    # decode
    # contents = sys.argv[1]
    dataType = verify(contents)
    if dataType != 3: err("input must be a map.")
    decodeMap(contents)

if __name__=="__main__":
    main()