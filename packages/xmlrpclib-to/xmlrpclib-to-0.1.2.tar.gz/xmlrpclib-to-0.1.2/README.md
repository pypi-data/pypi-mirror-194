[![Build Status](https://travis-ci.org/gisce/xmlrpclib-to.svg?branch=master)](https://travis-ci.org/gisce/xmlrpclib-to)

xmlrpclib-to
============

XMLRPC Client with timeout

```python
import socket

from xmlrpclib_to import ServerProxy

try
    proxy = ServerProxy('http://example.com', timeout=0.5)
    proxy.executeMethod()
except socket.timeout:
    print "Your are late..."
```
