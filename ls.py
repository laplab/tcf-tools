#!/usr/bin/env python3
import sys
from common import *

path = sys.argv[1]

c = connect()
handle = unwrap(c.FileSystem.opendir(path))
files = unwrap(c.FileSystem.readdir(handle))[0]

print('Permissions Name Size')
for file in files:
    filename = file["FileName"]
    attrs = file["Attrs"]
    permissions = attrs["Permissions"]
    size = attrs["Size"]
    print(f'{permissions:b} {filename} {size} bytes')

unwrap(c.FileSystem.close(handle))
