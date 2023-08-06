import os
import re
import subprocess
import json
import traceback
import sys

verbose = False
shellposix = False

def vprint(*args, **kwargs):
    if verbose:
        if shellposix:
            kwargs["file"] = sys.stderr
        print(*args, **kwargs)

def gprint(msg, *args, **kwargs):
    if shellposix:
        kwargs["file"] = sys.stderr
    msg = text_format_to_color(msg)
    print(msg, *args, **kwargs)

def cmdprint(cmd):
    if not shellposix:
        print("Please restart the terminal to enable kiwi")
        return
    print(f"@kiwicmd {cmd}")

def get_python_link_name(pydll_path, os_name):
    if os_name == "linux":
        for so in os.listdir(pydll_path):
            if so.startswith("libpython") and not so.endswith(".so") and so.find(".so") != -1:
                basename = os.path.basename(so[3:so.find(".so")])
                full_path = os.path.join(pydll_path, so)
                return basename, full_path
    return "", ""

def format_size(size):

    units = ["Byte", "KB", "MB", "GB", "PB"]
    for i, unit in enumerate(units):
        ref = 1024 ** (i + 1)
        if size < ref:
            div = 1024 ** i
            if i == 0:
                return f"{size} {unit}"
            else:
                return f"{size / div:.2f} {unit}"
    return f"{size} Bytes"

def run_bash_command_out_to_console(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")

    while True:
        realtime_output = p.stdout.readline()
        if realtime_output == "" and p.poll() is not None:
            break

        if realtime_output:
            print(realtime_output, flush=True, end="")
    return p.returncode

def run_bash_command_get_output(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")

    output = ""
    while True:
        realtime_output = p.stdout.readline()
        if realtime_output == "" and p.poll() is not None:
            break

        if realtime_output:
            output += realtime_output
    return output.strip(), p.returncode

# 3.1, 2.5, 3.1.6.8, 2.5.4.0
def version_to_int(version):

    array = version.split(".")
    if len(array) > 4:
        vprint(f"Ignore numbers after 4 digits of the version number, {version}")
        array = array[:4]
    
    multipliers = [1<<48, 1<<32, 1<<16, 1]
    imultiplier = 0
    output_number = 0
    for value in array:
        value = int(re.sub("\D", "", value))
        if value > (1 << 16):
            vprint(f"Numbers larger than {1 << 16} are trimmed to within {1 << 16}, when {value} > {1 << 16}")
            value = 1 << 16

        output_number += value * multipliers[imultiplier]
        imultiplier += 1
    return output_number

# return False if version can not meet the limit
def version_limit(version, minimum_limit=None, maximum_limit=None):

    if minimum_limit is None and maximum_limit is None:
        vprint("The return value is always True when both minimum_limit and maximum_limit are None.")
        return True

    iversion = version_to_int(version)
    if minimum_limit is not None:
        iminimum_limit = version_to_int(minimum_limit)
        if iversion < iminimum_limit:
            return False
    
    if maximum_limit is not None:
        imaximum_limit = version_to_int(maximum_limit)
        if iversion > imaximum_limit:
            return False
    return True

def remove(file):
    try:
        os.remove(file)
        vprint(f"Remove success, file: {file}")
    except:
        vprint(f"Can not remove file: {file}")

def loadjson_dict(file):
    try:
        if os.path.exists(file):
            with open(file, "r") as f:
                val = json.load(f)

            if not isinstance(val, dict):
                vprint(f"A worng config file found, I will remove it.{file}")
                remove(file)
                return None
            return val
        return None
    except:
        vprint(f"Failed to load json: {file}")
        return None

def dumpjson_dict(file, obj):
    try:
        with open(file, "w") as f:
            json.dump(obj, f, indent=4)
        return True
    except:
        print(f"An error encounter when dump the obj to file: {file}")
        return False

def replace_with_var_map(file, text, vars_dict, inverse=False):
    replaced = False
    printed  = False
    printed_dict = set()
    file_name = os.path.basename(file)

    if not inverse:
        items = re.split("(\${@[A-Za-z.\-_]{1,64}})", text)
        for i, item in enumerate(items):
            if item.startswith("${@") and item.endswith("}"):
                var_name = item[3:-1]
                if var_name in vars_dict:
                    if not printed:
                        printed = True
                        vprint(f"Replace the file variables: {file}")

                    if var_name not in printed_dict:
                        printed_dict.add(var_name)
                        vprint(f" {file_name} -- {var_name} -> {vars_dict[var_name]}")
                    items[i] = vars_dict[var_name]
                    replaced = True
                else:
                    vprint(f"Can not find variable {var_name}")
        
        if replaced:
            text = "".join(items)
    else:
        for value in vars_dict:
            name = vars_dict[value]
            if text.find(value) != -1:
                replaced = True
                if not printed:
                    printed = True
                    vprint(f"Replace the file variables: {file}")

                vprint(f" {file_name} -- {value} -> {name}")
                text = text.replace(value, f"${{@{name}}}")
    return replaced, text

def replace_file_with_var_map(file, vars_dict, root, inverse=False):

    try:
        if not os.path.exists(file):
            vprint(f"Can not replace variable in file: {file}")
            return False

        try:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError as e:
            gprint(f"Can not replace variable in file, maybe it is a binary file: {file}")
            return False

        use_cache  = False
        # if change the file, remove cache
        # if no change the file, use cahce
        rel_path   = file[len(root):]
        if rel_path != "" and rel_path[0] == "/":
            rel_path = rel_path[1:]

        cache_file = os.path.join(root, ".kiwi", "cache", rel_path)
        record_file = os.path.join(root, ".kiwi", "cache", rel_path + ".mtime")
        cache_dir  = os.path.dirname(cache_file)

        if not inverse:
            if os.path.exists(cache_file) and os.path.exists(record_file):
                file_record_time = int(open(record_file, "r", encoding="utf-8").read())
                if os.stat(file).st_mtime_ns == file_record_time:
                    text = open(cache_file, "r", encoding="utf-8").read()
                    use_cache = True
                    vprint(f"Use cached file: {cache_file}")

        replaced, new_text = replace_with_var_map(file, text, vars_dict, inverse)
        if replaced:
            with open(file, "w", encoding="utf-8") as f:
                f.write(new_text)

            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)

            with open(record_file, "w", encoding="utf-8") as f:
                f.write(str(os.stat(file).st_mtime_ns))

            if not use_cache and not inverse:
                vprint(f"Update cache file: {cache_file}")
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(text)
        return True
    except:
        traceback.print_exc()
        gprint(f"Can not replace variable in file: {file}")
    return False


# [1]${this}/lib:[2]${this}/lib2
def parse_weight_path(paths, default_weight=10):
    weight_items = []
    for item in paths.split(":"):
        if item.startswith("["):
            p = item.find("]")
            if p == -1:
                weight_items.append([default_weight, item])
                continue

            weight_items.append([int(item[1:p]), item[p+1:]])
            continue
        weight_items.append([default_weight, item])
    return weight_items

def text_format_to_color(text):
    
    color_maps = {
        "red"   : "31",
        "green" : "32",
        "yellow": "33",
        "blue"  : "34",
        "mag"   : "35",
        "cyan"  : "36",
    }
    
    def replace(match):
        a, c, b = match.groups(0)
        if a in color_maps:
            dcolor = color_maps[a]
        elif b in color_maps:
            dcolor = color_maps[b]
        else:
            return c

        return f"\033[{dcolor}m{c}\033[0m"

    return re.sub("<([a-zA-Z]+)>(.*?)</([a-zA-Z]+)>", replace, text)