import pyinotify
import os

wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY

class Tailer:
    def __init__(self, path):
        self.file_path = path
        self.file = open(path, 'r')
        self.file_size = os.path.getsize(self.file_path)
        self.file.seek(0, 2)
        self.try_count = 0

    def reload(self):
        try:
            print('reloading ...')
            self.file.close()
            self.file = open(self.file_path, 'r')
            self.file_size = os.path.getsize(self.file_path)
            self.file.seek(0, 2)
            return True
        except Exception as e:
            print('exception ', e)
            return False


    def process(self):
        now_size = os.path.getsize(self.file_path)
        print('now size {} last_size {}'.format(now_size, self.file_size))
        if now_size < self.file_size:
            while self.try_count < 10:
                if not self.reload():
                    self.try_count += 1
                else:
                    self.try_count = 0
                    break

            if self.try_count >= 10:
                raise Exception('Open %s failed after try 10 times' % self.file_path)

        else:
            self.file_size = now_size

        curr_position = self.file.tell()
        print('curr_position ', curr_position)
        line = self.file.readlines()
        print('raw line ', line)
        if not line:
            self.file.seek(curr_position)
        else:
            print('line ', line)


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, file_list, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_map = {}
        for file in file_list:
            abs_path = os.path.abspath(file)
            tailer = Tailer(abs_path)
            self.file_map[abs_path] = tailer

    def process_IN_MODIFY(self, event):
        # print('event ', event)
        # print('map ', self.file_map)
        file_path = event.pathname
        if file_path not in self.file_map:
            print('not found')
            return

        tailer = self.file_map[file_path]
        tailer.process()


file_list = ['a.txt', 'b.txt']
handler = EventHandler(file_list)

notifier = pyinotify.Notifier(wm, handler)

for file in file_list:
    wm.add_watch(file, mask)

notifier.loop()
