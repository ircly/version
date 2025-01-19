# version.py version 1.0.0 2024
#
# Copyright 2024-2025 iRacly <iracly@hotmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import getpass
import os
import platform
import subprocess
import textwrap
import time


# See Semantic Versioning 2.0.0 https://semver.org/
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_PRERELEASE = "baby"

VERSION_STR = str(VERSION_MAJOR) +\
    '.' + str(VERSION_MINOR) +\
    '.' + str(VERSION_PATCH)
VERSION_FULL = VERSION_STR +\
    (('-' + VERSION_PRERELEASE) if VERSION_PRERELEASE else '')

NOW_TIMESTAMP = time.mktime(time.localtime())
GEN_DATE_GMT = time.strftime('%d.%m(%b).%Y', time.gmtime(NOW_TIMESTAMP))
GEN_TIME_GMT = time.strftime('%d.%m(%b).%Y %H:%M:%S', time.gmtime(NOW_TIMESTAMP))
GEN_TIME_LOCAL = time.strftime('%d.%m(%b).%Y %H:%M:%S (GMT%z)', time.localtime(NOW_TIMESTAMP))
GEN_TIME_STAMP_GMT = NOW_TIMESTAMP

USER_NAME = getpass.getuser()
HOST_NAME = platform.node()


def hg_ver():
    hg_process = subprocess.Popen("hg id -i -n --encoding utf8", shell=True, stdout=subprocess.PIPE)
    ans = hg_process.stdout.readline().strip().decode('utf8').split()
    if ans:
        return ans
    return "n/a", "n/a"


def hg_branch():
    hg_process = subprocess.Popen("hg id -b --encoding utf8", shell=True, stdout=subprocess.PIPE)
    ans = hg_process.stdout.readline().strip().split()
    if ans:
        return ans[0].decode('utf8')
    return "n/a"


def hg_commitinfo(rev):
    if isinstance(rev, str):
        if rev[-1] == '+':
            rev = rev[:-1]
    cmd = 'hg log --encoding utf8 --template "{node|short} #{rev} @{branch}, {date|shortdate}, {author|person} -- {desc|firstline}\\n" -r "%s"' % rev
    hg_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ans = hg_process.stdout.readline().strip().decode('utf8')
    if ans:
        return ans
    return ""


VERSION_SOURCES_COMMIT, _ = hg_ver()
VERSION_SOURCES_CLEAN = "false" if VERSION_SOURCES_COMMIT[-1] == '+' else "true"
VERSION_SOURCES_BRANCH = hg_branch()
VERSION_SOURCES = hg_commitinfo(VERSION_SOURCES_COMMIT)


def update_outdated_file(file_content, file_path):
    def is_different(file_content, abs_path):
        if not os.path.exists(abs_path):
            print(f'destination file "{file_path}" does not exists')
            return True
        with open(abs_path, "rb") as f:
            saved_data = f.read().decode('utf8')
        return saved_data.splitlines()[2:] != file_content.splitlines()[2:]

    abs_path = os.path.abspath(file_path)
    if is_different(file_content, abs_path):
        print(f'writing {abs_path}...')
        with open(abs_path, "wb") as f:
            f.write(file_content.encode('utf8'))
    else:
        print(f'no changes for {abs_path}')
    return


def compose_include_file(file_name:str = 'version'):
    content = textwrap.dedent(f'''\
    // {file_name}.h
    // generated: {GEN_TIME_LOCAL} by {USER_NAME} at {HOST_NAME}
    // this is aumtomatically generated file, please do not edit
    #pragma once
    #include <cstdint>

    #define VERSION_MAJOR  {VERSION_MAJOR}
    #define VERSION_MINOR  {VERSION_MINOR}
    #define VERSION_PATCH  {VERSION_PATCH}
    #define VERSION        "{VERSION_STR}"
    #define VERSION_FULL   "{VERSION_FULL}"
    #define VERSION_BUILD_DATE_GMT "{GEN_DATE_GMT}"

    extern const char* VERSION_BUILD_TIME_GMT;
    extern uint64_t    VERSION_BUILD_TIME_STAMP;

    extern const char* VERSION_SOURCES;
    extern bool        VERSION_SOURCES_CLEAN;
    extern const char* VERSION_SOURCES_BRANCH;
    extern const char* VERSION_SOURCES_COMMIT;
    ''')
    return content


def compose_sources_file(file_name:str):
    content = textwrap.dedent(f'''\
    // {file_name}.cpp
    // generated: {GEN_TIME_LOCAL} by {USER_NAME} at {HOST_NAME}
    // this is aumtomatically generated file, please do not edit
    #include "{file_name}.h"
    #include <cstdint>

    // build time
    const char* VERSION_BUILD_TIME_GMT = "{GEN_TIME_GMT}";

    // build timestamp
    // microseconds since Thursday, January 1, 1970 00:00:00 (GMT)
    uint64_t VERSION_BUILD_TIME_STAMP  = {int(GEN_TIME_STAMP_GMT * 1000000)}ULL;

    const char* VERSION_SOURCES = "{VERSION_SOURCES}";
    bool        VERSION_SOURCES_CLEAN  = {VERSION_SOURCES_CLEAN};
    const char* VERSION_SOURCES_BRANCH = "{VERSION_SOURCES_BRANCH}";
    const char* VERSION_SOURCES_COMMIT = "{VERSION_SOURCES_COMMIT}";
    ''')
    return content


hdr_file_content = compose_include_file('app-version')
src_file_content = compose_sources_file('app-version')
update_outdated_file(hdr_file_content, 'app-version.h')
update_outdated_file(src_file_content, 'app-version.cpp')
