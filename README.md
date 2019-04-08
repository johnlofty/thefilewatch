## *the file watch*
[![Downloads](https://pepy.tech/badge/thefilewatch)](https://pepy.tech/project/thefilewatch)
[![996.ICU](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu) 
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)


* capable to watch multi files at the same time. 
* base on pyinotify
* easy to use



## install
<code>$ pip install thefilewatch</code>

## quick use

<code>$ python -m thefilewatch.file_watch a.txt b.txt</code>


## simple example

```python
import sys
from thefilewatch.file_watch import BaseWatchHandler, FileWatch

class PrintHandler(BaseWatchHandler):

    def process(self, content):
        print('getting content ', content)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('need watch files')
        exit(1)
    else:
        file_list = sys.argv[1:]
    
    watcher = FileWatch(file_list, PrintHandler())
    watcher.start()
```

start watching files

<code>$ python -m thefilewatch.file_watch a.txt b.txt</code>

## more examples

see more specific examples in handlers folder.
