import time
import tkinter as tk
from ensurepip import bootstrap

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

    def countdown(self):
        global time_left
        if time_left > 0:
            secs = divmod(time_left, 60)
            self.main.timer.time_left_label.config(text=f"{secs:02d}")
            time_left -= 1
            self.after(1000, func=self.countdown)
        else:
            messagebox.showinfo("Time's up!")


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
        self.current_score = CurrentScore(self.score_frame)

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

        self.current_score.pack()
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
        self.time_left_var = StringVar()
        self.time_left_var.set("60")
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
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.score_var = StringVar()
        self.score_var.set("0")
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.current_score_label = ttk.Label(self, text="Current WPM:", font=("Futura", 16))
        self.current_score_val = ttk.Label(self,
                                           textvariable=self.score_var,
                                           font=("Futura", 16),
                                           width=5,
                                           justify="center",
                                           anchor="center",
                                           relief="groove") # Fetched from DB

    def layout_widgets(self) -> None:
        self.current_score_label.pack(side="left", padx=10, pady=10)
        self.current_score_val.pack(side="left", padx=10, pady=10)

class CurrentWord(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.current_word_var = StringVar()
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.current_word_label = ttk.Label(self,
                                            text="CURRENT_WORD",
                                            font=("Futura", 20),
                                            background="white",
                                            foreground="black",
                                            borderwidth=2,
                                            relief="groove",
                                            textvariable=self.current_word_var)

    def layout_widgets(self) -> None:
        self.current_word_label.pack(padx=10, pady=10)

class ListBox(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.list_of_words = word_picker()
        self.listbox_var = StringVar()
        self.listbox_var.set(self.list_of_words)
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.listbox_label = ttk.Label(self, text="Next words: ", font=("Futura", 18), justify="left")
        self.listbox = tk.Listbox(self,
                                  font=("Futura", 18),
                                  width=560,
                                  height=10,
                                  justify="center",
                                  listvariable=self.listbox_var
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
                                        takefocus=True,
                                        font=("Futura", 20),
                                        justify="center",
                                        textvariable=self.user_entry_var)

    def layout_widgets(self) -> None:
        self.user_entry_box.pack(padx=10, pady=10)


class App(GUI):
    def __init__(self, title: str, size: tuple[int, int]):
        super().__init__(title=title, size=size)
        self.counter = 0
        self.user_input = self.main.user_entry.user_entry_var # get value on space or enter click
        self.list_of_words = self.main.listbox.list_of_words
        self.current_word_label = self.main.current_word.current_word_var
        self.update_current_word()
        self.bind("<Return>space", self.check_user_input)
        self.bind("<space>", self.check_user_input)

    def update_current_word(self):
        self.current_word = self.list_of_words[0]
        self.current_word_label.set(f"{self.current_word.strip().upper()}")
        self.list_of_words.remove(self.current_word)
        self.main.listbox.listbox_var.set(self.list_of_words)

    def check_user_input(self, event):
        user_string = self.user_input.get().lower()
        current_word = self.current_word_label.get().lower()
        current_score = self.main.current_score.score_var
        if user_string.strip() == current_word:
            self.counter += 1
        self.update_current_word()
        self.user_input.set("")
        current_score.set(f"{self.counter}")



# TODO Create countdown timer logic


# TODO Generate a list of 200 random words


    # user_mistakes_list = []
    # counter = 0
    # user_score = 0
    # # TODO Create logic for displaying current and next word
    # while True:
    #     print(f"Score: {user_score}\nThe word is: {test_list[counter].upper()}")
    #     user_input = input()
    #     if user_input.lower() == test_list[counter]:
    #         user_score += 1
    #     else:
    #         mistake = test_list.pop(counter)
    #         user_mistakes_list.append(mistake)
    #     counter += 1
    #
    # print(f"You typed the following words wrong: {user_mistakes_list}")
# TODO Create a logic for checking if the user typing is correct. Treat space as submit
#
#
if __name__ == "__main__":
    app = App("Typing Speed Test", (400, 600))
#
    app.mainloop()

