# SUMMARY
The nosj data format is the latest and greatest way to serialize data such that it can be shared across arbitrary channels, languages, and applications. Although formats like JSON, XML, and protocol-buffers already exist, they do not subscribe to nosj's philosophy of "No one ever needs more than three data-types!". nosj was created for the purpose of allowing even the most complex data structures to be represented in an ascii-only format useful for all known situations usage. 

A nosj object consists of a root-level map containing zero or more key-value pairs (see map data-type). One of the core design-goals of nosj is to all the unmarshalled data types to be handled by almost any languages' built-in data types and using only the languages built-in libraries for example (non-inclusive possibilities listed):

    - nosj num == float or int
    - nosj simple-string == str OR bytes
    - nosj complex-string == str OR bytes
    - nosj map == dict

# Regular Expression RegEx Searches
## Metacharacters
[Python RegEx](https://www.w3schools.com/python/python_regex.asp)
- **^** - Starts with
- **$** - Ends with
- **?** - Zero or one occurrences
- **\+**	- One or more occurrences
- **\d** - Returns a match where the string contains digits (numbers from 0-9)
- **\\** - Signals a special sequence (can also be used to escape special characters)
- **[]** - A set of characters

## Determine if a Num
A nosj num represents a numerical value between positive-infinity and negative-infinity. A marshalled num consists of the ascii-character "f", an optional ascii-dash representing a negative-sign ("-"), one or more ascii-digits ("0" through "9"), a decimal point, one or more ascii-digits ("0" through "9"), and the ascii-character "f".

```
<start> <zero or one '-'> <one or more digits> <one decimal> <one or more digits>  <end>
```

```python
pattern = "f-?\d+\.\d+f$"
```

## Determine if Simple String
In the simple representation, the string is restricted to a set of commonly-used ascii characters which (according to our extensive market survey) are the most-liked among humans (i.e. all ascii letters and numbers, spaces (" ", 0x20), and tabs ("\t", 0x09)). Simple-strings are followed by a trailing "s" which is NOT part of the data being encoded.

```
<start> <one or more letters, space, or tab> <one letter s> <end>
```

```python
pattern = "^[a-zA-Z0-9 \t]+s$"
```

## Determine if a Map
A nosj map is a sequence of zero or more key-value pairs that take the form of `<key-1:value-1,key-2:value-2,...>` similar to the conceptual hash-map data structure. A nosj map MUST start with a two left angle-bracket ("<<") and end with two right angle-bracket (">>") and map keys MUST be an ascii-string consisting of one or more lowercase letters ("a" through "z") only. Map values may be any of the three canonical nosj data-types (map, string or num) and there is no specification-bound on how many maps may be nested within each other. Though map values are not required to be unique, map keys MUST be unique within the current map (though they may be duplicated in maps at other levels of "nesting").

```
<start> <zero or more spaces> <two left carets> <one or more lowercase letters> <a single ':'> <zero or more values of any kind> <two right carets> <zero or more spaces> <end>
```

```python
pattern = "^ *<<[a-z]:.*>> *$"
```