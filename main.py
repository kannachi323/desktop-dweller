import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor, QPixmap, QColor, QPixmapCache

class FollowCursorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Follow Cursor")
        self.setFixedSize(200, 200)  # Set a fixed size for the window

        # Set the window to always stay on top and frameless
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.5);
            }  
        """)

        # Paths to images
        image_up = "/Users/mtccool668/projects/desktop-dweller/images/kanna_left.png"
        image_down = "/Users/mtccool668/projects/desktop-dweller/images/kanna_right.png"

        # Check if the image files exist
        if not os.path.exists(image_up):
            print(f"Error: Image not found at {image_up}")
        if not os.path.exists(image_down):
            print(f"Error: Image not found at {image_down}")

        # Create a label to display the image
        self.label = QLabel(self)

        # Load both pixmaps
        self.pixmap_up = QPixmap(image_up)
        self.pixmap_down = QPixmap(image_down)

        # Set a default image (e.g., down image initially)
        if not self.pixmap_down.isNull():
            self.label.setPixmap(self.pixmap_down)
        else:
            print("Failed to load down image.")

        self.label.setScaledContents(True)
        self.label.resize(self.size())


        # Create a timer to update the position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # Update every 10 milliseconds

        # Store the last cursor position
        self.last_cursor_pos = QCursor.pos()

    def update_position(self):
        current_pos = QCursor.pos()  # Get the current global cursor position

        # Determine movement direction
        if current_pos.x() < self.last_cursor_pos.x():
            # Moved left: Change to up image
            if not self.pixmap_up.isNull():
                QPixmapCache.clear()
                self.label.clear()
                self.label.setPixmap(self.pixmap_up)
                print('moving left')
             # Update the window position
            self.move(current_pos.x() + 50, current_pos.y() - self.height() // 2)
            
        elif current_pos.x() > self.last_cursor_pos.x():
            # Moved right: Change to down image
            if not self.pixmap_down.isNull():
                QPixmapCache.clear()
                self.label.clear()
               
                self.label.setPixmap(self.pixmap_down)
                print('moving right')
            self.move(current_pos.x() - 200 - 50, current_pos.y() - self.height() // 2)
        
        else:
            self.label.update()
            self.update()
            app.processEvents()

           
            print('fixed')
        
        
       
        
        # Remember this position for the next update
        self.last_cursor_pos = current_pos

# Main application
app = QApplication(sys.argv)

window = FollowCursorWindow()
window.show()

sys.exit(app.exec_())
