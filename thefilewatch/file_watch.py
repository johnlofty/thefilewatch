import pyinotify
import logging
import sys
import os

mask = pyinotify.IN_MODIFY

LOG = logging.getLogger('thefilewatch')

class BaseWatchHandler:

    def process(self, content):
        raise NotImplementedError


class Tailer:
    def __init__(self, path, content_handler):
        self.file_path = path
        self.file = open(path, 'r')
        self.file_size = os.path.getsize(self.file_path)
        self.file.seek(0, 2)
        self.try_count = 0
        self.handler = content_handler

    def reload(self):
        try:
            LOG.info('reloading file %s ...', self.file_path)
            self.file.close()
            self.file = open(self.file_path, 'r')
            self.file_size = os.path.getsize(self.file_path)
            self.file.seek(0, 2)
            return True
        except Exception as e:
            LOG.exception(e)
            return False

    def process(self):
        now_size = os.path.getsize(self.file_path)
        if now_size < self.file_size:
            while self.try_count < 10:
                if not self.reload():
                    self.try_count += 1
                else:
                    self.try_count = 0
                    break

            if self.try_count >= 10:
                LOG.error('Open %s failed after try 10 times' % self.file_path)
                raise Exception('Open %s failed after try 10 times' % self.file_path)

        else:
            self.file_size = now_size

        curr_position = self.file.tell()
        lines = self.file.readlines()
        if not lines:
            self.file.seek(curr_position)
        else:
            try:
                self.handler.process(lines)
            except Exception as e:
                logger.exception(e)


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, file_list, content_handler, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_map = {}
        for file in file_list:
            abs_path = os.path.abspath(file)
            tailer = Tailer(abs_path, content_handler)
            self.file_map[abs_path] = tailer

    def process_IN_MODIFY(self, event):
        file_path = event.pathname
        if file_path not in self.file_map:
            LOG.error('file path %s not found in file_map', file_path)
            return

        tailer = self.file_map[file_path]
        tailer.process()


class TailError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileWatch:
    def __init__(self, file_list, content_handler):
        if not isinstance(content_handler, BaseWatchHandler):
            raise TailError('invalid content handler %s', content_handler)

        self.file_list = file_list
        handler = EventHandler(file_list, content_handler)
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(wm, handler)
        for file_ in self.file_list:
            self.check_file_validity(file_)
            wm.add_watch(file_, mask)

    def check_file_validity(self, file_):
        if not os.access(file_, os.F_OK):
            raise TailError("File '%s' does not exis" % (file_))

        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))

        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))

    def start(self):
        LOG.info('Night gathers, and now my watch begins.')
        self.notifier.loop()


if __name__ == '__main__':
    import sys
    class PrintHandler(BaseWatchHandler):

        def process(self, content):
            if isinstance(content, list):
                for ele in content:
                    sys.stdout.write(ele)

            else:
                sys.stdout.write(content)

            sys.stdout.flush()

    if len(sys.argv) < 2:
        print('need watch files')
        exit(1)
    else:
        file_list = sys.argv[1:]

    watcher = FileWatch(file_list, PrintHandler())
    print('start watch ...')
    watcher.start()
