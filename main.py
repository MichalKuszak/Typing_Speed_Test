import time
import tkinter as tk
from ensurepip import bootstrap
from time import sleep

import requests
import random
import ttkbootstrap as ttk
from ttkbootstrap import Style
from tkinter import messagebox, StringVar

time_left = 0

try:
    with open("./assets/words.txt", mode="r") as file:
        WORDS = file.readlines()
except FileNotFoundError:
    with open("./assets/words.txt", mode="w") as file:
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        WORDS = response.text.splitlines()
        for item in WORDS:
            file.write(f"{item}\n")

def word_picker() -> list[str]:
    test_list = [word for word in random.choices(WORDS, k=200)]
    return test_list

# TODO Create a GUI
# Timer
# Current word
# Next word
# Current word counter
# Start/stop buttons
# Best score?
# User input field

class GUI(tk.Tk):
    def __init__(self, title: str, size: tuple[int, int]) -> None:
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.style = Style()
        self.style.theme_use("litera")
        self.config(padx=20, pady=20)

        self.main = Main(self)

    # def countdown(self):
    #     global time_left
    #     if time_left > 0:
    #         secs = divmod(time_left, 60)
    #         self.main.timer.time_left_label.config(text=f"{secs:02d}")
    #         time_left -= 1
    #         self.after(1000, func=self.countdown)
    #     else:
    #         messagebox.showinfo("Time's up!")


class Main(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.create_widgets()
        self.layout_widgets()

        self.pack(fill="both", expand=True)

    def create_widgets(self):
        self.title_frame = ttk.Frame(self)
        self.title_label = TitleLabel(self.title_frame)

        self.timer_frame = ttk.Frame(self)
        self.timer = TimerControls(self.timer_frame)

        self.score_frame = ttk.Frame(self)
        self.current_score_words = CurrentScore(self.score_frame, "Current WPM")
        self.current_score_chars = CurrentScore(self.score_frame, "Current CPM")

        self.word_frame = ttk.Frame(self)
        self.current_word = CurrentWord(self.word_frame)

        self.listbox_frame = ttk.Frame(self)
        self.listbox = ListBox(self.listbox_frame)

        self.entry_frame = ttk.Frame(self)
        self.user_entry = UserEntry(self.entry_frame)

    def layout_widgets(self):
        self.title_label.pack()
        self.title_frame.pack()

        self.timer.pack()
        self.timer_frame.pack()

        self.current_score_words.pack()
        self.current_score_chars.pack()
        self.score_frame.pack()

        self.current_word.pack()
        self.word_frame.pack()

        self.listbox.pack(expand=True, fill="both")
        self.listbox_frame.pack(expand=True, fill="x")

        self.user_entry.pack(expand=True, fill="x")
        self.entry_frame.pack(expand=True, fill="x")


        # self.layout_widgets()

class TitleLabel(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.title_label = ttk.Label(text="Typing Speed Test", font=('Futura', 20))

    def layout_widgets(self) -> None:
        self.title_label.pack()

class TimerControls(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.parent = parent
        self.time_left = 0
        self.timer_id = None
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.start_button = ttk.Button(self, text='START', style="success")
        self.time_left_var = tk.IntVar()
        self.time_left_var.set(60)
        self.time_left_label = ttk.Label(self,
                                   text="5",
                                   font=("Futura", 16),
                                   width=5,
                                   justify="center",
                                   anchor="center",
                                   relief="groove",
                                   textvariable=self.time_left_var)
        self.stop_button = ttk.Button(self, text='STOP', style="danger")

    def layout_widgets(self) -> None:
        self.start_button.pack(side="left", padx=10, pady=10)
        self.time_left_label.pack(side="left", padx=10, pady=10)
        self.stop_button.pack(side="left", padx=10, pady=10)

class CurrentScore(ttk.Frame):
    def __init__(self, parent: tk.Misc, label_title: str) -> None:
        super().__init__(parent)
        self.title = label_title
        self.score_var = StringVar()
        self.score_var.set("0")
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.current_score_label = ttk.Label(self, text=self.title, font=("Futura", 16))
        self.current_score_val = ttk.Label(self,
                                           textvariable=self.score_var,
                                           font=("Futura", 16),
                                           width=5,
                                           justify="center",
                                           anchor="center",
                                           relief="groove") # Fetched from DB

    def layout_widgets(self) -> None:
        self.current_score_label.pack(side="left", anchor="center", padx=10, pady=5)
        self.current_score_val.pack(side="right", anchor="center", padx=10, pady=5)

class CurrentWord(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.current_word_var = StringVar()
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.current_word_label = ttk.Label(self,
                                            text="#####",
                                            font=("Futura", 20),
                                            background="white",
                                            foreground="black",
                                            borderwidth=2,
                                            width=20,
                                            anchor="center",
                                            relief="groove",
                                            textvariable=self.current_word_var,
                                            state="disabled")

    def layout_widgets(self) -> None:
        self.current_word_label.pack(padx=10, pady=10)

class ListBox(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.listbox_var = StringVar()
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.listbox_label = ttk.Label(self,
                                       text="Next words: ",
                                       font=("Futura", 18),
                                       justify="left"
                                       )
        self.listbox = tk.Listbox(self,
                                  font=("Futura", 18),
                                  width=560,
                                  height=10,
                                  justify="center",
                                  listvariable=self.listbox_var,
                                  state="disabled"
                                  )

    def layout_widgets(self) -> None:
        self.listbox_label.pack(anchor="nw", padx=10, pady=5)
        self.listbox.pack(padx=10, pady=5)

class UserEntry(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.user_entry_var = StringVar()
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.user_entry_box = ttk.Entry(self,
                                        font=("Futura", 20),
                                        justify="center",
                                        textvariable=self.user_entry_var,
                                        state="disabled")

    def layout_widgets(self) -> None:
        self.user_entry_box.pack(padx=10, pady=10)


class App(GUI):
    def __init__(self, title: str, size: tuple[int, int]):
        super().__init__(title=title, size=size)
        self.words_counter = 0
        self.chars_counter = 0
        self.user_input = self.main.user_entry.user_entry_var # get value on space or enter click
        self.list_of_words = None
        self.current_word_label = self.main.current_word.current_word_var

        self.time_left = self.main.timer.time_left_var
        self.main.timer.start_button.config(command=self.start_test)

        for key in ["<Return>", "<space>"]: self.bind(key, self.check_user_input)


    def update_current_word(self):
        self.current_word = self.list_of_words[0]
        self.current_word_label.set(f"{self.current_word.strip().upper()}")
        self.list_of_words.remove(self.current_word)
        self.main.listbox.listbox_var.set(self.list_of_words)

    def check_user_input(self, event):
        user_string = self.user_input.get().lower()
        current_word = self.current_word_label.get().lower()
        current_words_score = self.main.current_score_words.score_var
        current_chars_score = self.main.current_score_chars.score_var
        if user_string.strip() == current_word:
            self.words_counter += 1
            self.chars_counter += len(current_word)
        self.update_current_word()
        self.user_input.set("")
        current_words_score.set(f"{self.words_counter}")
        current_chars_score.set(f"{self.chars_counter}")

    def countdown(self):
        timer = self.time_left.get()
        if timer > 0:
            timer -= 1
            self.time_left.set(timer)
            self.after(1000, self.countdown)
            return True
        else:
            self.time_left.set(timer)
            timer = 0
            return False

    def reset_timer(self):
        raise NotImplementedError

    def start_test(self):
        self.main.user_entry.user_entry_box.config(state="normal",
                                                   takefocus=True)

        self.list_of_words = word_picker()
        # current word
        self.main.current_word.current_word_label.config(state="normal")
        # listbox
        self.main.listbox.listbox.config(state="normal")
        self.main.listbox.listbox_var.set(self.list_of_words)

        self.update_current_word()
        self.main.current_word.current_word_label.config(state="disabled")
        self.main.listbox.listbox.config(state="disabled")

        self.main.user_entry.user_entry_box.focus_set()

        while not self.countdown():
            self.check_user_input()






# TODO Create countdown timer logic




if __name__ == "__main__":
    app = App("Typing Speed Test", (400, 600))
#
    app.mainloop()

