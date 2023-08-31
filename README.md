# SUMMARY
The nosj data format is the latest and greatest way to serialize data such that it can be shared across arbitrary channels, languages, and applications. Although formats like JSON, XML, and protocol-buffers already exist, they do not subscribe to nosj's philosophy of "No one ever needs more than three data-types!". nosj was created for the purpose of allowing even the most complex data structures to be represented in an ascii-only format useful for all known situations usage. 

A nosj object consists of a root-level map containing zero or more key-value pairs (see map data-type). One of the core design-goals of nosj is to all the unmarshalled data types to be handled by almost any languages' built-in data types and using only the languages built-in libraries for example (non-inclusive possibilities listed):

    - nosj num == float or int
    - nosj simple-string == str OR bytes
    - nosj complex-string == str OR bytes
    - nosj map == dict