from PyQt5.QtCore import QThreadPool, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
import time
from utils.worker import Worker

def example_task(command):
    if command == "gpt":
        print("running gpt api")
        time.sleep(3)
        print("response from gpt api")
    elif command == "google":
        print("running google api")
        time.sleep(5)
        print("response from google api")
    else:
        print("unknown command")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.workers = {}  # Dictionary to track worker statuses
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Click to start tasks")
        layout.addWidget(self.label)

        self.button_gpt = QPushButton("Start GPT Task")
        self.button_gpt.clicked.connect(lambda: self.startWorker(example_task, "gpt"))
        layout.addWidget(self.button_gpt)

        self.button_google = QPushButton("Start Google Task")
        self.button_google.clicked.connect(lambda: self.startWorker(example_task, "google"))
        layout.addWidget(self.button_google)

        self.setLayout(layout)

    def startWorker(self, task, *args, **kwargs):
        worker = Worker(task, *args, **kwargs)
        self.workers[worker] = "running"
        worker.signals.finished.connect(self.removeWorker)
        self.threadpool.start(worker)

    @pyqtSlot(QRunnable)
    def removeWorker(self, worker):
        if worker in self.workers:
            self.workers[worker] = "finished"
        print(self.workers)  

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
