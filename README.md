# python2-python3

Normalize functions across Python 2 and Python 3

## Notes on compatibility

### Common issues
All print statements must use parentheses i.e. print ("")  
The dictionary has_key() method does not exist in Python 3. Use 'key in dict' instead.  
The dictionary methods iterkeys(), itervalues() and iteritems() are deprecated and replaced with keys(), values() and items() respectively.  
The range() method is an iterator in Python 3. When accessing as an array it must be converted to a list i.e. myarray = list(range(n))  
"base64" is no longer a valid text encoding in Python 3 e.g. mystring.encode("base64"); use base64.b64encode(mystring) instead  
hashlib methods require unicode strings to be encoded before input i.e. hashlib.sha256(mystring.encode("latin_1"))  
Integer division results in floats in Python 3.  Use the // operator to ensure an integer result.  

See here for comprehensive list of differences: https://python-future.org/index.html  

### Source encoding
Python 2 interprets source files with ascii encoding. This can be modified with the '# coding:' directive  
Python 3 interprets source files with UTF-8 encoding  

Source encoding dictates the allowed contents of string literals. Ascii encoding allows 7-bit ascii characters only. UTF-8 allows all unicode characters.  

### File I/O
The builtin open() method returns a file object which is used for file I/O.  This behaves as follows depending on the file mode specified;  

Python 2:  
open(<filename>, "r").read()    returns single-byte string (with newline conversion)  
open(<filename>, "rb").read()   returns single-byte string  
open(<filename>, "w").write()   writes single-byte string (with newline conversion)  
open(<filename>, "wb").write()  writes single-byte string  

Python3:  
open(<filename>, "r").read()    returns unicode string (with newline conversion); file text is encoded to unicode automatically  
open(<filename>, "rb").read()   returns bytes() object  
open(<filename>, "w").write()   encodes unicode strings to CP-1252 encoding and writes to file (with newline conversion)  
open(<filename>, "wb").write()  encodes unicode strings to CP-1252 encoding and writes to file  

Therefore Python 3 will automatically handle decoding strings to unicode on a read, and encoding from unicode on a write. Where only latin_1 characters
are being used in strings there should be no compatibility issues with file I/O.

### Network I/O
Python 2 implements network I/O via the urllib2 module  
Python 3 implements network I/O via the urllib.request module  

These are different enough that its best to implement network I/O with a wrapper class that chooses the module and methods to use based on the current
python version.

For simple I/O, where there is no exception handling needed, the following can be used to make the modules appear the same;

```
try:
    import urllib2                      # Python 2
except:
    import urllib.request as urllib2    # Python 3
```

### Python 2 String and Byte Types
str - sequence of single-byte characters  
unicode - sequence of unicode characters  
bytearray - mutable sequence of bytes  
bytes() - alias for str()

### Python 2 Encoding/Casting
unicode.encode(encoding) - to single-byte string with specified encoding  
unicode.decode(encoding) - noop; equivalent to unicode.encode("ascii").decode(encoding);  input unicode string must be encodable to 7-bit ascii  
str.encode(encoding) - noop; equivalent to str.decode("ascii").encode(encoding);  input string must be 7-bit ascii  
str.decode(encoding) - to unicode from specified encoding  
bytearray.encode() - n/a  
bytearray.decode(encoding) - equivalent to str(bytearray).decode(encoding)  
str(unicode) - same as unicode.encode("ascii")  
str(bytearray) - casts bytearray to single-character string  
unicode(str) - same as str.decode("ascii")  
unicode(bytearray) - same as bytearray.decode("ascii")  
bytearray(str) - casts single-byte string to bytearray  
bytearray(unicode, encoding) - equivalent to bytearray(unicode.encode(encoding))  
bytes() - alias for str()

### Python 2 Concatenations
str() + bytearray() -> bytearray()

### Python 3 String and Byte Types
str - sequence of unicode characters  
bytes - immutable sequence of bytes  
bytearray - mutable sequence of bytes

### Python 3 Encoding/Casting
str.encode(encoding) - to bytes object with specified encoding  
str.decode(encoding) - n/a  
bytes.encode(encoding) - n/a  
bytes.decode(encoding) - to unicode string from specified encoding  
bytearray.encode() - n/a  
bytearray.decode(encoding) - to unicode string from specified encoding  
str(bytes) - results in a string of the form "b'original string'"  
str(bytearray) - results in a string of the form "bytearray('ascii representation of bytes')"  
bytes(str, encoding) - to bytes object with specified encoding  
bytes(bytearray) - casts 8-bit bytearray to 8-bit bytes object  
bytearray(str, encoding) - to bytearray object with specified encoding  
bytearray(bytes) - casts to bytearray()

Common encodings are 'ascii' (7-bit), 'latin_1' (8-bit) and 'utf-8' (multi-byte)

### Python 3 Concatenations
bytes() + bytearray() -> bytes()  
bytearray() + bytes() -> bytearray()  
N.B. Resulting type is the type of the first object!


enjoy!
 
frankie@rootcode.org
