import os
import stat
import sys
import glob
import json
import pygitgrab

CONFIG_HOME = os.path.join("~", ".pyclavis")
DOWNLOAD_HOME = os.path.join(CONFIG_HOME, "downloads")
PROVIDER_SEP = "/"

default_url = "https://github.com/kr-g/pyclavis/autofill.pygg?ref=main"


def expand_path(fpath):
    if type(fpath) in [list, tuple]:
        fpath = os.path.join(*fpath)
    fpath = os.path.expandvars(fpath)
    fpath = os.path.expanduser(fpath)
    fpath = os.path.abspath(fpath)
    return fpath


def cur_download_dir():
    return expand_path(DOWNLOAD_HOME)


download_dir = cur_download_dir()


def curdir():
    return expand_path(os.path.curdir)


def download_git_i(cmd_line):
    p = os.popen(cmd_line)
    try:
        while True:
            resp = p.readline()
            if len(resp) == 0:
                break
            yield resp
    except:
        pass
    p.close()


def download_git(git_url, download_dir, opts=None, callback=print):
    # callback prints the status

    if opts == None:
        opts = ""

    os.makedirs(download_dir, exist_ok=True)

    push_dir = curdir()

    os.chdir(download_dir)
    cur_dir = curdir()

    if cur_dir != download_dir:
        raise Exception("cd failed", cur_dir, download_dir)

    done_ok = False
    try:
        cmd_line = f"python3 -m pygitgrab -url {git_url} {opts}".strip()
        print("download from", cmd_line)
        for rc in download_git_i(cmd_line):
            callback(rc)
        done_ok = True
    except Exception as ex:
        print(ex)

    os.chdir(push_dir)

    cur_dir = curdir()

    if cur_dir != push_dir:
        raise Exception("cd to pushed failed")

    return done_ok


def list_downloads(download_dir):

    os.makedirs(download_dir, exist_ok=True)

    fpath = os.path.join(download_dir, "**")
    allentries = glob.iglob(fpath, recursive=True)
    allfiles = filter(lambda x: stat.S_ISREG(os.stat(x).st_mode), allentries)
    # todo
    alljson = filter(lambda x: os.path.splitext(x)[1] in [".json", ".py"], allfiles)
    return alljson


def download_defaults():
    resp = download_git(default_url, download_dir)
    return resp


def strip_download_dir(x):
    return x.replace(download_dir + os.path.sep, "")


def strip_download_dirs(files):
    files = map(strip_download_dir, files)
    return files


def split_provider_service(x):
    prov, serv = os.path.split(x)
    serv, _ = os.path.splitext(serv)
    return prov, serv


def load_provider_json(files):
    sp = {}
    for fnam in files:
        with open(fnam) as f:
            c = f.read()
            o = json.loads(c)

            part = strip_download_dir(fnam)
            prov, serv = split_provider_service(part)

            # m[prov + PROVIDER_SEP + serv] = o
            sp.setdefault(prov, {})
            sp[prov][serv] = o

    return sp


def get_provider_services():
    files = list(list_downloads(download_dir))

    plain_ext = list(strip_download_dirs(files))
    _plain_str = list(map(lambda x: os.path.splitext(x)[0], plain_ext))

    provider_service = load_provider_json(files)

    return provider_service


provider_service = get_provider_services()
# download_defaults()
