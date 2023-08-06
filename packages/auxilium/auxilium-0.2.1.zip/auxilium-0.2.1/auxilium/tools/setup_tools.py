# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.10, copyright Tuesday, 05 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from datetime import date
from logging import log, INFO
from os import getcwd, sep, walk, makedirs
from os.path import exists, join, basename, splitext
from shutil import move
from zipfile import ZipFile

from .const import ICONS, REPLACE
from .system_tools import open

EXT = ' (created by auxilium)'
PKG_ZIP_FILE = \
    __file__.replace(join(*__file__.split(sep)[-2:]), join('data', 'pkg.zip'))
FILE_EXT = '.py', '.rst', '.in'


def create_project(name=None, slogan=None, author=None, email=None, url=None,
                   pkg_zip_file=PKG_ZIP_FILE, path=getcwd()):
    """create a new project"""

    if not any((name, slogan, author, email)):
        log(INFO, '')
        log(INFO, 'Please enter project details.')
        log(INFO, '')

    name = input('Enter project name  : ') if name is None else name
    slogan = input('Enter project slogan: ') if slogan is None else slogan
    slogan += EXT
    author = input('Enter author name   : ') if author is None else author
    email = input('Enter project email : ') if email is None else email
    url = input('Enter project url  : ') if url is None else url
    url = url or 'https://github.com/<author>/<name>'

    pkg = name
    for r in REPLACE:
        pkg = pkg.replace(r, '_')
    project_path = join(path, pkg)
    pkg_path = join(path, pkg, pkg)

    # setup project infrastructure
    if exists(project_path):
        msg = 'Project dir %s exists. ' \
              'Cannot create new project.' % project_path
        raise FileExistsError(msg)

    if not exists(pkg_zip_file):
        msg = 'Project template %s does not exists. ' \
              'Cannot create new project.' % pkg_zip_file
        raise FileNotFoundError(msg)

    with ZipFile(pkg_zip_file, 'r') as zip_ref:
        zip_ref.extractall(project_path)

    makedirs(pkg_path)
    move(project_path + sep + '__init__.py', pkg_path)

    # setup source directory
    def rp(pth):
        f = open(pth, 'r')
        c = f.read()
        f.close()

        c = c.replace('<url>', url)
        c = c.replace('<email>', email)
        c = c.replace('<author>', author)
        c = c.replace('<doc>', slogan)
        c = c.replace('<name>', name)
        c = c.replace('<pkg>', pkg)
        c = c.replace('<date>', date.today().strftime('%A, %d %B %Y'))

        f = open(pth, 'w')
        f.write(c)
        f.close()
        return pth

    for subdir, _, files in walk(pkg):
        for file in files:
            if splitext(file)[1] in FILE_EXT:
                rp(join(subdir, file))

    log(INFO, '')
    log(INFO, ICONS["create"] +
        'created project %s with these files:' % name)
    log(INFO, ICONS[""] + 'in %s' % project_path)
    log(INFO, '')
    log(INFO, ICONS[""] + 'in %s' % path)
    for subdir, _, files in walk(name):
        log(INFO, '')
        for file in sorted(files):
            log(INFO, ICONS[""] + '  ' + join(subdir, file))
    log(INFO, '')
    return project_path


def create_finish(name=basename(getcwd())):
    log(INFO, ICONS["finish"] + 'project setup finished')
    log(INFO, '')
    log(INFO, 'Consider a first full run via: ')
    log(INFO, '')
    log(INFO, '  > cd %s' % name)
    log(INFO, '  > auxilium test')
    log(INFO, '  > auxilium doc --api')
    log(INFO, '  > auxilium build')
    log(INFO, '  > auxilium doc --show')
    log(INFO, '')
    return 0
