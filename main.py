import time
import tkinter as tk
from ensurepip import bootstrap

import requests
import random
import ttkbootstrap as ttk
from ttkbootstrap import Style
from tkinter import  messagebox
# TODO Get word list

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

def word_picker() -> set[str]:
    test_set ={word for word in random.choices(WORDS, k=200)}
    return test_set

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
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.start_button = ttk.Button(self, text='START', style="success")
        self.time_left = ttk.Label(self,
                                   text="60",
                                   font=("Futura", 16),
                                   width=5,
                                   justify="center",
                                   anchor="center",
                                   relief="groove")
        self.stop_button = ttk.Button(self, text='STOP', style="danger")

    def layout_widgets(self) -> None:
        self.start_button.pack(side="left", padx=10, pady=10)
        self.time_left.pack(side="left", padx=10, pady=10)
        self.stop_button.pack(side="left", padx=10, pady=10)

class CurrentScore(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.current_score_label = ttk.Label(self, text="Current WPM:", font=("Futura", 16))
        self.current_score_val = ttk.Label(self,
                                           text="0",
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
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.current_word_label = ttk.Label(self,
                                            text="CURRENT_WORD",
                                            font=("Futura", 20),
                                            background="white",
                                            foreground="black",
                                            borderwidth=2,
                                            relief="groove")

    def layout_widgets(self) -> None:
        self.current_word_label.pack(padx=10, pady=10)

class ListBox(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.words_dict = dict([(idx, val) for idx, val in enumerate(word_picker())])
        print(self.words_dict)
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.listbox_label = ttk.Label(self, text="Next words: ", font=("Futura", 18), justify="left")
        self.listbox = tk.Listbox(self,
                                  font=("Futura", 18),
                                  width=560,
                                  height=10,
                                  justify="center",
                                  )
        for key, value in self.words_dict.items():
            self.listbox.insert(key, value)
        self.listbox.configure(state="disabled")

    def layout_widgets(self) -> None:
        self.listbox_label.pack(anchor="nw", padx=10, pady=5)
        self.listbox.pack(padx=10, pady=5)

class UserEntry(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self) -> None:
        self.user_entry_box = ttk.Entry(self,
                                        takefocus=True,
                                        font=("Futura", 20),
                                        justify="center")

    def layout_widgets(self) -> None:
        self.user_entry_box.pack(padx=10, pady=10)




# TODO Create countdown timer logic
# timer = tk.StringVar()
# timer.set("60")

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
    app = GUI("Typing Speed Test", (400, 600))
#
    app.mainloop()

