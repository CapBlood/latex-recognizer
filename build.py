#!/usr/bin/env python

import sys
import subprocess
import shutil
import os
import pathlib
import configparser

from PyInstaller.__main__ import run as pyinstall_run


root_path = pathlib.Path(__file__).parent
os.chdir(root_path.resolve())

config = configparser.ConfigParser()
config.read('setup.cfg')
NAME_APP = config["metadata"]["name"]

if sys.platform == "darwin":
    pyinstall_run([
        'latex_recognizer/__main__.py',
        '--windowed',
        '--noconfirm',
        '--clean',
        '--osx-bundle-identifier',
        'com.capblood.latex.recognizer',
        '--add-data',
        'latex_recognizer/models:models',
        '--add-data',
        'latex_recognizer/assets:assets',
        '-n',
        NAME_APP
    ])

    if os.path.exists("./dmg_dist"):
        shutil.rmtree("./dmg_dist")
    os.mkdir("dmg_dist")
    os.mkdir("dmg_dist/{}".format(NAME_APP))
    shutil.copytree("./dist/{}.app".format(NAME_APP),
                    "./dmg_dist/{}/{}.app".format(NAME_APP,
                                                  NAME_APP))

    command = "hdiutil create -srcfolder ./dmg_dist/{} ./dmg_dist/{}.dmg".format(NAME_APP, NAME_APP)
    subprocess.call(command.split())

