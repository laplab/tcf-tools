# TCF tools

Some basic tools for interacting with `tcf-agent`. Usage:

```
# Prints contents of the remote file.
$ ./cat.py <path-on-remote-filesystem>

# Lists all files and directories in the given path.
$ ./ls.py <path-on-remote-filesystem>

# Overwrites remote file with contents from the local file.
$ ./put.py <path-on-local-filesystem> <path-on-remote-filesystem>
```

## License

The code in the `tcf` directory is a slightly modified version of the code from [this Gitlab repository](https://gitlab.eclipse.org/eclipse/tcf/tcf). Code in this Gitlab repository was released under Eclipse Public License 2.0 (EPL) at the moment of writing. All credit goes to original authors.

Code outside of `tcf` directory is licensed under MIT license, which you can find below.

```
MIT License

Copyright (c) 2024 Nikita Lapkov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```