from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings
from PyQt5.QtGui import QCursor, QPixmap, QKeyEvent, QMouseEvent
from core.cmd.commands import Commands
import os


# we need this bc dweller should communicate with other class objs
class DwellerSignals(QObject):
    keyboardSignal = pyqtSignal(QKeyEvent)
    mouseSignal = pyqtSignal(QMouseEvent)
    audioSignal = pyqtSignal(str)


class Dweller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.signals = DwellerSignals()
        self.initCommands()

    def initUI(self):
        self.setFixedSize(200, 200)  # Set a fixed size for the window
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a central widget for QMainWindow
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout and assign it to the central widget
        layout = QVBoxLayout(central_widget)

        # Initialize QLabel and set its pixmap
        self.label = QLabel(self)
        print(os.environ.get('SOURCE_IMAGE_PATH'))
        self.pixmap = QPixmap(os.environ.get('SOURCE_IMAGE_PATH'))
        if not self.pixmap.isNull():
            self.label.setPixmap(self.pixmap)
            self.label.setScaledContents(True)
            self.label.resize(self.size())
            print("i set image")

        layout.addWidget(self.label)  # Add QLabel to the layout

    def initCommands(self):
        self.menu = self.menuBar().addMenu("Actions")
        self.commands = Commands(self, self.menu)
        self.signals.keyboardSignal.connect(self.commands.receiver)

    def updatePosition(self):
        current_pos = QCursor.pos()  # Get the current global cursor position
        self.move(current_pos.x() - self.width() // 2, current_pos.y() - self.height() // 2)

    def keyPressEvent(self, event: QKeyEvent):
        self.signals.keyboardSignal.emit(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        self.signals.keyboardSignal.emit(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.signals.mouseSignal.emit(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.signals.mouseSignal.emit(event)
