# The launcher for our application. It's simple for now, but later we can layer on a GUI and such.
#
# CHEESE WHIZ
# A recipe transformer
#
# by Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder
# Northwestern University
# EECS 337
# Professor Lawrence Birnbaum
# March 2015

import sys

import app.app
import app.gui

__author__ = "Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder"
__credits__ = ["Kristen Amaddio", "Neal Kfoury", "Michael Nowakowski", "Adam Snyder"]
__status__ = "Development"

if len(sys.argv) > 1:
    app.app.main()
else:
    app.gui.GUI()