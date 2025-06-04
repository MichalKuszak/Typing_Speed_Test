
# Typing Speed Test App

A Python-based typing speed test app built using Tkinter and ttkbootstrap. This app helps users test their typing speed in real-time while tracking metrics like characters per second (CPS), words per minute (WPM), and more. It includes a highscore system to encourage users to improve their typing skills.

## Features

- **Real-Time Typing Metrics**: Displays typing speed in **CPS**, **CPM**, **WPS**, and **WPM**.
- **Highscore Tracking**: Keeps track of the user's highest scores and displays them during the test.
- **Random Word Selection**: Generates random words for the user to type, making each test unique.
- **Easy to Use Interface**: Clean and user-friendly UI built using Tkinter and ttkbootstrap.
- **Reset Functionality**: Allows users to restart the typing test anytime.

## Installation

1. Clone or download the repository.
2. Make sure you have Python 3.6 or higher installed.
3. Install required dependencies:
   ```
   pip install ttkbootstrap pandas
   ```

4. Download or create a `words.txt` file in the `./assets/` directory with a list of words (one word per line).
5. Run the application:
   ```
   python app.py
   ```

## Usage

- **Start Typing**: Simply start typing the words shown in the test area to begin the test.
- **Metrics**: Your typing speed will be displayed as you type, including characters per second (CPS), characters per minute (CPM), words per second (WPS), and words per minute (WPM).
- **Highscores**: The app will track your highest CPS, CPM, WPS, and WPM. Once you complete a test, the app checks if you've beaten your high score.
- **Reset**: Press the reset button to restart the test and clear the current session data.

## Contributing

Feel free to fork this repository and submit pull requests for bug fixes, enhancements, or features. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
