from collections import deque, defaultdict
import os
import json
from enum import Enum
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtCore import Qt, QObject, pyqtSlot
from PyQt5.QtGui import QKeyEvent, QKeySequence

from ai.gpt.request import chat, transcribe

from core.cmd.editor import CommandsEditor
from core.cmd.manager import CommandsManager


class Commands(QObject):
    def __init__(self, dweller, menu):
        super().__init__()
        self.commands_manager = CommandsManager(dweller, menu)
        self.commands_editor = CommandsEditor(dweller, menu)
        self.menu = menu
        self.initConfig()
        self.initActions()
    
    
    def initConfig(self):
        try:
            with open(os.environ.get("SOURCE_COMMAND_CONFIG_PATH")) as f:
                self.config = json.load(f)
                print(self.config)
        except:
            print("No config file found.")
        
    def initActions(self):
        if not self.config:
            print("error with config file")
            return
        
    
        for action_name, key_sequence in self.config.items():
            action = QAction(action_name.capitalize(), self)
            action.setShortcut(QKeySequence(key_sequence))
            action.triggered.connect(lambda checked, name=action_name: self.commands_manager.execute(name))
            self.menu.addAction(action)
        

    @pyqtSlot(QKeyEvent)
    def receiver(self, event: QKeyEvent):
        if event.modifiers() & Qt.MetaModifier:
            if event.type() == QKeyEvent.KeyPress:
                self.commands_manager.execute(event)
            
