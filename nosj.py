import sys # for standard error outputs
import re # find recurring strings

def verifyInput(marshalled):
    """
    Checks for valid marshmellow format of nosj input. If invalid input, 
    changes the global value of 'errMsg' and returns -1. If valid input,
    return 1 for num, 2 for simple-string, 3 for complex string, 4 for map.
    """

    # Check for num
    if(marshalled[:1] == 'f' and marshalled[-1:] == 'f'):
        return 1 # this is a num
    
    # check for simple-string
    elif(marshalled[-1:] == 's'):
        return 2
    
    # check for complex-string
    elif('%' in marshalled):
        return 3
   
    # Check for a map
    elif(marshalled.strip()[:2] == '<<' and marshalled.strip()[-2:] == '>>'):
        # If there is a space in the map, it should be invalid
        if ' ' in marshalled.strip():
            errMsg = "A properly formatted nosj map contains NO WHITESPACE characters"
            print(f"ERROR -- {errMsg}", file=sys.stderr)
            sys.exit(66)
        else:
            return 4 # this is a map
        
    # not a valid format, send error
    else:
        errMsg = "This is not a valid nosj input"
        print(f"ERROR -- {errMsg}", file=sys.stderr)
        sys.exit(66)

def decodeMap(map):

    map = map.strip() # ignore the white space

    # find important places where characters exist
    map_start_index = [match.start()+1 for match in re.finditer(re.escape("<<"), map)] # find map and submap start point
    map_end_index = [match.start() for match in re.finditer(re.escape(">>"), map)] # find map and submap end points
    key_end_index = [match.start() for match in re.finditer(re.escape(":"), map)] # find map and submap end points
    value_end_index = [match.start() for match in re.finditer(re.escape(","), map)] # find map and submap end points
    # print(map_start_index, map_end_index, key_end_index, value_end_index)

    # combine and sort the lists
    event_index = sorted(map_start_index + map_end_index + key_end_index + value_end_index)
    # print(event_index)

    # convert to a python dictionary
    map_dict = {} # where to store the dictionary
    map_count = 0 # number of maps encountered
    for key_end in key_end_index: # 1. for each ':' in map string
        event = event_index.index(key_end) # 2. find where that event occurred in the list of events 
        curr_event = event_index[event] # 3. find the index of where the ':' is in the string
        prev_event = event_index[event-1] # 4. find the index of the previous event
        next_event = event_index[event+1] # 5. find the index of the next event
        key = map[prev_event+1:curr_event] # 6. retrieve the key
        value = map[curr_event+1:next_event] # 7. retrieve the value

        if value == '<': # 8. if the value is a map
            map_end = map_end_index[map_count] # 8.1 find where the map ends
            map_count+=1 # 8.2 increase the map count
            value = map[curr_event+1:map_end+2] # 8.3 select the whole map as value

        dataType = verifyInput(value) # 9. Identify the data type
        value = decodeSelector(dataType, value) # 10. decode the value

        
        map_dict[key] = value # 11. store the decoded value

    return map_dict # 12. Return The dict

def decodeNum(num):
    num = num[1:-1] # remove the f at beginning and end
    return float(num)

def decodeSimpleString(sstring):
    sstring = sstring[:-1]
    return sstring

def decodeSelector(dataType, value):
    if dataType == 1: # if its a num
        value = decodeNum(value)
    if dataType == 2:
        value = decodeSimpleString(value)
    if dataType == 4: # if its a map
        value = decodeMap(value) # decode the map

    return value

def main():

    # Check the input is of valid length
    if(len(sys.argv)!=2):
        errMsg = "You must pass a single valid Marshalled nosj formatted argument"
        print(f"ERROR -- {errMsg}", file=sys.stderr)
        sys.exit(66)

    marshalled = sys.argv[1] # get the marshalled value from the input
    dataType = verifyInput(marshalled) # verify the input is correct
    unmarshalled = decodeSelector(dataType, marshalled) # decode the string
    print(unmarshalled)

if __name__=="__main__":
    main()