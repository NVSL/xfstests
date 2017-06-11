#!/usr/bin/env python

import sys
import re

lines = sys.stdin.readlines()

l = 0
max_l = len(lines)

def skipped(name):
    return ""

def success(name):
    a = name.split("/")
    return '<testcase classname="{}" name="{}"/>'.format(a[0], a[1])

def failure(name, kind, reason):
    a = name.split("/")
    return """<testcase classname="{}" name="{}">
        <failure type="{}"> {}</failure>
    </testcase>""".format(a[0], a[1], kind, reason)
    

out = []

while l < max_l:
    g = re.search("^(\w+/\d\d\d)\s+", lines[l])
    if g:
        test_name = g.group(1)
        lines[l] = lines[l][len(g.group(0)):]
        #print "test = {}".format(test_name)
        #print lines[l]
        if re.search("^\[not run]", lines[l]):
            out.append(skipped(test_name))
        elif re.search("^\d+s \.\.\. \d+s", lines[l]):
            out.append(success(test_name))
        elif re.search("^\d+s", lines[l]):
            out.append(success(test_name))
        elif re.search("^- output mismatch", lines[l]) or re.search("^\[failed", lines[l]):
            error = lines[l]
            l += 1
            while l < max_l:
                if re.search("^    ", lines[l]):
                    error += lines[l][4:]
                else:
                    break
                l += 1
            out.append(failure(test_name, "failure", error))
    
    l += 1

print """<testsuite name="xfstests" tests="{count}">
{tests}
</testsuite>
""".format(count=len(out), tests='\n'.join(out))
