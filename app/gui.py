# This file is called if no command line arguments are provided
# A GUI interface is created that interacts with the code, replacing the app.py file

import Tkinter
import ttk
import platform
import subprocess
import threading
import Queue
import time

import util
import app
import parser


class GUI(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title(util.app_name)
        self.current_window = None

        # Setting up basic GUI frames
        self.main_window = ttk.Frame()
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self.pack(fill=Tkinter.BOTH, expand=True)

        # Loading initial widgets
        self.splash_state()

        # Formatting window
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.raise_and_focus()

        # Knowledge base loading
        self.queue = Queue.Queue()
        self.knowledge_base = None
        self.recipe_url = None
        self.status_bar.set('Loading knowledge base in background...')
        threading.Thread(target=self.load_kb_for_gui).start()
        threading.Thread(target=self.start_splash_timer, args=[3]).start()
        self.periodic_dequeue()

    def periodic_dequeue(self):
        """
        Periodically checks for incoming asynchronous content so that the GUI will not freeze
        """
        while self.queue.qsize():
            try:
                function = self.queue.get(0)
                if function == 1:
                    self.url_state()
                elif function == 2 and self.current_window == 'load_kb':
                    self.display_recipe_state()
            except Queue.Empty:
                pass
        self.parent.after(100, self.periodic_dequeue)

    def init_main_window(self):
        """
        Resets the main window so that it can be refilled with a new interface
        """
        self.main_window.destroy()
        self.main_window = ttk.Frame(self)
        self.main_window.pack(fill=Tkinter.BOTH, expand=True)

    def load_kb_for_gui(self):
        """
        Loads the knowledge base. Meant to be run asynchronously.
        """
        self.knowledge_base = app.load_knowledge_base()
        self.status_bar.set('Finished loading knowledge base')
        self.queue.put(2)

    def start_splash_timer(self, seconds):
        """
        Waits for a specified number of seconds. Meant to be run asynchronously.
        """
        time.sleep(seconds)
        self.queue.put(1)

    def splash_state(self):
        """
        Loads splash image
        """
        self.current_window = 'splash'
        self.init_main_window()
        splash_image_file = Tkinter.PhotoImage(file=util.relative_path('img/cheese_wiz_splash.gif'))
        splash_image_widget = Tkinter.Label(self.main_window, image=splash_image_file)
        splash_image_widget.photo = splash_image_file
        splash_image_widget.pack()
        self.center_on_screen()

    def url_state(self):
        """
        Loads the widgets for the "Enter URL" interface
        """
        # self.parent.withdraw()
        self.current_window = 'url'
        self.init_main_window()
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(2, pad=10)
        self.main_window.pack_configure(padx=10, pady=10)

        url_label = ttk.Label(self.main_window, text="Enter a recipe URL to begin:")
        url_label.grid(columnspan=3, sticky=Tkinter.W)

        url_text_box = ttk.Entry(self.main_window, width=50)
        url_text_box.grid(row=1, sticky=Tkinter.E+Tkinter.W+Tkinter.S+Tkinter.N)

        ok_button = ttk.Button(self.main_window, text="OK", command=lambda: self.load_kb_state(url_text_box.get()))
        ok_button.grid(row=1, column=2)

        url_text_box.focus()
        self.parent.geometry('604x100')
        # self.center_on_screen()
        # self.parent.deiconify()
        self.update_idletasks()

    def load_kb_state(self, url):
        """
        Loads a blank interface that prompts the user to wait for the knowledge base to finish loading
        """
        self.recipe_url = url
        self.current_window = 'load_kb'
        if not self.knowledge_base:
            self.init_main_window()
            self.main_window.pack_configure(padx=10, pady=10)
            message = ttk.Label(self.main_window, text="Waiting for knowledge base to load...")
            message.pack()
        else:
            self.display_recipe_state()

    def display_recipe_state(self):
        """
        Loads the main interface, which shows the recipe and options for transformation
        """

        # TODO: Build recipe GUI (probably going to be another class)
        # TODO: Run recipe parser from this function and populate the recipe GUI with info
        # TODO: Build transform buttons and link them to functions

        self.current_window = 'recipe'
        self.init_main_window()
        self.parent.geometry('500x800')
        message = ttk.Label(self.main_window, text="(Recipe displays here)")
        message.pack()

        recipe = parser.url_to_dictionary(self.recipe_url)

        self.center_on_screen()

    def raise_and_focus(self):
        # window.lift()
        self.parent.call('wm', 'attributes', '.', '-topmost', '1')
        if platform.system() == 'Darwin':
            try:
                subprocess.call(['/usr/bin/osascript', '-e',
                                 'tell app "System Events" to set frontmost of process "Python" to true'])
            except OSError:
                pass
        self.parent.deiconify()

    def center_on_screen(self):
        self.update_idletasks()
        w = self.parent.winfo_screenwidth()
        h = self.parent.winfo_screenheight()
        rootsize = tuple(int(_) for _ in self.parent.geometry().split('+')[0].split('x'))
        x = (w - rootsize[0]) / 2
        y = (h - rootsize[1]) / 3
        self.parent.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))


class StatusBar(ttk.Frame):
    """
    A custom widget that sits at the bottom of the GUI and displays program status updates
    """

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, relief=Tkinter.SUNKEN, anchor='w')
        self.label.pack(fill=Tkinter.X)

    def set(self, format0, *args):
        self.label.config(text=format0 % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text='')
        self.label.update_idletasks()


def main():
    root = Tkinter.Tk()
    GUI(root)
    root.mainloop()
