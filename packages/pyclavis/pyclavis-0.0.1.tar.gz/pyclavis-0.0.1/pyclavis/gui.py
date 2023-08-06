import sys
import os
import time

import json
import webbrowser

import tkinter
from tkinter import Tk, messagebox, simpledialog, Toplevel

from .browse import get_supported_browsers
from .xgui_util import (
    clear_clipboard,
    write_clipboard,
    open_file_explorer,
    DELAY_KEY,
    CHUNK_SIZE,
)
from .replacer import replace_str

from .pyclavis import *

from .downloads import get_provider_services, CONFIG_HOME, expand_path
from .profile import load_profiles

from .config import get_download_task, cfg, cfg_exists, default_url

from .tile import *

#

_homepage = "https://github.com/kr-g/pyclavis"

#

supported_browsers = get_supported_browsers()

#

# todo
passphrase = "init"

#


HIST_VERSION = "0.1"
history_dir = expand_path(os.path.join(CONFIG_HOME, "history.json"))
history_stack = []
cur_hist = 0

#

delay_std = DELAY_STD
delay_key = DELAY_KEY

delay_scramble = 15

#

task = None
task_pending = []

#

secman = CredentialStore()
storage = None

categories = []
curcat = None

prov_serv = None

provider = None
curprov = None

providers = []  # for download url


#


def set_provider_services(update=False):
    global prov_serv, provider, curprov

    prov_serv = get_provider_services()

    provider = sorted(prov_serv.keys())
    if len(provider) > 0:
        curprov = provider[0]

    if update:
        print("update provider")
        gt("provider").set_values(provider)
        if len(provider) > 0:
            gt("provider").set_val(curprov)
        gt("service").set_values(get_prov_serv())


set_provider_services()

#


def set_passphrase():
    print("set_passphrase")
    pp = KeyBase64Conv().convert(passphrase)
    conv = ConvJson()
    global storage
    storage = CryptedFileBackend(conv=conv, passphrase=pp)


def load_sec_credits_or_default():

    set_passphrase()

    loaded = False
    secman.clear()

    if storage.exists():
        try:
            _credits = storage.load()

            print("loaded", _credits)

            secman.fromlist(_credits)
            loaded = True

        except Exception as ex:
            print(ex, "load credits")
    else:
        print("no storage file found")
        loaded = True

    set_cat_cred()

    return loaded


def set_cat_cred():
    global categories
    categories = list(secman.store.keys())
    global curcat
    curcat = categories[0] if len(categories) > 0 else None


#


def get_cat_credits():
    # print(secman.store[curcat])
    try:
        return secman.store[curcat].keys()
    except:
        return []


def set_cat_credits():
    gt("category").set_values()


def on_cat_sel(self):
    _, sel_cat = self.get_val()
    set_cat(sel_cat)


def set_cat(sel_cat):
    global curcat
    if sel_cat in secman.store:
        curcat = sel_cat
    else:
        curcat = list(secman.store.keys())[0]

    cc = get_cat_credits()
    gt("credit").set_values(cc)


def get_cat_credit_text(x):
    elem = secman.store[curcat][x]
    return elem.name + " / " + elem.user


#


def on_credit_edit_ok():
    print("on_credit_edit_ok")

    global credit_dlg, credit_vals

    try:
        credit, _category = credit_vals
        credit_org = secman.get(credit, _category)

        secman.remove(credit_org)
    except:
        print("no credit to remove")

    idn = [
        "edit_name",
        "edit_user",
        "edit_pass",
        "edit_cat",
    ]
    idn = list(map(lambda x: gt(x).get_val(), idn))
    cred = Credential(*idn)
    print(cred)

    secman.set(cred)

    credit_save(show_msg=True)

    # set_cat_cred()
    gt("category").set_values(secman.store.keys())
    # set_cat(_category)
    gt("credit").set_values(get_cat_credits())

    ##

    on_credit_edit_close()


def on_credit_edit_close():
    print("on_credit_edit_close")
    global credit_dlg, credit_vals
    credit_main.unregister_idn()
    credit_dlg.destroy()
    credit_dlg = None
    credit_org = None


credit_main = None
credit_dlg = None
credit_vals = None


def on_credit_add():
    print("on_credit_edit")

    if credit_dlg:
        return

    _category, credit, _provider, service, browser, profile = compact()

    if _category == str(None).lower():
        _category = None

    open_credit_dlg(Credential(category=_category))


def on_credit_edit():
    print("on_credit_edit")

    if credit_dlg:
        return

    global credit_vals

    _category, credit, _provider, service, browser, profile = compact()

    print(_category, credit, _provider, service, browser, profile)

    credit_vals = credit, _category

    credit_org = secman.get(credit, _category)

    open_credit_dlg(credit_org)


def open_credit_dlg(credit_org):

    global credit_dlg, credit_main

    credit_main = TileRows(
        source=[
            TileEntry(idn="edit_name", caption="name", value=credit_org.name),
            TileEntry(idn="edit_user", caption="user", value=credit_org.user),
            TileEntryPassword(
                idn="edit_pass", caption="password", value=credit_org.passwd
            ),
            TileEntry(idn="edit_cat", caption="category", value=credit_org.category),
            TileCols(
                source=[
                    TileButton(
                        caption="",
                        commandtext="ok",
                        on_click=on_credit_edit_ok,
                    ),
                    TileButton(
                        caption="",
                        commandtext="cancel",
                        on_click=on_credit_edit_close,
                    ),
                ]
            ),
        ]
    )

    mainframe = gt("mainframe")

    tk = mainframe.tk
    frame = mainframe.frame

    credit_dlg = Toplevel(tk)

    mframe = Tile(credit_dlg, tk_root=credit_dlg)

    mframe.tk.protocol("WM_DELETE_WINDOW", on_credit_edit_close)
    # mframe.tk.bind("<Escape>", lambda e: on_credit_edit_close)

    mframe.add(credit_main)

    mframe.layout()


def on_credit_del():
    confirm = messagebox.askokcancel(
        "please confirm", "do you really want to remove the credit?"
    )
    if confirm != True:
        return

    print("on_credit_del")
    (_category, credit, _provider, service, browser, profile) = compact()

    credit = secman.get(credit, category=_category)
    print(credit)

    secman.remove(credit)

    set_cat_cred()
    gt("category").set_values(secman.store.keys())
    set_cat(_category)
    gt("credit").set_values(get_cat_credits())

    credit_save()


def credit_save(really=True, show_msg=False):
    print("credit_save")
    credits = secman.tolist()
    # todo just for development
    if really:
        storage.save(credits)
    if show_msg:
        messagebox.showinfo("info", "credits saved")
    on_passwd_clr()


def on_passwd_save():
    print("on_passwd_save")
    p1 = gt("passwd_1").get_val().strip()
    p2 = gt("passwd_2").get_val().strip()

    if p1 != p2:
        messagebox.showerror("error", "passwords do not match")
        return

    if len(p1) == 0:
        messagebox.showerror("error", "password can not be empty")
        return

    global passphrase
    passphrase = p1
    set_passphrase()

    credit_save(really=True, show_msg=True)


def on_passwd_clr():
    print("on_passwd_clr")
    gt("passwd_1").set_val("")
    gt("passwd_2").set_val("")


#


def get_prov_serv():
    try:
        return sorted(prov_serv[curprov])
    except:
        return []


def on_prov_sel(self):
    _, sel = self.get_val()
    set_prov(sel)


def on_prov_usel(self):
    set_prov(None)


def set_prov(sel):
    print(sel)
    global curprov
    curprov = sel
    gt("service").set_values(get_prov_serv())
    gt("service").scrollbar()


def get_prov_serv_text(x):
    elem = prov_serv[curprov][x]
    try:
        return elem["name"]
    except:
        print("broken", x)
        return "---broken---"


def on_serv_sel(self):
    _, sel = self.get_val()
    set_serv(sel)


def on_serv_right(self):

    sel = self.get_mapval()

    print("on_serv_right", sel)

    elem = prov_serv[curprov][sel]

    content = elem["url"]
    autofill = elem["autofill"]

    messagebox.showinfo(f"autofill {sel}", f"{content}\n---\n{autofill}")


def set_serv(sel):
    print(sel)
    elem = prov_serv[curprov][sel]
    print(elem["autofill"])


#


def compact(which=None):

    if which == None:
        which = ["category", "credit", "provider", "service", "browser", "profile"]

    _category = curcat
    credit = gt("credit").get_mapval()
    _provider = curprov
    service = gt("service").get_mapval()
    browser = gt("browser").get_mapval()
    profile = gt("profile").get_mapval()

    print(_category, credit, _provider, service, browser, profile)

    return _category, credit, _provider, service, browser, profile


def deflate(hist):
    (_category, _credit, _provider, service, browser, profile) = hist

    print(hist)

    gt("browser").set_val(browser)

    gt("category").set_val(_category)
    set_cat(_category)

    gt("credit").set_val(_credit)

    gt("provider").set_val(_provider)
    set_prov(_provider)

    gt("service").set_val(service)

    gt("profile").set_val(profile)
    set_prof(profile)


#


def open_selection():
    print("open_selection")
    hist = compact()
    history_add(hist)

    (_category, credit, _provider, service, browser, profile) = hist

    try:
        url = prov_serv[_provider][service]["url"]

        profile_cfg = {}
        if profile:
            profile_cfg = profiles[profile]

        env_cfg = load_env_profile()

        print("profile, env", profile_cfg, env_cfg)

        print("before", url)
        url = replace_str(url, [profile_cfg, env_cfg, os.environ])
        print("after", url)

        webbrowser.get(browser).open(url, new=0)

    except Exception as ex:
        print(ex)
        messagebox.showerror("not found, broken", str(hist))


def load_env_profile():
    fnam = expand_path([CONFIG_HOME, "env.json"])
    try:
        with open(fnam) as f:
            cont = f.read()
            jso = json.loads(cont)
            return jso
    except:
        return {}


def play_autofill():
    print("play_autofill")

    hist = compact()
    history_add(hist)
    (_category, credit, _provider, service, browser, profile) = hist

    elem = prov_serv[_provider][service]
    autofill_cmd = elem["autofill"]
    autofill_cfg = autofill_cmd.splitlines()

    lopa = LoginParam(service, Autofill(autofill_cfg))
    # print(lopa)

    _credit = secman.get(credit, _category)

    profile_cfg = {}
    if profile:
        profile_cfg = profiles[profile]

    env_cfg = load_env_profile()

    print("profile, env", profile_cfg, env_cfg)

    key_seq = lopa.autofill.get_seq(_credit.todict(), profile_cfg, env_cfg, os.environ)
    ## danger zone
    # this contain passwd in plain !!!
    # only for debugging !!!
    ## print(key_seq); return

    gt("mainframe").tk.iconify()

    send_seq(
        key_seq,
        interval=delay_std / 1000,
        interval_key=delay_key / 1000,
        chunk=clip_chunk,
    )


#


def version_split(s):
    nums = str(s).split(".")
    return list(map(lambda x: int(x), nums))


def history_add(hist):
    history_set(hist)


def history_set(hist=None):
    print("history_set", hist)
    if hist != None:
        hist = list(hist)
        if hist in history_stack:
            history_stack.remove(hist)
        history_stack.append(hist)
    h = gt("history")
    h.set_values(history_stack)
    history_save()

    print(history_stack)


def get_history_text(hist):
    # print("history", hist)

    (_category, credit, _provider, service, browser, profile) = hist

    _credit = secman.get(credit, category=_category)

    try:
        # check provider and service
        _ = prov_serv[_provider][service]

        infostr = (
            _credit.user
            + " @ "
            + service
            + (" << " + profile if profile else "")
            + " / "
            + browser
        )

        return infostr
    except:
        return "--broken--> " + str(hist)


def history_load():
    global history_stack
    try:
        with open(history_dir) as f:
            cont = f.read()
            jso = json.loads(cont)
            version = version_split(jso["VERSION"])
            thisversion = version_split(HIST_VERSION)
            print("history version load", thisversion, version)
            if version[0] > thisversion[0]:
                print("history reset due to upgrade version")
                history_stack = []

            history_stack = jso["HISTORY"]

            for hist in history_stack:
                if len(hist) < 6:
                    hist.append(None)

    except Exception as ex:
        print("history_load", ex)


def set_history():
    global history_stack
    gt("history").set_values(history_stack)


def history_save():
    try:
        with open(history_dir, "w") as f:
            cont = json.dumps(
                {"HISTORY": history_stack, "VERSION": HIST_VERSION}, indent=4
            )
            f.write(cont)
    except Exception as ex:
        print(ex)


def on_hist_sel(x):
    global cur_hist
    cur_hist = x.get_mapval()
    print(cur_hist)
    deflate(cur_hist)


def on_hist_del():
    print(cur_hist)
    history_stack.remove(cur_hist)
    history_set()


def on_hist_clr():
    confirm = messagebox.askokcancel(
        "please confirm", "do you really want to remove all?"
    )
    if confirm == True:
        history_stack.clear()
        history_set()


#


def on_delay_std(oval, nval):
    print("new delay std", oval, nval)
    global delay_std
    delay_std = nval
    save_setting()


def on_delay_key(oval, nval):
    print("new delay key", oval, nval)
    global delay_key
    delay_key = nval
    save_setting()


#


def copy_user():
    print("copy_user")
    kill_task()
    sched_task()
    (_category, credit, _provider, service, browser, profile) = compact()
    _credit = secman.get(credit, _category)
    write_clipboard(_credit.user)


def copy_passwd():
    print("copy_passwd")
    kill_task()
    sched_task()
    (_category, credit, _provider, service, browser, profile) = compact()
    _credit = secman.get(credit, _category)
    write_clipboard(_credit.passwd)


#


def delay_scramble_text():
    return f"<-- scrambled after {delay_scramble} sec"


def on_delay_scramble(oval, nval):
    print("new delay scramble", oval, nval)
    global delay_scramble
    delay_scramble = nval
    gt("delay_scramble_info").text(delay_scramble_text())
    save_setting()


clip_chunk = CHUNK_SIZE


def on_clip_chunk(oval, nval):
    global clip_chunk
    clip_chunk = nval
    save_setting()


git_opts = ""


def on_git_opts(oval, nval):
    global git_opts
    git_opts = nval
    save_setting()


#


def clr_task():
    print("clr_task")
    clear_clipboard()
    kill_task()


_tasks = []


def sched_task():
    print("sched_task")
    root = gt("mainframe").tk
    t = root.after(delay_scramble * 1000, clr_task)
    _tasks.append(t)


def kill_task():
    root = gt("mainframe").tk
    while len(_tasks) > 0:
        t = _tasks.pop()
        root.after_cancel(t)


#


def on_open_setting_dir():
    open_file_explorer(expand_path(CONFIG_HOME))


def openweb():
    webbrowser.open(_homepage)


def on_log_clr():
    gt("logtext").set_val("")


#


def on_download_default():
    global task, task_pending
    if task:
        raise Exception("running, press log update")

    task_pending = [default_url, *providers]
    next_download()


def next_download():
    global task, task_pending
    if len(task_pending) > 0:
        print(task_pending)
        url = task_pending.pop(0)
        task = get_download_task(url, opts=git_opts)
        task.start()
        _sync_log_task()
        log_stat(f"download started: {url}\n")
    else:
        print("update tile data")
        set_provider_services(True)


def _sync_log_task():
    gt("mainframe").tk.after(500, on_log_update)


def on_log_update():
    lg = gt("logtext")
    global task
    if task:
        while True:
            t = task.pop()
            if t == None:
                break
            lg.append(t)
        if task.is_alive() == False:
            task = None
            log_stat("download done\n")
            next_download()
        else:
            _sync_log_task()


def log_stat(msg, prelude="\n---\n"):
    nowts = time.strftime("%H:%M:%S %d.%m.%Y")
    gt("logtext").append(f"{prelude}{nowts} {msg}\n")


#

profiles = {}
cur_prof = None


def set_profiles():

    global profiles, cur_prof

    profiles = load_profiles()
    cur_prof = None

    keys = list(profiles.keys())
    keys.sort()
    gt("profile").set_values(keys)

    if False and len(profiles) > 0:
        cur_prof = keys[0]
        gt("profile").set_val(cur_prof)

    set_prof_data()


def set_prof(nam):
    global cur_prof
    cur_prof = nam if nam in profiles else None
    set_prof_data()


def on_prof_sel(x):
    print("on_prof_sel")

    global cur_prof
    cur_prof = x.get_val()[1]

    set_prof_data()


def on_prof_usel(x):
    print("on_prof_usel")

    global cur_prof
    cur_prof = None

    set_prof_data(False)


def set_prof_data(dumpex=True):
    print("set_prof_data", cur_prof)
    try:
        data = json.dumps(profiles[cur_prof], indent=4)
    except Exception as ex:
        data = ex if dumpex else "---empty---"
        print("exception", ex)
    gt("profile_data").set_val(data)


#


def quit_all(frame):
    def quit():
        print("quit_all")
        # removes all, including threads
        # sys.exit()
        # soft, state remains
        frame.quit()

    return quit


def build_mainframes():

    tk_root = Tk()

    mainframe = Tile(tk_root=tk_root, idn="mainframe")

    mainframe.tk.protocol("WM_DELETE_WINDOW", quit_all(mainframe))
    mainframe.tk.bind("<Escape>", lambda e: quit_all(mainframe)())

    main = TileRows(
        source=[
            TileLabelButton(
                caption="close app", commandtext="bye", command=quit_all(mainframe)
            ),
            TileTab(
                source=[
                    (
                        "base",
                        TileRows(
                            source=[
                                TileLabel(
                                    caption="select autofill provider / service",
                                ),
                                TileCols(
                                    source=[
                                        TileEntryListbox(
                                            idn="provider",
                                            caption="provider",
                                            values=provider,
                                            map_value=lambda x: x,
                                            on_select=on_prov_sel,
                                            on_unselect=on_prov_usel,  # todo remove
                                            nullable=False,
                                        ),
                                        TileEntryListbox(
                                            idn="service",
                                            caption="service",
                                            values=get_prov_serv(),
                                            map_value=get_prov_serv_text,
                                            on_select=on_serv_sel,
                                            on_right_click=on_serv_right,
                                        ),
                                    ]
                                ),
                                TileLabel(caption="select your category / credit"),
                                TileCols(
                                    source=[
                                        TileEntryListbox(
                                            idn="category",
                                            caption="category",
                                            values=secman.store.keys(),
                                            map_value=lambda x: x,
                                            on_select=on_cat_sel,
                                        ),
                                        TileEntryListbox(
                                            idn="credit",
                                            caption="credit",
                                            values=get_cat_credits(),
                                            map_value=get_cat_credit_text,
                                        ),
                                    ]
                                ),
                                TileCols(
                                    source=[
                                        TileLabelButton(
                                            caption="new credit",
                                            commandtext="add",
                                            command=on_credit_add,
                                        ),
                                        TileLabelButton(
                                            caption="selected credit",
                                            commandtext="edit",
                                            command=on_credit_edit,
                                        ),
                                        TileButton(
                                            # caption="",
                                            commandtext="remove",
                                            command=on_credit_del,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ),
                    (
                        "profile",
                        TileRows(
                            source=[
                                TileLabel(caption="select profile"),
                                TileCols(
                                    source=[
                                        TileEntryListbox(
                                            idn="profile",
                                            caption="select",
                                            values=[],
                                            map_value=lambda x: x,
                                            on_select=on_prof_sel,
                                            on_unselect=on_prof_usel,
                                        ),
                                        TileLabelButton(
                                            caption="profile data",
                                            commandtext="reload",
                                            command=set_profiles,
                                        ),
                                    ]
                                ),
                                TileEntryText(
                                    idn="profile_data",
                                    caption="data",
                                    height=10,
                                    readonly=True,
                                ),
                            ]
                        ),
                    ),
                    (
                        "browser",
                        TileEntryListbox(
                            idn="browser",
                            caption="select",
                            values=supported_browsers,
                            map_value=lambda x: x,
                        ),
                    ),
                    (
                        "history",
                        TileRows(
                            source=[
                                TileLabel(caption=""),
                                TileEntryListbox(
                                    idn="history",
                                    caption="select",
                                    values=history_stack,
                                    map_value=get_history_text,
                                    on_select=on_hist_sel,
                                    nullable=False,
                                    max_show=7,
                                    width=40,
                                ),
                                TileCols(
                                    source=[
                                        TileLabelButton(
                                            caption="selected history",
                                            commandtext="remove",
                                            command=on_hist_del,
                                        ),
                                        TileLabelButton(
                                            caption="all history",
                                            commandtext="clear",
                                            command=on_hist_clr,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ),
                    (
                        "settings",
                        TileRows(
                            source=[
                                TileLabelButton(
                                    caption="settings folder",
                                    commandtext="open",
                                    command=on_open_setting_dir,
                                ),
                                TileEntryInt(
                                    idn="delay_std",
                                    caption="delay standard [milli sec]",
                                    only_positiv=True,
                                    on_change=on_delay_std,
                                ),
                                TileEntryInt(
                                    idn="delay_key",
                                    caption="delay keystroke [milli sec]",
                                    min_val=0,
                                    max_val=1000,
                                    on_change=on_delay_key,
                                ),
                                TileEntryInt(
                                    idn="delay_scramble",
                                    caption="scramble clipboard [sec]",
                                    min_val=5,
                                    max_val=30,
                                    on_change=on_delay_scramble,
                                ),
                                TileEntryInt(
                                    idn="clip_chunk",
                                    caption="clipboard chunk size",
                                    min_val=3,
                                    max_val=7,
                                    on_change=on_clip_chunk,
                                ),
                                TileEntry(
                                    idn="git_opts",
                                    caption="pygitgrab opts (e.g. -c for credit file)",
                                    on_change=on_git_opts,
                                ),
                                TileTab(
                                    source=[
                                        (
                                            "change password",
                                            TileRows(
                                                source=[
                                                    # TileLabel(caption="change password"),
                                                    TileCols(
                                                        source=[
                                                            TileEntryPassword(
                                                                idn="passwd_1",
                                                                caption="new",
                                                            ),
                                                            TileEntryPassword(
                                                                idn="passwd_2",
                                                                caption="repeat",
                                                            ),
                                                        ]
                                                    ),
                                                    TileCols(
                                                        source=[
                                                            TileLabelButton(
                                                                caption="crypted passwords",
                                                                commandtext="save",
                                                                command=on_passwd_save,
                                                            ),
                                                            TileLabelButton(
                                                                caption="input fields",
                                                                commandtext="clear",
                                                                command=on_passwd_clr,
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ),
                    (
                        "download",
                        TileRows(
                            source=[
                                TileEntryText(idn="logtext", caption="log history"),
                                TileLabelButton(
                                    caption="log history",
                                    commandtext="clear",
                                    command=on_log_clr,
                                ),
                                TileLabelButton(
                                    caption="pyclavis provider data",
                                    commandtext="download",
                                    command=on_download_default,
                                ),
                            ]
                        ),
                    ),
                ]
            ),
            TileCols(
                source=[
                    TileLabelButton(
                        caption="open", commandtext="in browser", command=open_selection
                    ),
                    TileLabelButton(
                        caption="autofill",
                        commandtext="send key sequence",
                        command=play_autofill,
                    ),
                ]
            ),
            TileCols(
                source=[
                    TileLabelButton(
                        caption="user", commandtext="copy user", command=copy_user
                    ),
                    TileLabelButton(
                        caption="passwd", commandtext="copy passwd", command=copy_passwd
                    ),
                    TileLabel(
                        idn="delay_scramble_info",
                        caption=delay_scramble_text(),
                    ),
                ]
            ),
            TileLabel(caption=":-)"),
            TileCols(
                source=[
                    TileLabelClick(caption=f"homepage: {_homepage}", on_click=openweb),
                    TileLabel(
                        caption=f"version: {VERSION}",
                    ),
                ]
            ),
        ]
    )

    return mainframe, main


#


def save_setting():
    mv_setting(True)
    cfg.save()
    print("saved")


def mv_setting(src2cfg=True):
    global delay_std, delay_key, delay_scramble, clip_chunk, providers, git_opts
    if src2cfg == True:
        print("src2cfg")
        cfg().delay_std = delay_std
        cfg().delay_key = delay_key
        cfg().delay_scramble = delay_scramble
        cfg().clip_chunk = clip_chunk
        cfg().providers = providers
        cfg().git_opts = git_opts
    else:
        print("cfg2src")
        delay_std = cfg.setdefault("delay_std", delay_std)
        delay_key = cfg.setdefault("delay_key", delay_key)
        delay_scramble = cfg.setdefault("delay_scramble", delay_scramble)
        clip_chunk = cfg.setdefault("clip_chunk", clip_chunk)
        providers = cfg.setdefault("providers", [])
        git_opts = cfg.setdefault("git_opts", git_opts)


def set_settings():

    mv_setting(cfg_exists == False)

    gt("delay_std").set_val(delay_std)
    gt("delay_key").set_val(delay_key)
    gt("delay_scramble").set_val(delay_scramble)
    gt("clip_chunk").set_val(clip_chunk)
    gt("git_opts").set_val(git_opts)

    set_profiles()

    nowts = time.strftime("%H:%M:%S %d.%m.%Y")
    log_stat(f"good day. app started")


def set_states():
    pass


def startup():

    load_sec_credits_or_default()

    mainframe, main = build_mainframes()

    mainframe.add(main)
    mainframe.resize_grip()
    mainframe.layout()

    set_settings()
    set_states()

    history_load()
    set_history()

    mainframe.mainloop()


def ask_startup_passphrase():

    tk_root = Tk()
    tk_root.withdraw()

    # just for checking
    set_passphrase()

    if not storage.exists():
        print(
            "found no storage",
        )
        messagebox.showinfo(
            "info", "found no storage. create new one. enter password next."
        )
    # done checking

    caption = "Password"

    # only for development
    ask_password = True

    while ask_password:
        passwd = simpledialog.askstring(
            caption, "Enter password: (empty for exit)", show="*", parent=tk_root
        )

        if passwd:
            global passphrase
            passphrase = passwd
        else:
            sys.exit()

        if load_sec_credits_or_default():
            break

        caption = "Wrong Password, try again"

    tk_root.destroy()
