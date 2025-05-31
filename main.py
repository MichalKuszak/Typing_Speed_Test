import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import time
import threading
import random
import pandas as pd


FUNC_KEYS = [64, 113, 22, 110, 66, 37, 109, 107, 104, 103, 9, 111, 67, 68, 96, 97, 106, 100, 54, 90, 87, 88, 89, 83,
             84, 85, 79, 80, 81, 86, 84, 91, 91, 112, 88, 87, 108, 79, 90, 83, 63, 89, 81, 85, 82, 80, 105, 77, 110,
             111, 99, 36, 102, 78, 50, 62, 23, 98]




def load_words():
    try:
        with open("./assets/words.txt", mode="r") as file:
            return file.readlines()
    except FileNotFoundError:
        print("words.txt file not found!")
        exit()

def load_highscores(self):
    raise NotImplementedError("Function not implemented!")
    try:
        df = pd.read_csv('assets/scores.csv')


    except FileNotFoundError:
        df = {}





def word_picker(k=10) -> str:
    words_list = [word.strip() for word in random.sample(load_words(), k)]
    return " ".join(words_list)

class GUI(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(600, 600)
        self.style = Style()
        self.style.theme_use("litera")
        self.main = Main(self)
        self.main.pack(expand=True)

class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        for _ in range(0, 6):
            self.rowconfigure(_, weight=1)
        self.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self, text="Test your typing speed", font=("Futura", 24, "bold"), justify="left")
        self.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="wn")

        self.description_label = ttk.Label(self, text="Start typing to begin the test.\n"
                                                      "Type the ten words shown below - without mistakes.\n",
                                           font=("Futura", 18, "italic"), justify="left")
        self.description_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="wn")


        self.test_text_label = ttk.Label(self, text=word_picker(), font=("Futura", 20), relief="sunken")
        self.test_text_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.entry_var = ttk.StringVar()
        self.user_entry = ttk.Entry(self, width=40, font=("Futura", 24), textvariable=self.entry_var)
        self.user_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        self.user_entry.focus_set()

        self.info_label = ttk.Label(self, text="Your typing speed: \n0.00 CPS\t\t0.00 WPS\n"
                                               "0.00 CPM\t\t0.00 WPM", font=("Futura", 20))
        self.info_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.reset_button = ttk.Button(self, text="Reset", bootstyle='warning')
        self.reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


class App(GUI):
    def __init__(self, title, size):
        super().__init__(title, size)
        self.counter = 0
        self.running = False
        self.main.user_entry.bind("<KeyRelease>", self.start)
        self.main.reset_button.configure(command=self.reset)

    def start(self, event):
        if not self.running:
            if not event.keycode in FUNC_KEYS:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.main.test_text_label.cget('text').startswith(self.main.entry_var.get()):
            self.main.user_entry.config(foreground='red')
        else:
            self.main.user_entry.config(foreground='black')
        if self.main.entry_var.get() == self.main.test_text_label.cget('text'):
            self.running = False
            self.main.user_entry.config(foreground='green')


    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            chars_per_second = len(self.main.entry_var.get()) / self.counter
            chars_per_minute = chars_per_second * 60
            words_per_second = len(self.main.entry_var.get().split(" ")) / self.counter
            words_per_minute = words_per_second * 60
            self.main.info_label.config(text=f"Your typing speed: \n{chars_per_second:.2f} CPS\t\t{words_per_second:.2f}WPS\n"
                                               f"{chars_per_minute:.2f} CPM\t\t{words_per_minute:.2f} WPM")

    def reset(self):
        self.running = False
        self.counter = 0
        self.main.info_label.config(text="Your typing speed: \n0.00 CPS\t\t0.00 WPS\n"
                                               "0.00 CPM\t\t0.00 WPM")
        self.main.test_text_label.config(text=word_picker())
        self.main.user_entry.delete(0, tk.END)






if __name__ == "__main__":
    app = App("Typing Speed Test", (600, 600))
    app.mainloop()



