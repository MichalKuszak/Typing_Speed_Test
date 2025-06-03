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


def load_words() -> list[str]:
    """
    Reads a list of words from a file and returns them as a list of strings.

    This function attempts to read the "words.txt" file located in the
    "./assets/" directory. It returns the contents of the file as a list of
    lines, with each line representing a single word. If the file cannot
    be found, a message is printed to the console, and the program
    terminates.

    :return: A list of strings representing the words read from the file.
    :rtype: list[str]
    """
    try:
        with open("./assets/words.txt", mode="r") as file:
            return file.readlines()
    except FileNotFoundError:
        print("words.txt file not found!")
        exit()


def word_picker(k=10) -> str:
    """
    Constructs and returns a string by randomly selecting a specified number of words
    from a loaded list, separating the selected words with spaces.

    :param k: An integer representing the number of words to randomly pick from
        the list. Default value is 10.
    :return: A string composed of randomly selected words joined by spaces.
    """
    words_list = [word.strip() for word in random.sample(load_words(), k)]
    return " ".join(words_list)

class GUI(tk.Tk):
    """
    Represents a graphical user interface (GUI) application window.

    This class provides the main window for a GUI application, initializes
    the window parameters such as title, size, and style, and centers the
    window on the screen upon creation. It incorporates a main widget container
    to house the core application functionality.

    :ivar width: Width of the GUI window in pixels.
    :type width: int
    :ivar height: Height of the GUI window in pixels.
    :type height: int
    :ivar diameter: Dimensions of the GUI window as a tuple (width, height).
    :type diameter: tuple[int, int]
    :ivar style: The ttk Style object responsible for theming the GUI.
    :type style: ttk.Style
    :ivar main: The main widget container for the application content.
    :type main: Main
    """
    def __init__(self, title: str, size: tuple[int, int]):
        """
        A class constructor for initializing a graphical user interface. The
        class sets various properties such as window dimensions, title, and
        minimum size. Additionally, it applies a theme using the built-in
        Style class, and initializes and packs a main widget.

        :param title: The title of the window
        :type title: str
        :param size: The size dimensions for the window in the format (width, height)
        :type size: tuple[int, int]
        """
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

    def center_window(self) -> None:
        """
        Centers the window on the screen based on the current screen dimensions and the
        configured width and height of the window. Adjusts the geometry of the window
        to ensure it is aligned at the center of the user's screen.

        :return: None
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))


class Main(ttk.Frame):
    """
    Represents the primary interface for the typing speed test application.

    This class contains widgets for the GUI,
    including labels, an entry box for user input, and statistical displays
    for typing speed metrics such as characters per second, words per minute, etc.

    :ivar highscore_label: Label to display the high score of the typing speed test.
    :type highscore_label: ttk.Label
    :ivar title_label: Label to display the title of the application.
    :type title_label: ttk.Label
    :ivar description_label: Label to display instructions for the typing test.
    :type description_label: ttk.Label
    :ivar test_text_label: Label to display the randomly generated words
        for users to type.
    :type test_text_label: ttk.Label
    :ivar entry_var: String variable to track user input in the entry box.
    :type entry_var: ttk.StringVar
    :ivar user_entry: Entry widget for the user to type words.
    :type user_entry: ttk.Entry
    :ivar info_label: Label to display descriptive text for typing speed metrics.
    :type info_label: ttk.Label
    :ivar cps_label: Label to display the typing speed in characters per second.
    :type cps_label: ttk.Label
    :ivar cpm_label: Label to display the typing speed in characters per minute.
    :type cpm_label: ttk.Label
    :ivar wps_label: Label to display the typing speed in words per second.
    :type wps_label: ttk.Label
    :ivar wpm_label: Label to display the typing speed in words per minute.
    :type wpm_label: ttk.Label
    :ivar reset_button: Button to reset the typing test and clear the data.
    :type reset_button: ttk.Button
    :ivar final_score_label: Label to display the user's final score upon
        completion of the test.
    :type final_score_label: ttk.Label
    """

    def __init__(self, parent: tk.Misc) -> None:
        """
        Initializes the app's GUI with various labels and widgets for
        displaying and interacting with typing speed metrics. The layout includes highscore,
        instructional text, user input entry, real-time speed metrics, and a reset button.

        Key features:
        - Displays highscore information.
        - Provides typing test instructions.
        - Presents a set of words for the typing test dynamically.
        - Collects user input for the typing test.
        - Calculates and displays typing speed metrics in characters and words per second/minute.
        - Offers a reset functionality to restart the test.
        - Displays the final score after the typing test.

        :param parent: The tkinter parent widget to which this interface will be attached.
        :type parent: tk.Misc
        """
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
    """
    Represents the application logic for a graphical user interface (GUI)-based typing speed test application.

    This class is responsible for managing the state of the application, handling user input,
    calculating typing speed metrics, and tracking and updating highscores. It also communicates
    with the GUI to display real-time statistics and test results. The application tracks
    character per second (CPS), character per minute (CPM), word per second (WPS), and
    word per minute (WPM) scores, saving highscores to a file.

    :ivar counter: Tracks the elapsed time in seconds since the start of the test.
    :type counter: float
    :ivar running: Indicates whether the typing test is currently in progress.
    :type running: bool
    :ivar highscore_cps: Stores the highest characters-per-second score achieved.
    :type highscore_cps: float
    :ivar highscore_cpm: Stores the highest characters-per-minute score achieved.
    :type highscore_cpm: float
    :ivar highscore_wps: Stores the highest words-per-second score achieved.
    :type highscore_wps: float
    :ivar highscore_wpm: Stores the highest words-per-minute score achieved.
    :type highscore_wpm: float
    :ivar highscores: A pandas DataFrame containing the current highscores, or None if not loaded.
    :type highscores: pandas.DataFrame or None
    """

    def __init__(self, title: str, size: tuple[int, int]) -> None:
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

    def load_highscores(self) -> None:
        """
        Loads high scores from a CSV file or initializes defaults if the file is not
        found.

        This function attempts to load high score data from a pre-defined file
        location. If the file is missing or cannot be accessed, it creates a new
        default DataFrame for storing high scores. The function ensures that
        the attributes `highscore_cps`, `highscore_cpm`, `highscore_wps`, and
        `highscore_wpm` are updated with the corresponding values from the file
        or default values.

        :raises FileNotFoundError: If the file 'assets/scores.csv' cannot be found.
        """
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

    def start(self, event: tk.Event) -> None:
        """
        Handles the starting and execution logic for tracking typing events and updating the GUI
        elements accordingly. This function starts a timing thread when needed, updates the
        font color of the user entry field based on the correctness of the input, and
        checks for high scores upon successful completion of the typing task.

        :param event: Event object containing metadata about the user-initiated action;
            commonly used to determine the pressed key.
        :type event: Event
        :return: None
        """
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


    def time_thread(self) -> None:
        """
        Continuously calculates and updates typing speed metrics while running.
        This function is intended to execute within a separate thread. It monitors
        a running condition and performs periodic computations of typing speed in terms of
        characters per second, characters per minute, words per second, and words per minute.
        The calculated metrics are dynamically updated on corresponding labels in the user interface.

        While the thread is active (defined by the `running` attribute), the loop will:
          - Increment a counter with a timed interval (0.1 seconds).
          - Compute typing speed metrics based on the text entered in the GUI input field.
          - Update related GUI labels with the computed values.

        :raises RuntimeError: If there are issues with thread operation during execution.
        :return: None
        """
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



    def reset(self) -> None:
        """
        Resets the current typing test state and updates all related labels and fields to
        their initial state. This includes stopping ongoing timings, resetting counters,
        updating score and speed labels, clearing the user input, and setting new text for
        the typing test.

        :rtype: None
        :return: None
        """
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

    def check_for_highscore(self) -> None:
        """
        Updates the highscores based on the current test results for characters per second (CPS),
        characters per minute (CPM), words per second (WPS), and words per minute (WPM).
        If a new highscore is achieved for either characters or words metrics, it updates the
        corresponding records, modifies the final score display with appropriate messages,
        and writes the updated highscores to a CSV file.

        :raises ValueError: If the text extracted from `cps_label`, `cpm_label`, `wps_label`,
                            or `wpm_label` cannot be converted to a float.
        :type last_cps_score: float
        :attr last_cps_score: Current CPS score extracted from the `main.cps_label`.
        :type last_cpm_score: float
        :attr last_cpm_score: Current CPM score extracted from the `main.cpm_label`.
        :type last_wps_score: float
        :attr last_wps_score: Current WPS score extracted from the `main.wps_label`.
        :type last_wpm_score: float
        :attr last_wpm_score: Current WPM score extracted from the `main.wpm_label`.

        :param chars_is_new_highscore: Boolean flag indicating if a new highscore for
                                        characters (CPS/CPM) metrics has been achieved.
        :type chars_is_new_highscore: bool
        :param words_is_new_highscore: Boolean flag indicating if a new highscore for
                                        words (WPS/WPM) metrics has been achieved.
        :type words_is_new_highscore: bool

        :postcondition: Updates the `highscore_cps`, `highscore_cpm`, `highscore_wps`,
                        and `highscore_wpm` attributes and saves them to `highscores`
                        DataFrame when a new highscore is achieved.
        :postcondition: Updates the final score label in the `main` attribute with relevant
                        highscore messages.
        :postcondition: Writes the updated `highscores` DataFrame back to a CSV file
                        for persistent storage.

        :return: None
        """
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



