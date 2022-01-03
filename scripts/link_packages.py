#!/usr/bin/python3
'''
Create symlinks to .ads and .adb files with expanded filenames.
'''
import os.path
import os
import sys

sources = ['gnat', 'gnarl']
links = 'links'

def package_name(path):
    with open(path, 'r') as fd:
        for line in fd.readlines():
            if line.startswith('package '):
                line = line.split(' ')[1:]
                if line[0] == 'body':
                    line = line[1:]
                return line[0]

def basename(filename):
    return filename.split('.', 1)[0]

bases = {}

if not os.path.exists('links'):
    os.makedirs('links')

for source in sources:
    for dirpath, dirnames, filenames in os.walk(source):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            pn = package_name(path)
            if pn is not None:
                bases[basename(filename)] = pn

    for dirpath, dirnames, filenames in os.walk(source):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            pn = bases.get(basename(filename), None)
            if pn is not None:
                newname = '%s.%s' % (pn.lower().replace('.', '-'), filename.rsplit('.', 1)[-1])
                newname = os.path.join(links, newname)
                path = os.path.join('../', path)
                print('ln', '-s', path, newname)
                os.symlink(path, newname)
