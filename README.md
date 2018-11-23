## *the file watch*

* capable to watch multi files at the same time. 
* base on pyinotify
* easy to use



## install
<code>$ pip install thefilewatch</code>

## how to use

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