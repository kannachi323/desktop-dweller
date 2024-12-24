from collections import deque
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import Qt, QObject, QThreadPool
from PyQt5.QtGui import QKeyEvent, QCursor

from core.vad.audio_vad import AudioVAD
from utils.worker import Worker
from ai.gpt.request import transcribe


class CommandsManager(QObject):
    def __init__(self, dweller, menu):
        super().__init__()
        self.dweller = dweller
        self.threadpool = QThreadPool()
        
    

    def execute(self, name):
        match name:
            case "MOVE": 
                self.handleMove()
            case "HOME":
                self.handleHome()
            case "TALK":
                self.handleTalk()
            case "READ":
                self.handleRead()
            case "WATCH":
                self.handleWatch()

            
    def handleMove(self):
        current_pos = QCursor.pos()
        self.dweller.move(
            current_pos.x() - self.dweller.width() // 2,
            current_pos.y() - self.dweller.height() // 2
        )

    def handleHome(self):
        screen = self.dweller.screen().geometry()
        self.dweller.move(
            screen.width() // 2 - self.dweller.width() // 2,
            screen.height() // 2 - self.dweller.height() // 2
        )
    
    def handleTalk(self):
        audio_recorder = AudioVAD(2)
        print("listening")
        worker = Worker(audio_recorder.start)
        worker.signals.finished.connect(lambda _: print("not listening anymore"))
        self.threadpool.start(worker)
        