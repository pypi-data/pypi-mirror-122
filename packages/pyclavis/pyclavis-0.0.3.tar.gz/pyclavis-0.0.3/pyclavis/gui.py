import sys
import os
import time

import json
import webbrowser

import tkinter
from tkinter import Tk, messagebox, simpledialog, Toplevel

from .logging import log, print_t, print_e

from .pyclavis import *
from .tile import *

from .common import expand_path, readkeyfile, createkeystorage, readkeystore
from .browse import get_supported_browsers
from .xgui_util import (
    clear_clipboard,
    write_clipboard,
    open_file_explorer,
    DELAY_KEY,
    CHUNK_SIZE,
)
from .replacer import replace_str
from .config import get_download_task, cfg, cfg_exists, default_url
from .downloads import get_provider_services, CONFIG_HOME, default_repo_url
from .profiles import load_profiles
from .passgen import predef_alphabet, SecretGen, PassGen
from .updatecheck import check_download_version, do_pip_install, get_check_download_task

from .singleinstance import check_instance

#


def check_instance_or_die():
    pnam = os.path.join(CONFIG_HOME, "socket.info")
    pnam = expand_path(pnam)
    rc = check_instance(info_name="pyclavis", pnam=pnam)
    print_t("check_instance", rc)
    if rc == None:
        sys.exit()
    return rc


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
        print_t("update provider")
        gt("provider").set_values(provider)
        if len(provider) > 0:
            gt("provider").set_val(curprov)
        gt("service").set_values(get_prov_serv())


#


def set_passphrase():
    print_t("set_passphrase")
    global storage
    storage = createkeystorage(passphrase)


def load_sec_credits_or_default():

    set_passphrase()

    loaded = readkeystore(secman, storage)
    if loaded == None:
        # wrong password
        return False

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


def on_cat_sel(self):
    _, sel_cat = self.get_val()
    set_cat(sel_cat)
    gt("credit").set_index(0)
    set_selected_text()


def set_cat(sel_cat):
    global curcat
    if sel_cat in secman.store:
        curcat = sel_cat
    else:
        curcat = 0

    cc = get_cat_credits()
    gt("credit").set_values(cc)


def get_cat_credit_text(x):
    elem = secman.store[curcat][x]
    return elem.name + " / " + elem.user


#


def on_credit_sel(x):
    set_selected_text()


def on_credit_double(x):
    on_credit_sel(x)
    open_selection()


#


def on_credit_edit_ok():
    print_t("on_credit_edit_ok")

    global credit_dlg, credit_vals

    try:
        credit, _category = credit_vals
        credit_org = secman.get(credit, _category)

        secman.remove(credit_org)
    except:
        print_e("no credit to remove")

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

    # set_cat_cred()
    gt("category").set_values(secman.store.keys())
    # set_cat(_category)
    gt("credit").set_values(get_cat_credits())

    ##

    on_credit_edit_close()

    credit_save(show_msg=True)


def on_credit_edit_close():
    print_t("on_credit_edit_close")
    global credit_dlg, credit_vals
    credit_main.unregister_idn()
    credit_dlg.destroy()
    credit_dlg = None
    credit_org = None


credit_main = None
credit_dlg = None
credit_vals = None


def on_credit_add():
    print_t("on_credit_edit")

    if credit_dlg:
        return

    _category, credit, _provider, service, browser, profile = compact()

    if _category == str(None).lower():
        _category = None

    open_credit_dlg(Credential(category=_category))


def on_credit_edit():
    print_t("on_credit_edit")

    if credit_dlg:
        return

    global credit_vals

    _category, credit, _provider, service, browser, profile = compact()

    print_t(_category, credit, _provider, service, browser, profile)

    credit_vals = credit, _category

    credit_org = secman.get(credit, _category)

    open_credit_dlg(credit_org)


def on_show_pass():
    vis = gt("chk_show_passwd").get_val()
    gt("edit_pass").show(vis)


def open_credit_dlg(credit_org):

    global credit_dlg, credit_main

    credit_main = TileRows(
        source=[
            TileEntry(
                idn="edit_name",
                caption="name",
                value=str(credit_org.name if credit_org.name else ""),
            ),
            TileEntry(
                idn="edit_user",
                caption="user",
                value=str(credit_org.user if credit_org.user else ""),
            ),
            TileEntryPassword(
                idn="edit_pass",
                caption="password",
                value=str(credit_org.passwd if credit_org.passwd else ""),
            ),
            TileEntry(
                idn="edit_cat",
                caption="category",
                value=str(credit_org.category if credit_org.category else ""),
            ),
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
                    TileCheckbutton(
                        idn="chk_show_passwd",
                        caption="show password",
                        on_click=on_show_pass,
                    ),
                ]
            ),
        ]
    )

    mainframe = gt("mainframe")

    tk = mainframe.tk
    frame = mainframe.frame

    credit_dlg = Toplevel(tk)
    # credit_dlg.transient(tk)

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
    print_t(credit)

    secman.remove(credit)

    set_cat_cred()
    gt("category").set_values(secman.store.keys())
    set_cat(_category)
    gt("credit").set_values(get_cat_credits())

    credit_save()


def credit_save(really=True, show_msg=False):
    print_t("credit_save")
    credits = secman.tolist()
    # todo just for development
    if really:
        storage.save(credits)
    if show_msg:
        messagebox.showinfo("info", "credits saved")
    on_passwd_clr()


def on_passwd_save():
    print_t("on_passwd_save")
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
    print_t("on_passwd_clr")
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
    gt("service").set_index(0)
    set_selected_text()


def on_prov_usel(self):
    set_prov(None)


def set_prov(sel):
    print_t(sel)
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
    set_selected_text()


def on_serv_right(self):

    sel = self.get_mapval()

    print_t("on_serv_right", sel)

    elem = prov_serv[curprov][sel]

    content = elem["url"]
    autofill = elem["autofill"]

    messagebox.showinfo(f"autofill {sel}", f"{content}\n---\n{autofill}")


def set_serv(sel):
    print_t(sel)
    elem = prov_serv[curprov][sel]
    print_t(elem["autofill"])


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

    print_t(_category, credit, _provider, service, browser, profile)

    return _category, credit, _provider, service, browser, profile


def deflate(hist):
    (_category, _credit, _provider, service, browser, profile) = hist

    print_t(hist)

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
    print_t("open_selection")
    hist = compact()
    history_add(hist)

    (_category, credit, _provider, service, browser, profile) = hist

    try:
        url = prov_serv[_provider][service]["url"]

        profile_cfg = {}
        if profile:
            profile_cfg = profiles[profile]

        env_cfg = load_env_profile()

        print_t("profile, env", profile_cfg, env_cfg)

        print_t("before", url)
        url = replace_str(url, [profile_cfg, env_cfg, os.environ])
        print_t("after", url)

        webbrowser.get(browser).open(url, new=0)

    except Exception as ex:
        print_e(ex)
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
    print_t("play_autofill")

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

    print_t("profile, env", profile_cfg, env_cfg)

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
    print_t("history_set", hist)
    if hist != None:
        hist = list(hist)
        if hist in history_stack:
            history_stack.remove(hist)
        history_stack.append(hist)
    history_save()
    set_history(False)

    # print(history_stack)


def set_history(scrollend=True):
    global history_stack
    hist = gt("history")
    hist.set_values(history_stack)
    if scrollend:
        hist.set_index(-1)


def get_history_text(hist):
    # print("history", hist)

    (_category, credit, _provider, service, browser, profile) = hist

    s = build_selected_text(_category, credit, _provider, service, browser, profile)

    return s


def set_selected_text():
    s = build_selected_text(*compact())
    s = "selected: " + s
    gt("curselectinfo").text(s)


def build_selected_text(_category, credit, _provider, service, browser, profile):

    hist = _category, credit, _provider, service, browser, profile

    _credit = secman.get(credit, category=_category)

    try:
        # check provider and service
        serv = prov_serv[_provider][service]

        infostr = (
            _credit.name
            + " / "
            + _credit.user
            + " @ "
            + serv["name"]
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
            print_t("history version load", thisversion, version)
            if version[0] > thisversion[0]:
                print("history reset due to upgrade version")
                history_stack = []

            history_stack = jso["HISTORY"]

            # upgrade old structure
            for hist in history_stack:
                if len(hist) < 6:
                    hist.append(None)

    except Exception as ex:
        print_e("history_load", ex)

    set_history()


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
    print_t(cur_hist)
    deflate(cur_hist)
    set_selected_text()


def on_hist_double(x):
    on_hist_sel(x)
    open_selection()
    set_selected_text()


def on_hist_del():
    print_t(cur_hist)
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
    print_t("new delay std", oval, nval)
    global delay_std
    delay_std = nval
    save_setting()


def on_delay_key(oval, nval):
    print_t("new delay key", oval, nval)
    global delay_key
    delay_key = nval
    save_setting()


#


def copy_user():
    print_t("copy_user")
    kill_task()
    sched_task()
    (_category, credit, _provider, service, browser, profile) = compact()
    _credit = secman.get(credit, _category)
    write_clipboard(_credit.user)


def copy_passwd():
    print_t("copy_passwd")
    kill_task()
    sched_task()
    (_category, credit, _provider, service, browser, profile) = compact()
    _credit = secman.get(credit, _category)
    write_clipboard(_credit.passwd)


#


def delay_scramble_text():
    return f"<-- scrambled after {delay_scramble} sec"


def on_delay_scramble(oval, nval):
    print_t("new delay scramble", oval, nval)
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
    print_t("clr_task")
    clear_clipboard()
    kill_task()


_tasks = []


def sched_task():
    print_t("sched_task")
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

task_version = None


def on_check_new_version():
    global task_version
    if task_version:
        raise Exception("already running")
    log_stat("getting version.")
    task_version = get_check_download_task(
        default_repo_url, VERSION, git_opts, python_bin=python_bin
    )
    task_version.start()
    _sync_log_version_task()


def _sync_log_version_task():
    gt("mainframe").tk.after(500, on_log_version_update)


def on_log_version_update():
    global task_version
    if task_version:
        while True:
            t = task_version.pop()
            if t == None:
                break
            log_append(t)
        if task_version.is_alive() == False:
            check_new_version_task_done(task_version.rc)
            task_version = None
            log_stat("download done\n")
        else:
            _sync_log_version_task()


def check_new_version_task_done(rc):

    update, ver, thisversion = rc

    if update == False:
        messagebox.showinfo("status", f"installed version {thisversion} is up to date.")
    else:
        rc = messagebox.askyesnocancel(
            "status",
            f"installed version {thisversion}\n"
            f"available version {ver}\n\n"
            f"do you want to update now?\n\n"
            f"you need to restart the application after updating.",
        )

        print_t("update check answer", rc)

        if rc == True:
            log_stat("update started.")
            do_pip_install("pyclavis", python_bin=python_bin, callb=log_append)
            log_stat("update done.")


#


def on_download_default():
    global task, task_pending
    if task:
        raise Exception("already running")

    task_pending = [default_url, *providers]
    next_download()


def next_download():
    global task, task_pending
    if len(task_pending) > 0:
        print_t(task_pending)
        url = task_pending.pop(0)
        task = get_download_task(url, opts=git_opts, python_bin=python_bin)
        task.start()
        _sync_log_task()
        log_stat(f"download started: {url}\n")
    else:
        print_t("update tile data")
        on_download_refresh()


def on_download_refresh():
    set_provider_services(True)


def download_stop():
    print_t("download_stop")
    task_pending = []


def _sync_log_task():
    gt("mainframe").tk.after(500, on_log_update)


def on_log_update():
    global task
    if task:
        while True:
            t = task.pop()
            if t == None:
                break
            log_append(t)
        if task.is_alive() == False:
            task = None
            log_stat("download done\n")
            next_download()
        else:
            _sync_log_task()


def log_stat(msg, prelude="\n---\n"):
    nowts = time.strftime("%H:%M:%S %d.%m.%Y")
    log_append(f"{prelude}{nowts} {msg}\n")


def log_append(t):
    lg = gt("logtext")
    lg.append(t)


#


def on_browser_sel(x):
    print_t("on_browser_sel", x)
    set_selected_text()


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
    print_t("on_prof_sel")

    global cur_prof
    cur_prof = x.get_val()[1]

    set_prof_data()
    set_selected_text()


def on_prof_usel(x):
    print_t("on_prof_usel")

    global cur_prof
    cur_prof = None

    set_prof_data(False)
    set_selected_text()


def set_prof_data(dumpex=True):
    print_t("set_prof_data", cur_prof)
    try:
        if cur_prof in profiles:
            data = json.dumps(profiles[cur_prof], indent=4)
        else:
            data = "---empty---"
    except Exception as ex:
        data = ex if dumpex else "---empty-profile---"
        print("exception", ex)
    gt("profile_data").set_val(data)


#


def quit_all(frame):
    def quit():
        print_t("quit_all")
        # removes all, including threads
        # sys.exit()
        # soft, state remains
        download_stop()
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
                idn="maintabs",
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
                                            nullable=False,
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
                                            nullable=False,
                                        ),
                                        TileEntryListbox(
                                            idn="credit",
                                            caption="credit",
                                            values=get_cat_credits(),
                                            map_value=get_cat_credit_text,
                                            on_select=on_credit_sel,
                                            on_double_click=on_credit_double,
                                            nullable=False,
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
                            on_select=on_browser_sel,
                            map_value=lambda x: x,
                        ),
                    ),
                    (
                        ("history", "t_history"),
                        TileRows(
                            source=[
                                TileLabel(caption=""),
                                TileEntryListbox(
                                    idn="history",
                                    caption="select",
                                    values=history_stack,
                                    map_value=get_history_text,
                                    on_select=on_hist_sel,
                                    on_double_click=on_hist_double,
                                    nullable=False,
                                    max_show=13,
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
                                TileCols(
                                    source=[
                                        TileLabelButton(
                                            caption="log history",
                                            commandtext="clear",
                                            command=on_log_clr,
                                        ),
                                        TileLabelButton(
                                            caption="programm update",
                                            commandtext="check",
                                            command=on_check_new_version,
                                        ),
                                    ]
                                ),
                                TileCols(
                                    source=[
                                        TileLabelButton(
                                            caption="pyclavis provider data",
                                            commandtext="download",
                                            command=on_download_default,
                                        ),
                                        TileLabelButton(
                                            caption="from disk",
                                            commandtext="reload",
                                            command=on_download_refresh,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ),
                    (
                        "password generator",
                        TileRows(
                            source=[
                                TileLabel(
                                    caption="generate password from a given alphabet"
                                ),
                                TileEntryText(
                                    idn="alphabet",
                                    width=25,
                                    height=4,
                                    caption="alphabet",
                                ),
                                TileLabelButton(
                                    caption="default alphabet",
                                    commandtext="reset",
                                    command=on_reset_pass_gen,
                                ),
                                TileEntryInt(
                                    idn="thepasswdlen",
                                    caption="length ( 6 >= x <= 32 )",
                                    min_val=6,
                                    max_val=32,
                                ),
                                TileLabelButton(
                                    caption="new password",
                                    commandtext="generate",
                                    command=on_new_pass_gen,
                                ),
                                TileEntry(
                                    idn="thepasswd",
                                    caption="password",
                                    width=32,
                                ),
                                TileLabelButton(
                                    caption="password to clipboard",
                                    commandtext="copy",
                                    command=on_copy_pass_gen,
                                ),
                            ]
                        ),
                    ),
                ],
            ),
            TileLabel(idn="curselectinfo", caption=""),
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
            TileCols(
                source=[
                    TileLabelClick(caption=f"homepage: {_homepage}", on_click=openweb),
                    TileLabel(
                        caption=f"version: {VERSION}",
                    ),
                    TileLabel(caption=":-)"),
                ]
            ),
        ]
    )

    return mainframe, main


#


def on_reset_pass_gen():
    gt("alphabet").set_val(predef_alphabet)


def on_new_pass_gen():
    _alphabet = gt("alphabet").get_val()

    alphabet = ""
    for c in _alphabet:
        if c in predef_alphabet:
            alphabet += c

    pwlen = int(gt("thepasswdlen").get_val())
    pw = SecretGen(baseset=alphabet, passlen=pwlen).create()
    gt("thepasswd").set_val(pw)


def on_copy_pass_gen():
    write_clipboard(gt("thepasswd").get_val())
    gt("thepasswd").set_val("")
    print_t("passwd copy 2 clipboard")


PASSWORD_LENGTH = 12


def set_password_state():
    on_reset_pass_gen()
    gt("thepasswdlen").set_val(PASSWORD_LENGTH)


#

python_bin = None
downloads_version = None


def save_setting():
    mv_setting(True)
    cfg.save()
    print_t("saved")


def mv_setting(src2cfg=True):
    global delay_std, delay_key, delay_scramble, clip_chunk
    global providers, git_opts, python_bin, downloads_version
    if src2cfg == True:
        print_t("src2cfg")
        cfg().delay_std = delay_std
        cfg().delay_key = delay_key
        cfg().delay_scramble = delay_scramble
        cfg().clip_chunk = clip_chunk
        cfg().providers = providers
        cfg().git_opts = git_opts
    else:
        print_t("cfg2src")
        delay_std = cfg.setdefault("delay_std", delay_std)
        delay_key = cfg.setdefault("delay_key", delay_key)
        delay_scramble = cfg.setdefault("delay_scramble", delay_scramble)
        clip_chunk = cfg.setdefault("clip_chunk", clip_chunk)
        providers = cfg.setdefault("providers", [])
        git_opts = cfg.setdefault("git_opts", git_opts)
        python_bin = cfg.setdefault("python", "python3")
        print_t("using python_bin:", python_bin)
        downloads_version = cfg.setdefault("downloads_version", None)
        print_t("using downloads_version:", downloads_version)


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
    set_password_state()


def startup():

    load_sec_credits_or_default()

    set_provider_services()

    mainframe, main = build_mainframes()

    mainframe.add(main)
    mainframe.resize_grip()
    mainframe.layout()

    set_settings()
    set_states()

    history_load()
    if len(history_stack) > 0:
        gt("maintabs").select("t_history")

    mainframe.mainloop()


def ask_startup_passphrase():

    tk_root = Tk()
    tk_root.withdraw()

    # just for checking
    set_passphrase()

    if not storage.exists():
        print_t(
            "found no storage",
        )
        messagebox.showinfo(
            "info", "found no storage. create new one. enter password next."
        )
    # done checking

    caption = "Password"

    # check key file
    clavis = readkeyfile()

    # ask and check password

    while clavis != True:

        if type(clavis) != str:
            passwd = simpledialog.askstring(
                caption, "Enter password: (empty for exit)", show="*", parent=tk_root
            )
        else:
            passwd = clavis

        if passwd:
            global passphrase
            passphrase = passwd
        else:
            sys.exit()

        clavis = load_sec_credits_or_default()

        caption = "Wrong Password, try again"

    tk_root.destroy()
