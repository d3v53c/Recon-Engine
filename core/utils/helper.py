import os
import threading
import time
import pyautogui
import math
import validators
import re
import socket
import importlib
import inspect

from itertools import cycle
from halo import Halo
from datetime import datetime
from pathlib import Path
from random import randint


def banner(native_print=False):
    logoTxt = """

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
         R E C O N - E N G I N E        v0.1 
======================================================
    """
    return logoTxt


def ticktock(win, exit_event):
    """
    Basic implementation of a timer.
    TODO: Implement a killable threading instance or self killing timer.
    Maybe pass in an instance to notify death time.
    """
    tick = 0
    while not exit_event.isSet():
        tick += 1
        win.addstr(
            1, 1,
            f"{str(math.floor(tick / (60 * 60))).zfill(2)}:{str(math.floor(tick / 60)).zfill(2)}:{str(tick % 60).zfill(2)}"
        )
        win.refresh()
        time.sleep(1)


def spinner(win):
    s = cycle(['-', '\\', '|', '/'])
    while True:
        win.addstr(1, 1, next(s))
        win.refresh()
        time.sleep(0.1)


def start_timer(screen, exit_event):
    timer_thread = threading.Thread(target=ticktock, args=(screen, exit_event))
    timer_thread.start()


def makedir(directory):
    curpath = os.getcwd()
    new_path = os.path.join(curpath, directory)

    if not os.path.exists(directory):
        os.makedirs(directory)
        created = True
    else:
        created = False
    return created


def touch_file(path):
    Path(path).touch()


def get_home_dir():
    return os.getcwd()


def init_logger():
    today = datetime.now()
    home_dir = get_home_dir()
    logfilename = 'engine_' + str(today.year) + str(today.month) + str(
        today.day) + str(today.hour) + str(today.minute) + str(
            today.second) + ".log"
    makedir(os.path.join(home_dir, 'logs'))
    filepath = os.path.join(home_dir, 'logs', logfilename)
    touch_file(filepath)
    return filepath


def makedir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return False
    return True


def delall(fpath):
    dircount, fcount = 0, 0
    for (root, dirs, files) in os.walk(fpath, topdown=True):
        for file in files:
            os.remove(os.path.join(root, file))


def wrap_html_line_break(func):
    def inner(*args, **kwargs):
        return "\n<br>" + func(*args, **kwargs) + "<br>\n"

    return inner


def generate_report_template(target, version):
    content = f"<HTML><HEAD><TITLE>'F I R E W A L L    S E G M E N T A T I O N      T O O L' -{version}</TITLE>"
    content += f"{REPORT_STYLE}"
    content += "</HEAD><Center><HR>"
    content += "<H2  class='tg'>FIREWALL SEGMENTATION REPORT<H2>"
    content += f"<H4  class='tg'> TARGET: {target}</H2><HR>"
    return content


@wrap_html_line_break
def create_html_component(_type, data, sclass=""):
    if _type is None:
        return data

    html = f"<{_type} class={sclass}>{data}</{_type}>"
    if _type in ["hr", "br"]:
        html = f"<{_type}>"
    return html


def spoof_mac():
    chars = "0123456789abcdef"
    mac_parts = map(
        lambda _: f"{chars[randint(0, 15)]}{chars[randint(0, 15)]}",
        range(1, 7),
    )
    return ":".join(mac_parts)


def take_snapshot(filepath, filename):
    try:
        path = os.path.join(filepath, filename)
        pic = pyautogui.screenshot()
        pic.save(path)
    except Exception as e:
        return True, str(e)
    else:
        return False, ""


def validate_ip_address(ip_addr):
    """
    Check if an IP address is valid.

    :param ip_addr: IP address
    :returns: True / False: if valid / invalid.
    """
    l, parts = len(ip_addr), ip_addr.split('.')
    if l < 7 or l > 16:
        return False
    if not len(parts) == 4:
        return False
    if not all(0 <= int(p) < 256 for p in parts):
        return False
    return True


def mask_host_bits(ip_addr, parts, fill=None):
    """
    Returns parts of an IP specified.
    Eg: 192.168.45.2 -> 192.168.45.*

    :param ip_addr: IP address
    :param parts: No. of parts to be returned (out of 4)
    :param fill: Character to fill on the removed part
    :returns: masked ip. See example above
    """
    if not validate_ip_address(ip_addr):
        raise ValueError(f"Invalid IP address specified : {ip_addr}")
    if int(parts) > 4:
        raise ValueError(f"No. of parts must be less than 4.")
    octets = ip_addr.split(".")
    resultant_ip = ".".join(octets[:parts])
    if fill is not None:
        resultant_ip += f".{fill}" * (4 - parts)
    return resultant_ip


def validate_domain(domain):
    """
    Validates a domain name.

    :param domain: domain name Eg: example.com
    :returns: boolean. True/False
    """
    return validators.domain(domain)


def find_match(regex, text, stripchars='^$'):
    """
    Finds a match from given text and return match else None.

    :param regex: Regular expression
    :param text: Target text
    :param stripchars: Characters to be removed from left and right
    :returns: boolean match object if match found else False
    """
    regex = regex.strip(stripchars)
    match = re.search(regex, text)
    if match:
        return match
    return False


def regex_multisearch(search_dict, text):
    """
    Search multiple values using unique regex for each.

    :param search_dict: {label_for_each_search: (regex_for_each, group_num_to_return)}
    :param text: Text in which search should be done
    :returns: dict(label_for_each_search=search_output or None)
    """
    search_val = dict()
    for label, regex in search_dict.items():
        cb = None
        if not isinstance(regex, tuple):
            raise ValueError(
                f"Expected a tuple (expr, (group1, group2), callback), but got {regex}"
            )

        try:
            if len(regex) > 2:
                exp, group, cb = regex
            else:
                exp, group = regex
        except:
            raise

        match = find_match(exp, text)
        if match:
            if isinstance(group, tuple):
                search_val[label] = [match.group(g) for g in group]
            else:
                search_val[label] = match.group(group)
            if cb:
                search_val[label] = cb(search_val[label])

    return search_val


def resolve_ip_from_domain(domain):
    """
    Resolves Domain address to an IP address.

    :param domain: Valid domain name
    :returns: IP address pointed to Domain
    """
    if not validate_domain(domain):
        raise ValueError("Invalid domain name.")
    return socket.gethostbyname(domain)


def import_module(filepath):
    """
    Imports module from filepath dynamically.
    """
    spec = importlib.util.spec_from_file_location("", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_class(obj):
    """
    Returns True if obj is a class, else False.
    """
    return inspect.isclass(obj)


def is_subclass(tcls, scls, strict=True):
    """
    Returns True only if `tcls` is a subclass of `scls` and
    not `scls` itself. 
    """
    return tcls is not scls and issubclass(tcls, scls)


def is_class_and_subclass(tcls, scls, strict=True):
    """
    Combination of `is_class` and `is_subclass`
    """
    return is_class(tcls) and is_subclass(tcls, scls)


def extract_script_classes(module, target_kls):
    """
    Returns list of classes (`Script`) detected from the module.
    """
    return iter(kls for name, kls in inspect.getmembers(module)
                if is_class_and_subclass(kls, target_kls))


def list_files_in_dir(dir_path):
    """
    List out files only from a target directory path.
    """
    if not os.path.isdir(dir_path):
        raise ValueError('`dir_path` must be a directory.')
    return iter(f for f in os.listdir(dir_path)
                if os.path.isfile(os.path.join(dir_path, f)))


def check_for_open_port(ip_addr, port, timeout=None):
    """
    Creates a socket connection and tries to connect to the specified port.
    If connection succeeds returns True, else False.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if timeout is not None:
        sock.settimeout(timeout)
    conn = sock.connect_ex((ip_addr, port))
    sock.close()
    return conn == 0
