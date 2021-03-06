# Copyright (c) 2012-2013 Paul Tagliamonte <paultag@debian.org>
# Copyright (c) 2013 Leo Cavaille <leo@cavaille.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from debile.slave.wrappers.lintian import parse_lintian
from debile.utils.commands import run_command


def lintian(targets, analysis, lintian_binary='lintian'):

    if not isinstance(targets, list):
        targets = [targets]

    log = ""
    failed = False
    for target in targets:
        out, err, ret = run_command([lintian_binary, "-IE", "--pedantic",
                                     "--show-overrides", target])
        for issue in parse_lintian(out.splitlines(), target):
            analysis.results.append(issue)
            if issue.severity == 'error':
                failed = True
        log += out

    return (analysis, log, failed, None, None)


def version(lintian_binary='lintian'):
    out, err, ret = run_command([
        lintian_binary, '--version'
    ])
    if ret != 0:
        raise Exception(lintian_binary + " is not installed")
    name, version = out.split(" ")
    return (name, version.strip())
