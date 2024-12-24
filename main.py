import sys
from PyQt5.QtWidgets import QApplication
from dweller import Dweller
from dotenv import load_dotenv

# Main application
if __name__ == "__main__":
    load_dotenv()
    app = QApplication(sys.argv)
    dweller = Dweller()


    #only show after all resources are created
    dweller.show()
   
    sys.exit(app.exec())
