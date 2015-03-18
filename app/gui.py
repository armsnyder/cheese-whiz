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
import transformations
import style_fusions


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
        threading.Thread(target=self.start_timer, args=[3, 1]).start()
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

    def start_timer(self, seconds, code):
        """
        Waits for a specified number of seconds. Meant to be run asynchronously.
        """
        time.sleep(seconds)
        self.queue.put(code)

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
        self.center_on_screen()
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

    def display_recipe_state(self, recipe=None):
        """
        Loads the main interface, which shows the recipe and options for transformation
        """

        # TODO: Build recipe GUI (probably going to be another class)
        # TODO: Run recipe parser from this function and populate the recipe GUI with info
        # TODO: Build transform buttons and link them to functions

        self.current_window = 'recipe'
        self.init_main_window()
        self.fullscreen()
        self.main_window.pack_configure(padx=50, pady=10)
        if not recipe:
            recipe = parser.url_to_recipe(self.recipe_url, self.knowledge_base)
        title = ttk.Label(self.main_window, text=recipe.title)
        title.grid(row=0, column=0, columnspan=2)
        recipe_frame = ttk.Frame(self.main_window)
        for ingredient in recipe.ingredients:
            IngredientWidget(recipe_frame, ingredient).pack()

        for step in reversed(recipe.steps):
            StepWidget(recipe_frame, step).pack(side=Tkinter.BOTTOM, pady=10)

        recipe_frame.grid(column=0, row=1, rowspan=7)

        more_healthy_button = ttk.Button(self.main_window, text="More Healthy",
                                         command=lambda: self.display_recipe_state(
                                             transformations.make_healthy(
                                                 recipe, self.knowledge_base)))
        more_healthy_button.config(width=15)
        more_healthy_button.grid(column=2, row=1)
        less_healthy_button = ttk.Button(self.main_window, text="Less Healthy",
                                         command=lambda: self.display_recipe_state(
                                             transformations.make_unhealthy(
                                                 recipe, self.knowledge_base)))
        less_healthy_button.config(width=15)
        less_healthy_button.grid(column=2, row=2)
        vegetarian_button = ttk.Button(self.main_window, text="Vegetarian",
                                       command=lambda: self.display_recipe_state(
                                           transformations.to_vegetarian(
                                               self.knowledge_base, recipe)))
        vegetarian_button.config(width=15)
        vegetarian_button.grid(column=2, row=3)
        vegan_button = ttk.Button(self.main_window, text="Vegan",
                                  command=lambda: self.display_recipe_state(
                                      transformations.to_vegan(
                                          self.knowledge_base, recipe)))
        vegan_button.config(width=15)
        vegan_button.grid(column=2, row=4)
        more_mexican_button = ttk.Button(self.main_window, text="More Mexican",
                                         command=lambda: self.display_recipe_state(
                                             style_fusions.recipe_fusion(
                                                 recipe, 'mexican', self.knowledge_base)))
        more_mexican_button.config(width=15)
        more_mexican_button.grid(column=2, row=5)
        more_asian_button = ttk.Button(self.main_window, text="More Asian",
                                       command=lambda: self.display_recipe_state(
                                           style_fusions.recipe_fusion(
                                               recipe, 'asian', self.knowledge_base)))
        more_asian_button.config(width=15)
        more_asian_button.grid(column=2, row=6)
        more_italian = ttk.Button(self.main_window, text="More Italian",
                                  command=lambda: self.display_recipe_state(
                                      style_fusions.recipe_fusion(
                                          recipe, 'italian', self.knowledge_base)))
        more_italian.config(width=15)
        more_italian.grid(column=2, row=7)
        next_recipe_button = ttk.Button(self.main_window, text="Next Recipe", command=self.next_recipe)
        next_recipe_button.config(width=15)
        next_recipe_button.grid(column=1, row=8, columnspan=2)

        self.center_on_screen()

    def next_recipe(self):
        self.url_state()
        pass

    def to_veg(self, recipe, knowledge_base):
        self.display_recipe_state(transformations.to_vegetarian(knowledge_base, recipe))

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

    def fullscreen(self):
        w, h = self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()
        self.parent.overrideredirect(1)
        self.parent.geometry("%dx%d+0+0" % (w, h))


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


class IngredientWidget(ttk.Frame):
    def __init__(self, parent, ingredient):
        ttk.Frame.__init__(self, parent)
        self.ingredient = ingredient
        self.init_widgets()

    def init_widgets(self):
        strip_none_list = []
        ok = True
        new_amount = int(self.ingredient.quantity.amount)
        if new_amount == self.ingredient.quantity.amount:
            new_amount = str(new_amount)
        else:
            new_amount = '%.1f' % self.ingredient.quantity.amount
        for t in [
                    new_amount,
                    self.ingredient.quantity.unit,
                    self.ingredient.name,
                    self.ingredient.descriptor,
                    self.ingredient.preparation,
                    self.ingredient.prep_description,
                    ]:
            if t == 'none':
                strip_none_list.append('')
            elif t == 'unknown':
                ok = False
                util.warning('Skipping unknown ingredient in GUI')
                break
            else:
                strip_none_list.append(t+' ')
        if not ok:
            return
        quantity = ttk.Label(self, text=strip_none_list[0])
        unit = ttk.Label(self, text=strip_none_list[1])
        name = ttk.Label(self, text=strip_none_list[2])
        descriptor = ttk.Label(self, text=strip_none_list[3])
        preparation = ttk.Label(self, text=strip_none_list[4])
        prep_description = ttk.Label(self, text=strip_none_list[5])
        unavailable_button = ttk.Button(self, text="X", command=self.do_not_have)

        quantity.pack(side=Tkinter.LEFT)
        unit.pack(side=Tkinter.LEFT)
        prep_description.pack(side=Tkinter.LEFT)
        preparation.pack(side=Tkinter.LEFT)
        descriptor.pack(side=Tkinter.LEFT)
        name.pack(side=Tkinter.LEFT)
        unavailable_button.pack(side=Tkinter.LEFT)

    def do_not_have(self):
        pass


class StepWidget(ttk.Frame):
    def __init__(self, parent, step):
        ttk.Frame.__init__(self, parent)
        self.step = step
        self.init_widgets()

    def init_widgets(self):
        step = ttk.Label(self, text=self.step, wraplength=400)
        step.pack()


def main():
    root = Tkinter.Tk()
    GUI(root)
    root.mainloop()
