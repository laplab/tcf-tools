#!/usr/bin/env python3
import sys
import base64
from common import *

path = sys.argv[1]

c = connect()
handle = unwrap(c.FileSystem.open(path, 1, {}))
content_b64 = unwrap(c.FileSystem.read(handle, 0, 4096))[0]
content = base64.b64decode(content_b64).decode('utf-8')

print(content)

unwrap(c.FileSystem.close(handle))
