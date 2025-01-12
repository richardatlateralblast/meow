#!/usr/bin/env python

# Name:         meow (MP3 tag Editor Organiser Writer)
# Version:      0.1.3
# Release:      1
# License:      CC-BA (Creative Commons By Attrbution)
#               http://creativecommons.org/licenses/by/4.0/legalcode
# Group:        System
# Source:       N/A
# URL:          https://github.com/lateralblast/meow
# Distribution: UNIX
# Vendor:       Lateral Blast
# Packager:     Richard Spindler <richard@lateralblast.com.au>

# pylint: disable=W0311
# pylint: disable=C0301
# pylint: disable=C0114
# pylint: disable=C0116
# pylint: disable=C0415
# pylint: disable=R0912
# pylint: disable=R0914
# pylint: disable=R0915
# pylint: disable=W0611
# pylint: disable=C0413
# pylint: disable=E0401

# Import modules

import argparse
import sys
import os
import re

from pathlib import Path

# Set some defaults

script_exe = sys.argv[0]
script_dir = os.path.dirname(script_exe)

# Check we have pip installed

try:
  from pip._internal import main
except ImportError:
  os.system("easy_install pip")
  os.system("pip install --upgrade pip")

# install and import a python module

def install_and_import(package):
  import importlib
  try:
    importlib.import_module(package)
  except ImportError:
    command = f"python3 -m pip3 install --user {package}"
    os.system(command)
  finally:
    globals()[package] = importlib.import_module(package)

# Load music_tag

try:
  import music_tag
except ImportError:
  install_and_import("music_tag")
  import music_tag

# Load tinytag

try:
  import tinytag
except ImportError:
  install_and_import("tinytag")
  import tinytag

from tinytag import TinyTag

# Load mutagen

try:
  import mutagen
except ImportError:
  install_and_import("mutagen")
  import mutagen

from mutagen.flac import FLAC
from mutagen.mp3 import MP3

# Load magic

try:
  import magic
except ImportError:
  install_and_import("python-magic")
  import magic
# Print help

def print_help():
  print("\n")
  command = f"{script_exe} -h"
  os.system(command)
  print("\n")

# Verbose message

def verbose_message(mode, message):
  if options['verbose'] is True or re.search("verbose", mode):
    match mode:
      case "warn":
        header = "Warning:\t"
      case "info":
        header = "Information:\t"
      case _:
        header =""
    string = f"{header}{message}"
    print(string)

# Warning message

def warning_message(message):
  verbose_message("warn", message)

# Information message

def information_message(message):
  verbose_message("info", message)

# Print version

def print_version():
  file_array = file_to_array(script_exe)
  version    = list(filter(lambda x: re.search(r"^# Version", x), file_array))[0].split(":")[1]
  version    = re.sub(r"\s+","",version)
  print(version)
  sys.exit()

# Read a file into an array

def file_to_array(file_name):
  with open(file_name, encoding="utf-8") as file_data:
    file_array = file_data.readlines()
  return file_array

# Build file name

def build_file_name():
  base_name = os.path.basename(options['file'])
  base_name, _ = os.path.splitext(base_name)
  dir_name  = os.path.dirname(options['file'])
  if re.search("-", base_name):
    fields = base_name.split("-")
  else:
    fields = {}
  _, file_extension = os.path.splitext(options['file'])
  if options['tracknumber'] is None:
    message = "Determining Track Number"
    information_message(message)
    track_number = str(options['counter'])
    if fields[0]:
      if not re.search(r"[A-Z]|[a-z]", fields[0]):
        if re.search(r"[0-9]", fields[0]):
          track_number = fields[0]
          track_number = re.sub(" ", "", track_number)
    options['tracknumber'] = track_number
  else:
    track_number = str(options['tracknumber'])
  if re.search(r"[0-9]", track_number):
    if len(track_number) < 2:
      track_number = f"0{track_number}"
  message = f"Setting Track Number to \"{track_number}\""
  information_message(message)
  if options['albumartist'] is None:
    message = "Determining Album Artist"
    information_message(message)
    if len(fields) > 2:
      if re.search(r"[A-Z]|[a-z]", fields[1]):
        band_name = fields[1]
    else:
      if len(fields) > 1:
        if re.search(r"[A-Z]|[a-z]", fields[0]):
          band_name = fields[0]
    band_name  = re.sub(r"^-|-$|^\s+|\s+$", "", band_name)
    options['artist'] = band_name
  else:
    band_name  = str(options['artist'])
  message = f"Setting Album Artist to \"{band_name}\""
  information_message(message)
  band_name  = re.sub(r"\/| |\s+", "_", band_name)
  if options['album'] is None:
    message = "Determining Album"
    information_message(message)
    album_name = os.path.basename(dir_name)
    if re.search("-", album_name):
      album_name = re.split("-", album_name)[1]
    if re.search(r"2[0-9][0-9][0-9]", album_name):
      temp_name = re.split(r"2[0-9][0-9][0-9]", album_name)[1]
      if not re.search(r"[0-9]|[A-Z]|[a-z]", temp_name):
        temp_name = re.split(r"2[0-9][0-9][0-9]", album_name)[0]
      album_name = temp_name
    album_name = re.sub(r"^-|-$|^\s+|\s+$", "", album_name)
    options['albumartist'] = album_name
  else:
    album_name = str(options['album'])
  message = f"Setting Album to \"{album_name}\""
  information_message(message)
  album_name = re.sub(r"\/| |\s+", "_", album_name)
  if options['tracktitle'] is None:
    message = "Determining Track Title"
    information_message(message)
    if len(fields) > 2:
      if re.search(r"[A-Z]|[a-z]", fields[2]):
        track_name = fields[2]
    else:
      if len(fields) > 1:
        if re.search(r"[A-Z]|[a-z]", fields[1]):
          track_name = fields[1]
    track_name = re.sub(r"^-|-$|^\s+|\s+$", "", track_name)
    options['tracktitle'] = track_name
  else:
    track_name = str(options['tracktitle'])
  message = f"Setting Title to \"{track_name}\""
  information_message(message)
  track_name = re.sub(r"\/| |\s+", "_", track_name)
  values = {}
  values['tracknumber']  = track_number
  values['albumartist'] = band_name
  values['album']  = album_name
  values['tracktitle']  = track_name
  file_name  = ""
  valid_keys = [ 'all', 'tracknumber', 'albumartist', 'album', 'tracktitle' ]
  if options['titleorder']:
    string = str(options['titleorder'])
    keys   = string.split(",")
  else:
    keys = [ 'tracknumber', 'albumartist', 'album', 'tracktitle' ]
  for key in keys:
    if re.search("all", options['titlefields']) or re.search(key, str(options['titlefields'])) or re.search(key, str(options['titleorder'])):
        if re.search(key, str(valid_keys)):
          if re.search(r"[A-Z]|[a-z]|[0-9]", values[key]):
            file_name = f"{file_name}-{values[key]}"
  file_name = re.sub(r"^-|-$", "", file_name)
  file_name = f"{file_name}{file_extension}"
  return file_name

# Check directory

def check_directory():
  dir_name  = os.path.dirname(options['file'])
  new_base  = options['albumartist']
  new_album = options['album']
  if new_base is None:
    new_base = options['artist']
  new_base  = re.sub(r"\/| |\s+", "_", str(new_base))
  new_album = re.sub(r"\/| |\s+", "_", str(new_album))
  top_dir   = os.path.dirname(dir_name)
  new_dir   = f"{top_dir}/{new_base}/{new_album}"
  if not os.path.isdir(new_dir):
    message = f"Creating directory {new_dir}"
    information_message(message)
    if options['dryrun'] is False:
      os.makedirs(new_dir)
  return new_dir

# Process file

def process_file():
  update_file = False
  if os.path.exists(options['file']):
    options['file'] = os.path.abspath(options['file'])
    if options['type'] == "flac":
      info = FLAC(options['file'])
    dir_name = os.path.dirname(options['file'])
    items = [ 'album', 'albumartist', 'artist', 'comment', 'composer',
              'discnumber', 'genre', 'lyrics', 'totaldiscs', 'tracktitle',
              'tracknumber', 'totaltracks', 'year' ]
    info = music_tag.load_file(options['file'])
    if options['print']:
      string = f"file:\t\t{options['file']}"
      print(string)
    for key in items:
      if key in info:
        value = info[key]
        if isinstance(value, int):
          value = str(value)
        if options['print']:
          if len(key) < 7:
            string = f"{key}:\t\t{value}"
          else:
            string = f"{key}:\t{value}"
          print(string)
        if options[key] is None:
          if len(value) > 0:
            options[key] = value
        else:
          if options["fix"]:
            message = f"Setting \"{key}\" to \"{options[key]}\'"
            information_message(message)
            if options['dryrun'] is False:
              info[key]   = options[key]
              update_file = True
    if options['check']:
      file_name = build_file_name()
      string = f"newfile:\t{dir_name}/{file_name}"
      if options['print']:
        print(string)
    if options["fix"]:
      if update_file is True:
        if options['dryrun'] is False:
          info.save()
      if options['rename'] is True and options['move'] is False:
        message = f"Renaming {options['file']} to {file_name}"
        information_message(message)
        if options['dryrun'] is False:
          os.rename(options['file'], file_name)
      if options['move'] is True:
        print(str(options['albumartist']))
        new_dir   = check_directory()
        new_name  = f"{new_dir}/{file_name}"
        message   = f"Moving {options['file']} to {new_name}"
        information_message(message)
        if options['dryrun'] is False:
          os.rename(options['file'], new_name)
      if options['updatetags'] is True:
        if options['dryrun'] is False:
          info.save()
  else:
    string = f"File {options['file']} does not exist"
    warning_message(string)

# Get file type

def get_file_type():
  file_type = magic.from_file(options['file'])
  if re.search(r"FLAC", file_type):
    options['type'] = "flac"
  if re.search(r"layer III", file_type):
    options['type'] = "mp3"

# If we have no command line arguments print help

if sys.argv[-1] == sys.argv[0]:
  print_help()
  sys.exit()

# Get command line arguments

parser = argparse.ArgumentParser(prog = "meow", add_help = False)
parser.add_argument('-A', '--albumartist',    help = "Album artist")
parser.add_argument('-a', '--album',          help = "Album title")
parser.add_argument('-b', '--artist',         help = "Tack artist")
parser.add_argument('-C', '--composer',       help = "Track composer")
parser.add_argument('-c', '--compilation',    help = "Compilation")
parser.add_argument('-f', '--file',           help = "Process file" )
parser.add_argument('-D', '--comment',        help = "Track comment")
parser.add_argument('-d', '--dir',            help = "Process directory")
parser.add_argument('-F', '--fix',            help = "Fix file information",    action = 'store_true')
parser.add_argument('-g', '--genre',          help = "Genre")
parser.add_argument("-h", "--help",           help = "Display help",            action = "store_true")
parser.add_argument('-I', '--isrc',           help = "International Standard Recording Code")
parser.add_argument('-i', '--titlefields',    help = "Fields to include in file name")
parser.add_argument('-l', '--lyrics',         help = "Lyrics")
parser.add_argument('-M', '--rename',         help = "Rename file(s)",          action = 'store_true')
parser.add_argument('-m', '--move',           help = "Move file(s)",            action = 'store_true')
parser.add_argument('-N', '--totaltracks',    help = "Total tracks")
parser.add_argument('-n', '--tracknumber',    help = "Track number")
parser.add_argument('-o', '--titleorder',     help = "Order of fields to include in file name")
parser.add_argument('-p', '--print',          help = "Print file information",  action = 'store_true')
parser.add_argument('-R', '--totaldiscs',     help = "Total discs")
parser.add_argument('-r', '--disc',           help = "Disk number")
parser.add_argument('-T', '--tracktitle',     help = "Track title")
parser.add_argument('-t', '--type',           help = "File type")
parser.add_argument("-U", "--updatetags",     help = "Update tags",             action = "store_true")
parser.add_argument("-V", "--version",        help = "Display version",         action = "store_true")
parser.add_argument("-v", "--verbose",        help = "Verbose mode",            action = "store_true")
parser.add_argument('-Y', '--year',           help = "Year")
parser.add_argument('-Z', '--dryrun',         help = "Run in dry run mode",     action = 'store_true')
parser.add_argument('-z', '--check',          help = "Check file information",  action = 'store_true')

options = vars(parser.parse_args())

# Handle help

if options['help']:
  #print_help(script_exe)
  parser.print_help()
  sys.exit()

# Handle dryrun

if options['dryrun']:
  information_message("Runing in dryrun mode")

# Handle verbose

if options['verbose']:
  information_message("Runing in verbose mode")

# Handle title

if not options['titlefields']:
  options['titlefields'] = "all"

# Handle version switch

if options['version'] is True:
  print_version()

# Handle file / dir switch

if not options['file'] and not options['dir']:
  print("No file or directory specified")

if not options['print'] and not options['fix']:
  options['print'] = True

# Handle file switch

if options['file']:
  options['counter'] = 1
  if os.path.exists(options['file']):
    if TinyTag.is_supported(options['file']):
      get_file_type()
      process_file()
  else:
    warning_message(f"File \"{options['file']}\" does not exist")
  sys.exit()

# Handle dirextory switch

if options['dir']:
  copy = options.copy()
  if os.path.exists(options['dir']):
    files = list(Path(options['dir']).rglob("*"))
    for file in files:
      if os.path.isdir(file) is True:
        options['counter'] = 1
      if os.path.isfile(file) is True:
        if TinyTag.is_supported(file):
          options['file'] = file
          get_file_type()
          process_file()
          options['counter'] = options['counter'] + 1
          options = copy.copy()
  else:
    warning_message(f"Directory \"{options['dir']}\" does not exist")
