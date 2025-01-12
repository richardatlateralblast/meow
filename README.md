![alt tag](meow.gif)

meow
====

MP3/FLAC tag Editor Organiser Writer

Information
===========

A script to print, check, or update MP3/4/A tags and file names.

If information is missing from the file or tags, it will try to fix the data or file name based on what information is available

Version
=======

Current version 0.2.1

Requirements
============

Required standard python modules:

- argparse
- datetime
- pathlib
- sys
- os
- re

Required additional python modules:

- music_tag
- tinytag
- mutagen
- magic


Usage
=====

```
usage: meow [-A ALBUMARTIST] [-a ALBUM] [-b ARTIST] [-C COMPOSER] [-c COMPILATION] [-f FILE] [-D COMMENT] [-d DIR] [-F] [-g GENRE]
            [-h] [-I ISRC] [-i TITLEFIELDS] [-l LYRICS] [-M] [-m] [-N TOTALTRACKS] [-n TRACKNUMBER] [-o TITLEORDER] [-p]
            [-R TOTALDISCS] [-r DISC] [-T TRACKTITLE] [-t TYPE] [-U] [-V] [-v] [-Y YEAR] [-Z] [-z]

options:
  -A ALBUMARTIST, --albumartist ALBUMARTIST
                        Album artist
  -a ALBUM, --album ALBUM
                        Album title
  -b ARTIST, --artist ARTIST
                        Tack artist
  -C COMPOSER, --composer COMPOSER
                        Track composer
  -c COMPILATION, --compilation COMPILATION
                        Compilation
  -f FILE, --file FILE  Process file
  -D COMMENT, --comment COMMENT
                        Track comment
  -d DIR, --dir DIR     Process directory
  -F, --fix             Fix file information
  -g GENRE, --genre GENRE
                        Genre
  -h, --help            Display help
  -I ISRC, --isrc ISRC  International Standard Recording Code
  -i TITLEFIELDS, --titlefields TITLEFIELDS
                        Fields to include in file name
  -l LYRICS, --lyrics LYRICS
                        Lyrics
  -M, --rename          Rename file(s)
  -m, --move            Move file(s)
  -N TOTALTRACKS, --totaltracks TOTALTRACKS
                        Total tracks
  -n TRACKNUMBER, --tracknumber TRACKNUMBER
                        Track number
  -o TITLEORDER, --titleorder TITLEORDER
                        Order of fields to include in file name
  -p, --print           Print file information
  -R TOTALDISCS, --totaldiscs TOTALDISCS
                        Total discs
  -r DISC, --disc DISC  Disk number
  -T TRACKTITLE, --tracktitle TRACKTITLE
                        Track title
  -t TYPE, --type TYPE  File type
  -U, --updatetags      Update tags
  -V, --version         Display version
  -v, --verbose         Verbose mode
  -Y YEAR, --year YEAR  Year
  -Z, --dryrun          Run in dry run mode
  -z, --check           Check file information
```

Examples
========

Print file tags:

```
./meow.py --print --file ./test.mp3
file: ./test.mp3
album: Back In Black
albumartist:
artist: AC/DC
comment:
compilation:
composer:
discnumber:
genre: Hard Rock
lyrics:
totaldiscs:
totaltracks: 10
tracknumber: 1
tracktitle: Hells Bells
year: 2003
isrc:
```

Update cooment tag:

```
./meow.py --fix --file ./test.mp3 --comment "Remaster"
```

Rename file name based on tags (additionally run in dryrun mode with verbose output):

```
./meow.py --fix --dryrun --file ./test.mp3 --check --rename --verbose
Information:    Runing in dryrun mode
Information:    Runing in verbose mode
Information:    Renaming ./test.mp3 to 01-AC_DC-Back_In_Black-Hells_Bells.mp3
```


License
=======

This software is licensed as CC-BA (Creative Commons By Attrbution)

http://creativecommons.org/licenses/by/4.0/legalcode
