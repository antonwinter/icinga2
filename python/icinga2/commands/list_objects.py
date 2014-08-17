# Icinga 2
# Copyright (C) 2012-2014 Icinga Development Team (http://www.icinga.org)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

import os, sys, getopt
from icinga2.utils.debug import ObjectsFileReader
from icinga2.config import LocalStateDir
from signal import signal, SIGPIPE, SIG_DFL

def main():
    signal(SIGPIPE, SIG_DFL)

    color_mode = 'auto'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "color"])
    except getopt.GetoptError:
        t, err = sys.exc_info()[:2]
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "--color":
            color_mode = 'always'
        else:
            assert False, "unhandled option"

    if len(args) > 0:
        fname = args[0]
    else:
        fname = LocalStateDir + "/cache/icinga2/icinga2.debug"

    if color_mode == 'always':
        use_colors = True
    elif color_mode == 'never':
        use_colors = False
    else:
        use_colors = os.isatty(1)

    fp = open(fname)
    ofr = ObjectsFileReader(fp)
    for obj in ofr:
        print obj.format(use_colors)

def usage():
    print "Syntax: %s [--color] [file]" % (sys.argv[0])
    print ""
    print "Displays a list of objects from the specified Icinga 2 objects file."