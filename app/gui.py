# This file is called if no command line arguments are provided
# A GUI interface is created that interacts with the code, replacing the app.py file

from Tkinter import *

import util


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title(util.app_name)
        self.init_widgets()
        self.center_on_screen()
        self.raise_and_focus()
        self.root.mainloop()

    def init_widgets(self):
        pass

    def raise_and_focus(self):
        self.root.call('wm', 'attributes', '.', '-topmost', '1')
        # if platform.system() == 'Darwin':
        #     os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def center_on_screen(self):
        self.root.geometry("+%d+%d" % (
            (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2,
            (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 3
        ))
        self.root.deiconify()