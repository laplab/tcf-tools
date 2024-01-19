#!/usr/bin/env python3
import sys
import base64
from common import *

local_path = sys.argv[1]
remote_path = sys.argv[2]

with open(local_path, 'r') as f:
    content = f.read()

content_b64 = base64.b64encode(bytes(content, 'utf-8'))

c = connect()
handle = unwrap(c.FileSystem.open(remote_path, 2, {}))
unwrap(c.FileSystem.write(handle, 0, content_b64))

unwrap(c.FileSystem.close(handle))
