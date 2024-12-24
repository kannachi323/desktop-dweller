from PyQt5.QtCore import QObject, pyqtSignal
import time

class DwellerWorker(QObject):
    task_finished = pyqtSignal(str)  # Signal to notify when a task is done

    def __init__(self):
        super().__init__()

    def perform_task(self):
        time.sleep(3)  # Simulated delay
        result = "Task completed!"  # Replace with actual task logic
        self.task_finished.emit(result)
