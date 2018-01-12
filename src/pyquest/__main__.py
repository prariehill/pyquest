__author__ = "Adrian Welcker"
__copyright__ = """Copyright 2018 Adrian Welcker

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import argparse
import os
import sys
import tempfile
from zipfile import ZipFile

from pyquest.game import QuestGame

VERSION = "0.1-SNAPSHOT"

parser = argparse.ArgumentParser(prog="pyquest", description=
                                 'A Python-based interpreter for Quest interactive fiction games.')
parser.add_argument('filename', type=str, help="The name of a Quest game file.")
parser.add_argument('-v', '--verbose', help="Run in verbose mode", action='store_true')
arguments = parser.parse_args()

print("pyQuest", VERSION)
# if len(sys.argv) < 2:
#     print("\nUsage:")
#     print("py" if os.name == 'nt' else "python3", "-m pyquest [FILENAME]")
#     print("Where [FILENAME] is the name of a Quest game file")
#     print("(either a packed .quest file, or a raw .aslx source file)")
#     exit(1)

# This will become necessary for multimedia functions.
# try:
#     import pygame
# except ImportError:
#     print("*** Module pygame not found! Pygame is required to run pyQuest.", file=sys.stderr)
#     exit(1)

file_name = arguments.filename
if arguments.verbose:
    print("Considering", file_name)
if file_name[-4:] == ".zip" or file_name[-6:] == ".quest":
    print("Opening QUEST file...")
    try:
        zipped = ZipFile(file_name, 'r')
    except FileNotFoundError:
        print("*** Game File", file_name, "not found!", file=sys.stderr)
        exit(127)
    game_folder = tempfile.mkdtemp()
    zipped.extractall(game_folder)
    zipped.close()
    print(game_folder)
    # os.system('ls -lah ' + game_folder)
    the_game = QuestGame(game_folder, launch_dir=os.path.sep.join(os.path.split(file_name)[:-1]),
                         from_qfile=True, debug=arguments.verbose)
    the_game.run()
    os.system('rm -rf ' + game_folder)
else:
    if arguments.verbose:
        print("Hmm... doesn't look like a packed Quest game file to me.")
    the_game = QuestGame(sys.argv[1], from_qfile=False, debug=arguments.verbose)
    the_game.run()