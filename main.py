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


def word_picker(k=10) -> str:
    words_list = [word.strip() for word in random.sample(load_words(), k)]
    return " ".join(words_list)

class GUI(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.width = size[0]
        self.height = size[1]
        self.title(title)
        self.center_window()
        self.minsize(600, 600)
        self.diameter = size
        self.style = Style()
        self.style.theme_use("litera")
        self.main = Main(self)
        self.main.pack(expand=True, fill="y")

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.highscore_label = ttk.Label(self, font=("Futura", 14, "bold"))
        self.highscore_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")

        self.title_label = ttk.Label(self, text="Test your typing speed", font=("Futura", 24, "bold"), justify="left")
        self.title_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="wn")

        self.description_label = ttk.Label(self, text="Start typing to begin the test.\n"
                                                      "Type the ten words shown below - without mistakes.\n",
                                           font=("Futura", 18, "italic"), justify="left")
        self.description_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="wn")

        self.test_text_label = ttk.Label(self, text=word_picker(), font=("Futura", 20), relief="sunken")
        self.test_text_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.entry_var = ttk.StringVar()
        self.user_entry = ttk.Entry(self, width=40, font=("Futura", 24), textvariable=self.entry_var)
        self.user_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        self.user_entry.focus_set()

        self.info_label = ttk.Label(self, text="Your typing speed:", font=("Futura", 20), justify="center")
        self.info_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.cps_label = ttk.Label(self, text="0.00 Characters/second", font=("Futura", 20), justify="right")
        self.cps_label.grid(row=6, column=0, columnspan=1, padx=5, pady=5, sticky="news")
        self.cpm_label = ttk.Label(self, text="0.00 Characters/minute", font=("Futura", 20), justify="right")
        self.cpm_label.grid(row=6, column=1, columnspan=1, padx=5, pady=5, sticky="news")
        self.wps_label = ttk.Label(self, text="0.00 Words/second", font=("Futura", 20), justify="right")
        self.wps_label.grid(row=7, column=0, columnspan=1, padx=5, pady=5, sticky="news")
        self.wpm_label = ttk.Label(self, text="0.00 Words/minute", font=("Futura", 20), justify="right")
        self.wpm_label.grid(row=7, column=1, columnspan=1, padx=5, pady=5, sticky="news")

        self.reset_button = ttk.Button(self, text="Reset", bootstyle='warning', width=20)
        self.reset_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

        self.final_score_label = ttk.Label(self, font=("Futura", 14, "bold"))
        self.final_score_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="n")



class App(GUI):
    def __init__(self, title, size):
        super().__init__(title, size)
        self.counter = 0
        self.running = False

        self.highscore_cps = 0.00
        self.highscore_cpm = 0.00
        self.highscore_wps = 0.00
        self.highscore_wpm = 0.00
        self.highscores = None
        self.load_highscores()

        self.main.highscore_label.config(
            text=f"Your highscore: {self.highscore_cpm} CPM ({self.highscore_cps} CPS)\t{self.highscore_wpm} WPM ({self.highscore_wps} WPS)")
        self.main.user_entry.bind("<KeyRelease>", self.start)
        self.main.reset_button.configure(command=self.reset)

        self.update_idletasks()

    def load_highscores(self):
        try:
            self.highscores = pd.read_csv('assets/scores.csv')
            self.highscore_cps = self.highscores.loc[0, "HIGHSCORE_CPS"]
            self.highscore_cpm = self.highscores.loc[0, "HIGHSCORE_CPM"]
            self.highscore_wps = self.highscores.loc[0, "HIGHSCORE_WPS"]
            self.highscore_wpm = self.highscores.loc[0, "HIGHSCORE_WPM"]
        except FileNotFoundError:
            self.highscores = pd.DataFrame(data={
                "HIGHSCORE_CPS": self.highscore_cps,
                "HIGHSCORE_CPM": self.highscore_cpm,
                "HIGHSCORE_WPS": self.highscore_wps,
                "HIGHSCORE_WPM": self.highscore_wpm
            },
                index=[0])

    def start(self, event):
        if not self.running:
            if event.keycode not in FUNC_KEYS:
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
            self.check_for_highscore()


    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            chars_per_second = len(self.main.entry_var.get()) / self.counter
            chars_per_minute = chars_per_second * 60
            words_per_second = len(self.main.entry_var.get().split(" ")) / self.counter
            words_per_minute = words_per_second * 60
            self.main.cps_label.config(text=f"{chars_per_second:.2f} Characters/second")
            self.main.cpm_label.config(text=f"{chars_per_minute:.2f} Characters/minute")
            self.main.wps_label.config(text=f"{words_per_second:.2f} Words/second")
            self.main.wpm_label.config(text=f"{words_per_minute:.2f} Words/minute")



    def reset(self):
        self.running = False
        self.counter = 0
        self.main.highscore_label.config(
            text=f"Your highscore: {self.highscore_cpm} CPM ({self.highscore_cps} CPS)\t{self.highscore_wpm} WPM ({self.highscore_wps} WPS)",
            foreground="black")
        self.main.cps_label.config(text=f"0.00 Characters/second")
        self.main.cpm_label.config(text=f"0.00 Characters/minute")
        self.main.wps_label.config(text=f"0.00 Words/second")
        self.main.wpm_label.config(text=f"0.00 Words/minute")
        self.main.test_text_label.config(text=word_picker())
        self.main.final_score_label.config(text="")
        self.main.user_entry.delete(0, tk.END)
        self.main.user_entry.focus_set()

    def check_for_highscore(self):
        last_cps_score = float(self.main.cps_label.cget("text").split(" ")[0])
        last_cpm_score = float(self.main.cpm_label.cget("text").split(" ")[0])
        last_wps_score = float(self.main.wps_label.cget("text").split(" ")[0])
        last_wpm_score = float(self.main.wpm_label.cget("text").split(" ")[0])

        chars_is_new_highscore = False
        words_is_new_highscore = False

        if last_cps_score > self.highscore_cps:
            self.highscore_cps = last_cps_score
            self.highscores.loc[0, "HIGHSCORE_CPS"] = self.highscore_cps
            self.highscore_cpm = last_cpm_score
            self.highscores.loc[0, "HIGHSCORE_CPM"] = self.highscore_cpm
            chars_is_new_highscore = True

        if last_wps_score > self.highscore_wps:
            self.highscore_wps = last_wps_score
            self.highscores.loc[0, "HIGHSCORE_WPS"] = self.highscore_wps
            self.highscore_wpm = last_wpm_score
            self.highscores.loc[0, "HIGHSCORE_WPM"] = self.highscore_wpm
            words_is_new_highscore = True

        if chars_is_new_highscore and words_is_new_highscore:
            self.main.final_score_label.config(text=f"You finished the test with the following scores:\n"
                                     f"{last_cpm_score} CPM ({last_cps_score} CPS), "
                                          f"{last_wpm_score} WPM ({last_wps_score} WPS)\n"
                                          f"You've beaten both your CPS/CPM AND WPS/WPM highscores! Now that's a combo!",
                                             foreground="orange")
        elif chars_is_new_highscore and not words_is_new_highscore:
            self.main.final_score_label.config(text=f"You finished the test with the following scores:\n"
                                          f"{last_cpm_score} CPM ({last_cps_score} CPS), "
                                          f"{last_wpm_score} WPM ({last_wps_score} WPS)\n"
                                          f"You've beaten your CPS/CPM highscore! Congratulations!",
                                             foreground="orange")
        elif words_is_new_highscore and not chars_is_new_highscore:
            self.main.final_score_label.config(text=f"You finished the test with the following scores:\n"
                                          f"{last_cpm_score} CPM ({last_cps_score} CPS), "
                                          f"{last_wpm_score} WPM ({last_wps_score} WPS)\n"
                                          f"You've beaten your WPS/WPM highscore! Nicely done!",
                                             foreground="orange")
        else:
            self.main.final_score_label.config(text=f"You finished the test with the following scores:\n"
                                          f"{last_cpm_score} CPM ({last_cps_score} CPS), "
                                          f"{last_wpm_score} WPM ({last_wps_score} WPS)",
                                             foreground="orange")
        self.highscores.to_csv('assets/scores.csv')


if __name__ == "__main__":
    app = App("Typing Speed Test", (700, 500))
    app.mainloop()



