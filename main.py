import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import requests

# TODO Get word list

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()

# TODO Create a GUI
# Timer
# Current word
# Next word
# Current word counter
# Start/stop buttons
# Best score?
# User input field

class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("600x800")




# TODO Create countdown timer logic

# TODO Generate a list of 200 random words

# TODO Create logic for displaying current and next word

# TODO Create a logic for checking if the user typing is correct. Treat space as submit


if __name__ == "__main__":
    app = GUI()

    app.mainloop()
