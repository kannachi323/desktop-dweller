import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtGui import QKeySequence


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Shortcuts from Config")
        self.setGeometry(100, 100, 400, 300)

        # Load configuration from JSON file
        self.config = self.load_config("/Users/mtccool668/projects/desktop-dweller/core/config.json")
        print(self.config)

        # Menu for actions
        self.menu = self.menuBar().addMenu("Actions")

        # Dictionary to store actions
        self.actions = {}

        # Create actions dynamically
        self.create_actions()

    def load_config(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        else:
            print(f"Config file not found: {path}")
            return {}

    def create_actions(self):
        for action_name, shortcut in self.config.items():
            # Create a new QAction
            action = QAction(action_name.capitalize(), self)
            action.setShortcut(QKeySequence(shortcut))

            # Connect the action to a handler
            action.triggered.connect(lambda checked, name=action_name: self.handle_action(name))

            # Add action to menu
            self.menu.addAction(action)

            # Store the action in a dictionary for further reference
            self.actions[action_name] = action

    def handle_action(self, action_name):
        print(f"Action triggered: {action_name}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
