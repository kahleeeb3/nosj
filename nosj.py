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

    print('begin-map')
    map = map.strip() # ignore the white space at ends

    # find important places where characters exist
    begin_map_points = [match.start()+1 for match in re.finditer(re.escape("<<"), map)] #  find index in map string where map begins
    end_map_points = [match.start() for match in re.finditer(re.escape(">>"), map)] # find index in map string where map ends
    end_key_points = [match.start() for match in re.finditer(re.escape(":"), map)] # find index in map string where key value ends
    end_value_points = [match.start() for match in re.finditer(re.escape(","), map)] # find index in map string where assigned value for a key ends

    # combine and sort the lists
    event_index = sorted(begin_map_points + end_map_points + end_key_points + end_value_points) # ordered list of indexes where events occur

    # extract keys and decode values
    maps_encountered = 0 # number of maps encountered
    for key_end in end_key_points: # 1. for each ':' in the map string
        event = event_index.index(key_end) # 2. find where that event occurred in the list of events 
        curr_event = event_index[event] # 3. find the index of where the ':' is in the string
        prev_event = event_index[event-1] # 4. find the index of the previous event
        next_event = event_index[event+1] # 5. find the index of the next event
        key = map[prev_event+1:curr_event] # 6. retrieve the key
        value = map[curr_event+1:next_event] # 7. retrieve the value

        if value == '<': # 8. if the value is a map
            map_end = end_map_points[maps_encountered] # 8.1 find where the map ends
            maps_encountered+=1 # 8.2 increase the map count
            value = map[curr_event+1:map_end+2] # 8.3 select the whole map as value
            print(f'{key} -- map -- ') # print that map began
            decodeSelector(3, value) # decode the map
            # break # stop checking

        dataType = verify(value) # 9. Identify the data type
        value = decodeSelector(dataType, value) # 10. decode the value
        dataTypeStrings = ['num', 'string', 'string', 'map']
        print(f'{key} -- {dataTypeStrings[dataType]} -- {value}')

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