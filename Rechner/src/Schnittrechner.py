from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os 
from pathlib import Path

import Calculator



class MainWindow(QWidget):
    """Main window of the application"""
    def __init__(self):
        super().__init__()
        self.resize(250, 250)
        self.setWindowTitle("Schnittrechner")
        self.setGeometry(100, 100, 400, 100)


 
        layout = QVBoxLayout() # Creating a layout (in this case a vertical one)
        self.setLayout(layout) # Setting the layout to the window
        # file selection

        file_browse = QPushButton('Browse') # Creating a button widget
        file_browse.clicked.connect(self.open_file_dialog) # Connecting the button to a function (in this case the function is for opening a file dialog)

        # set the file list as a textbox
        self.file_list = QListWidget(self) # Creating a list widget
        self.file_list_it = [] # Creating a list for the items in the list widget

        calculate_button = QPushButton("Calculate") # Creating a button widget for calculating the average grade
        calculate_button.clicked.connect(self.calculation) # Connecting the button to a function (in this case the function is for calculating the average grade)

        self.output_table = QTableWidget(self)
        self.output_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Set the table widget to not be editable

        # Hinzufügen eines Schalters für den Dark-Modus
        self.dark_mode_switch = QCheckBox("Dark Mode")
        self.dark_mode_switch.stateChanged.connect(self.toggle_dark_mode)


        layout.addWidget(self.dark_mode_switch)
        layout.addWidget(QLabel('Selected Files:'), 0) # Adding a widget to the layout (in this case a label aka text)
        layout.addWidget(self.file_list, 1) # Adding a widget to the layout (in this case it is a ListWidget aka a list of items, in this case the items are the files)
        layout.addWidget(file_browse, 2) # Adding a widget to the layout (in this case it is a button for browsing files)
        layout.addWidget(calculate_button) # Adding a widget to the layout (in this case it is a button for calculating the average grade)
        layout.addWidget(self.output_table) # Adding a widget to the layout (in this case it is a table for the output of the average grades)
    

# Explanation of the stylesheet:
        
    """ For dark mode:

        # For all QWidget elements in the application
        QWidget {
            # Set the background color to #2b2b2b (a dark gray)
            background-color: #2b2b2b;
            # Set the text color to #ffffff (white)
            color: #ffffff;
        }
        # For all QPushButton elements in the application
        QPushButton {
            # Set the background color to #353535 (an even darker gray)
            background-color: #353535;
        }
        # For all QCheckBox elements in the application
        QCheckBox {
            # Set the text color to #ffffff (white)
            color: #ffffff;
        }
    """
    """ For light mode:
        # For all QWidget elements in the application
        QWidget {
            # Set the background color to #ffffff (white)
            background-color: #ffffff;
            # Set the text color to #000000 (black)
            color: #000000;
        }
        # For all QPushButton elements in the application
        QPushButton {
            # Set the background color to #f0f0f0 (a light gray)
            background-color: #f0f0f0;
        }
        # For all QCheckBox elements in the application
        QCheckBox {
            # Set the text color to #000000 (black)
            color: #000000;
        }
    """

    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #353535;
                }
                QCheckBox {
                    color: #ffffff;
                }
            """) # Set the stylesheet of the window to the dark mode stylesheet)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QPushButton {
                    background-color: #f0f0f0;
                }
                QCheckBox {
                    color: #000000;
                }
            """) # Set the stylesheet of the window to the light mode stylesheet

    def calculation(self):
        """Calculate the average grade for all files in the list widget and add the result to the table widget"""
        for i, item in enumerate(self.file_list_it): # Loop through all items in the list widget
            self.input_for_calculation = item # Set the input for the calculation to the current item
            rechner = Calculator.Schnittrechner(pdf_path=self.input_for_calculation) # Create an instance of the Schnittrechner class
            ects = rechner.get_ects() # Get the ECTS from the PDF file
            sum_ects = rechner.get_sum_ects() # Get the sum of the ECTS from the PDF file
            grades = rechner.get_grades() # Get the grades from the PDF file
            average_grade = rechner.calculation() # Calculate the average grade
            ects_vo, ects_ue, ects_pue, ects_vu, ects_lp, ects_module, ects_se = rechner.get_some_ects() # Get the ECTS for VO, UE, PUE, VU and LP from the PDF file

            ects_relevant = ects_vo + ects_ue + ects_vu + ects_lp + ects_module + ects_se - ects_pue# Get the relevant ECTS from the PDF file
            ects_not_relevant = ects_pue # Get the not relevant ECTS from the PDF file


            # Get the filename from the path
            filename = os.path.basename(self.input_for_calculation) # Get the filename from the path
            self.output_table.setColumnCount(len(self.file_list_it) + 4) # Set the number of columns in the table widget to the number of items in the list widget
            self.output_table.setRowCount(len(self.input_for_calculation)) # Set the number of rows in the table widget to the number of items in the list widget
            self.output_table.setItem(i, 0, QTableWidgetItem(filename)) # Add the filename to the table widget

            if average_grade == 0: # If the average grade is 0, set the average grade to "N/A"
                average_grade = "N/A"
                self.output_table.setItem(i, 1, QTableWidgetItem(str(average_grade)))
            else:
                self.output_table.setItem(i, 1, QTableWidgetItem(str(round(average_grade, 2)))) # Add the average grade to the table widget

            if ects_relevant == 0: # If the relevant ECTS is 0, set the relevant ECTS to "N/A"
                ects_relevant = "N/A"
                self.output_table.setItem(i, 2, QTableWidgetItem(str(ects_relevant)))
            else:
                self.output_table.setItem(i, 2, QTableWidgetItem(str(round(ects_relevant, 2))))

            if ects_not_relevant == 0: # If the not relevant ECTS is 0, set the not relevant ECTS to "N/A"
                ects_not_relevant = "N/A"
                self.output_table.setItem(i, 3, QTableWidgetItem(str(ects_not_relevant)))
            else:
                self.output_table.setItem(i, 3, QTableWidgetItem(str(round(ects_not_relevant, 2))))

            if sum_ects == 0: # If the sum of the ECTS is 0, set the sum of the ECTS to "N/A"
                sum_ects = "N/A"
                self.output_table.setItem(i, 4, QTableWidgetItem(str(sum_ects)))
            else:
                self.output_table.setItem(i, 4, QTableWidgetItem(str(round(sum_ects, 2)))) # Add the sum of the ECTS to the table widget


            self.output_table.setHorizontalHeaderLabels(["Dateiname", "Schnitt", "Relevant ECTS", "Non-relevant ECTS", "Total ECTS"]) # Set the header labels for the table widget
            self.output_table.resizeColumnsToContents() # Resize the columns of the table widget to fit the content
            self.output_table.resizeRowsToContents() # Resize the rows of the table widget to fit the content

            # Center the text in the table for all elements in the table
            for i in range(self.output_table.rowCount()):
                for j in range(self.output_table.columnCount()):
                    item = self.output_table.item(i, j)
                    if item is not None:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def open_file_dialog(self):
        """Open a file dialog for selecting files"""
        script_dir = os.path.dirname(__file__) # Absolute path to the directory of the script
        path = os.path.join(script_dir, "..", "..") # Absolute path to the directory of the script
        path = os.path.join(path, "Daten") # Absolute path to the directory of the script

        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            path,
            "Files (*.pdf)"
        ) # Open a file dialog for selecting files

        if filenames: # If the user selected a file, add it to the list widget
            for filename in filenames:
                path = Path(filename)
                self.file_list.addItem(str(path))
                self.file_list_it.append(str(path))

app = QApplication([]) # Creating an application (you dont need the sys.argv if you dont want to use command line arguments, if you want to use them you need to pass them to the QApplication)
window = MainWindow() # Creating a window (in this case the window is the main window)
window.show() # Showing the window

# Start the event loop of the application. This will keep the program running until the user closes the main window or the program is terminated in another way.
app.exec()