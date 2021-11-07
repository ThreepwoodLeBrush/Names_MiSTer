#!/usr/bin/env python3
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

import os
from pathlib import Path
import hashlib
import json
import time
import re
import subprocess
import sys
from datetime import datetime
import os
import tempfile

def main(sha):
    print('sha: %s' % sha)

    url_base = envvar('URL_BASE')
    git_push = envvar('GIT_PUSH', 'false') == 'true'

    dbs = []

    for entry in os.scandir('.'):
        if not entry.is_file():
            continue

        if not entry.name.startswith('names_') or not entry.name.endswith('.txt'):
            continue

        path = Path(entry.name)

        dbs.append((path.stem + '.json', {
            'base_files_url': '',
            'db_id': 'names_txt',
            'db_files': [],
            'db_url': (url_base % 'dbs') + path.stem + '.json',
            'default_options': {},
            'files': {
                'names.txt': {
                    'hash': hash(entry.name),
                    'size': size(entry.name),
                    'url': (url_base % sha) + entry.name
                }
            },
            'folders': {},
            'timestamp': int(time.time()),
            'zips': {},
        }))

    changes_detected = False

    for db_name, db in dbs:
        old_db = get_db_from_db_url(db['db_url'])
        if dbs_are_different(db, old_db):
            changes_detected = True

    if not changes_detected:
        print("No dbs needed.")
        return

    if git_push:
        run_successfully('git checkout -qf --orphan dbs')
        run_successfully('git rm -rf .github * || true')

    for db_name, db in dbs:
        with open(db_name, 'w+') as f:
            json.dump(db, f, indent=4, sort_keys=True)

        if git_push:
            run_successfully('git add %s' % db_name)

    if git_push:
        run_successfully('git commit -m "-"')
        run_successfully('git fetch origin')
        run_successfully('git push --force origin dbs')

def get_db_from_db_url(db_url):
    try:
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            print('Downloading %s to %s' % (db_url, tmp_file.name))
            run_successfully('curl --show-error --fail --location -o %s %s' % (tmp_file.name, db_url))
            json_str = run_stdout("unzip -p %s" % tmp_file.name)
            return json.loads(json_str)
    except:
        return None

def dbs_are_different(input_db1, input_db2):
    if input_db1 is None or input_db2 is None:
        return True

    db1 = input_db1.copy()
    db2 = input_db2.copy()
    db1["timestamp"] = 0
    db2["timestamp"] = 0
    str1 = json.dumps(db1, sort_keys=True)
    str2 = json.dumps(db2, sort_keys=True)

    print()
    print('str1:')
    print(str1)
    print()
    print('str2:')
    print(str2)
    print()

    return str1 != str2

def envvar(var, backup=None):
    result = os.getenv(var, backup)
    print("{} = {}".format(var, result))
    return result

def hash(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
        return file_hash.hexdigest()

def size(file):
    return os.path.getsize(file)

def run_successfully(command):
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    if stdout.strip():
        print(stdout)

    if stderr.strip():
        print(stderr)

    if result.returncode != 0:
        raise Exception("subprocess.run %s Return Code was '%d'" % (command, result.returncode))

def run_stdout(command):
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception("subprocess.run Return Code was '%d'" % result.returncode)

    return result.stdout.decode()

if __name__ == '__main__':
    main(sys.argv[1])
