import os
import threading
from queue import Queue

from .downloads import download_dir, download_git, CONFIG_HOME, default_url, expand_path
from pyjsoncfg import Config


class BackgroundDownload(threading.Thread):
    def set_remote(self, pygg_url, dest_dir=None, opts=None, python_bin=None):
        self.url = pygg_url
        if dest_dir == None:
            dest_dir = download_dir
        self.dest_dir = dest_dir
        self.opts = opts
        self.python_bin = python_bin
        return self

    def start(self):
        self.qu = Queue()
        self.rc = None
        super().start()

    def run(self):
        super().run()
        self.rc = download_git(
            self.url,
            self.dest_dir,
            self.opts,
            callback=self._append_rc,
            python_bin=self.python_bin,
        )

    def _append_rc(self, rc):
        print(rc)
        self.qu.put(rc)

    def pop(self):
        try:
            return self.qu.get(block=False)
        except:
            pass


def get_download_task(url, opts=None, python_bin=None):
    return BackgroundDownload().set_remote(
        url, download_dir, opts=opts, python_bin=python_bin
    )


cfg = Config(expand_path([CONFIG_HOME, "config.json"]))
cfg_exists = cfg.exists()

if not cfg_exists:
    print("create new cfg")
    cfg().version = 1
else:
    print("load cfg")
    cfg.load()
    cfg.conv()
