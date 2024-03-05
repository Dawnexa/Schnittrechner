# Standard library imports
import sys
import os
import csv
from datetime import date
from pathlib import Path

# Third party imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qtwidgets import AnimatedToggle, Toggle
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator

# Local application imports
from utils import *
import Calculator


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, x_axis=None, y_axis=[1], title=None, total_ects=None):
        fig = Figure(figsize=(3, 3), dpi=100)
        self.axes = fig.add_subplot(111)
        # Dies ist wichtig, da dies sicherstellt, dass das Canvas und die Figure die gleiche Größe haben
        # was verhindert, dass das Diagramm abgeschnitten wird
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.plot(y_axis=y_axis)

    def plot(self, x_axis=None, y_axis=None, title=None, total_ects=None):
        self.axes.clear()
        semester = len(y_axis)
        x_axis = list(range(1, semester + 1, 1))
        
        self.axes.bar(x_axis, y_axis, align='center', width=0.2, alpha=0.5, color='b', label='ECTS per Semester')
        self.axes.set_xlabel('Semester')
        self.axes.set_ylabel('ECTS')

        # Make a line at 180 ECTS
        self.axes.axhline(y=180, color='r', linestyle='--', label='180 ECTS')
        
        # Plot the total ects and the development of the ects
        total_ects = []
        for i in range(len(y_axis)):
            if i == 0:
                total_ects.append(y_axis[i])
            else:
                total_ects.append(total_ects[i-1] + y_axis[i])

        self.axes.plot(x_axis, total_ects, label='Total ECTS', color='g', marker='o', linestyle='-', linewidth=2)
        self.axes.xaxis.set_major_locator(MultipleLocator(1))
        self.axes.legend(loc='upper left')
        self.draw()

    def plot_semester(self, x_axis=None, y_axis=None, title=None, total_ects=None):
        self.axes.clear()
        subjects = len(y_axis)

        self.axes.bar(x_axis, y_axis, align='center', width=0.2, alpha=0.5, color='darkblue')
        self.axes.set_xlabel('Subject')
        self.axes.set_ylabel('ECTS')
        # self.axes.legend(loc='upper left')
        self.draw()


class MainWindow(QMainWindow):
    """Main window of the application"""
    def __init__(self):
        super().__init__()


        # Set the size and title of the window
        self.setWindowTitle("Schnittrechner")
        self.setFixedSize(1000, 660)
        # self.showFullScreen()

        # Variables for calculation
        self.ects = []
        self.ects_Plot = []
        self.ects_semester_plot = []
        self.subjects_semester_plot = []
        self.sum_ects = {}
        self.data_list = []

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)  # Set the layout to the central widget

        # Create a menu bar
        filebar = QMenu(self)

        openFile = QAction("Open Datafile", self)
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(self.open_file)

        saveFile = QAction("Save Datafile", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.triggered.connect(self.save_file)
        

        filebar.addAction(openFile)
        filebar.addAction(saveFile)



        # Create a toolbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # Create an action for the toolbar
        openfilemenu = QAction("File", self)
        openfilemenu.setMenu(filebar)


        # Add the action to the toolbar
        toolbar.addAction(openfilemenu)

        # Add the toolbar to the layout
        layout.addWidget(toolbar)

        # file selection
        file_browse = QPushButton('Browse') # Creating a button widget
        # file_browse.setFixedWidth(100) # Set the width of the button widget
        file_browse.setFixedHeight(33) # Set the height of the button widget
        file_browse.clicked.connect(self.open_file_dialog) # Connecting the button to a function (in this case the function is for opening a file dialog)

        # set the file list as a textbox
        self.file_list = QListWidget(self) # Creating a list widget
        self.file_list.setFixedHeight(100) # Set the height of the list widget
        self.file_list.setFixedWidth(600) # Set the width of the list widget
        self.file_list.setItemAlignment(Qt.AlignmentFlag.AlignCenter) # Set the alignment of the list widget

        self.refresh_button = QPushButton("Refresh")
        # self.refresh_button.setFixedWidth(100)
        self.refresh_button.setFixedHeight(33)
        self.refresh_button.clicked.connect(self.plot)

        calculate_button = QPushButton("Calculate") # Creating a button widget for calculating the average grade
        # calculate_button.setFixedWidth(100) # Set the width of the button widget
        calculate_button.setFixedHeight(33) # Set the height of the button widget
        calculate_button.clicked.connect(self.calculation) # Connecting the button to a function (in this case the function is for calculating the average grade)

        self.file_list_it = [] # Creating a list for the items in the list widget

        self.output_table = QTableWidget(self)
        self.output_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Set the table widget to not be editable


        self.data = [] # Creating a list for the data

        self.toggle_2 = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )

        self.toggle_2.stateChanged.connect(self.toggle_dark_mode)
        self.toggle_2.setFixedSize(100, 50)
        self.Data = []

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.plot)

        layout.addWidget(QLabel('Dark Mode:'))
        layout.addWidget(self.toggle_2)

        # Create a vertical layout for the label and the file list
        vlayout_file_list = QVBoxLayout()

        # Add the label and the file list to the vertical layout
        vlayout_file_list.addWidget(QLabel('Selected Files:'))
        vlayout_file_list.addWidget(self.file_list)

        # Create a vertical layout for the buttons
        vlayout_buttons = QVBoxLayout()

        # Add the browse button, calculate button, and refresh button to the vertical layout
        vlayout_buttons.addWidget(QLabel(''))
        vlayout_buttons.addWidget(file_browse)
        vlayout_buttons.addWidget(calculate_button)
        vlayout_buttons.addWidget(self.refresh_button)

        # Create a horizontal layout
        hlayout_filelist_buttons = QHBoxLayout()

        # Add the vertical layout for the file list and the vertical layout for the buttons to the horizontal layout
        hlayout_filelist_buttons.addLayout(vlayout_file_list)
        hlayout_filelist_buttons.addLayout(vlayout_buttons)

        # Add the horizontal layout to the main layout
        layout.addLayout(hlayout_filelist_buttons)
        
        self.canvas = MyMplCanvas(y_axis=self.ects) # Create an instance of the MyMplCanvas class
        self.canvas.setFixedHeight(400) # Set the height of the canvas widget
        self.canvas.setFixedWidth(600) # Set the width of the canvas widget

        self.output_table.setFixedHeight(200) # Set the height of the table widget
        self.output_table.setFixedWidth(300) # Set the width of the table widget

        # Create a horizontal layout for the plot and the output list
        hlayout_plot_output = QHBoxLayout()

        vlayout_plot_output = QVBoxLayout()
    


        vlayout_plot_output.addWidget(self.output_table)
        self.list_widget = QListWidget(self)
        self.list_widget.setFixedHeight(200)
        self.list_widget.setFixedWidth(300)
        self.list_widget.itemClicked.connect(self.semester_choose)
        
        vlayout_plot_output.addWidget(self.list_widget)

        # Add the plot and the output list to the horizontal layout
        hlayout_plot_output.addLayout(vlayout_plot_output)
        hlayout_plot_output.addWidget(self.canvas)

        # Add the horizontal layout for the plot and the output list to the main layout
        layout.addLayout(hlayout_plot_output)

    """Explanation of the stylesheet:
         For dark mode:

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
        
         For light mode:
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

            ects_relevant = ects_vo + ects_ue + ects_vu + ects_lp + ects_module + ects_se - ects_pue # Get the relevant ECTS from the PDF file
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


            self.sum_ects = rechner.semester_ects()
            self.raw_ects = rechner.get_semester_ects_per_LV()

            for key, value in self.sum_ects.items():
                self.ects_Plot.append(value)

            if self.Data == []:
                data_header = ["Dateiname", "Schnitt", "Relevant ECTS", "Non-relevant ECTS", "Total ECTS", "Datum"] # Set the header labels for the table widget

                ects = rechner.get_ects_per_semester() # Get the ECTS per semester from the PDF file
                for key, value in ects.items():
                    data_header.append(key)
                    self.list_widget.addItem(key)

                self.data.append(data_header) # Add the header labels to the list
                today = date.today()

                data = [filename, average_grade, ects_relevant, ects_not_relevant, sum_ects, today.strftime("%d/%m/%Y")] 

                for key, value in ects.items():
                    daten = get_sum(value)
                    print(daten)
                    data.append(daten)
                    self.ects.append(daten)

                self.data.append(data) # Add the data to the list

            elif self.Data != []:

                self.data = self.Data
                data_header = ["Dateiname", "Schnitt", "Relevant ECTS", "Non-relevant ECTS", "Total ECTS", "Datum"] # Set the header labels for the table widget

                ects = rechner.get_ects_per_semester() # Get the ECTS per semester from the PDF file
                for key, value in ects.items():
                    data_header.append(key)

                self.data.append(data_header) # Add the header labels to the list
                today = date.today()

                data = [filename, average_grade, ects_relevant, ects_not_relevant, sum_ects, today.strftime("%d/%m/%Y")] 

                for key, value in ects.items():
                    daten = get_sum(value)
                    print(daten)
                    data.append(daten)
                    self.ects.append(daten)

                self.data.append(data) # Add the data to the list

            print(self.ects_semester_plot, self.subjects_semester_plot) 

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
                self.file_list.addItem(str(path.name))
                self.file_list_it.append(str(path))

    def open_file(self):
        """Open a file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Files (*.csv)" # Maybe add support for other file types
        )

        if filename:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                self.Data = list(reader)
                self.data_list.clear()
                for i in self.Data:
                    self.data_list.append(i)

    def save_file(self):
        """Save a file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Files (*.csv)" # Maybe add support for other file types
        )

        if filename:
            with open(filename, "w") as file:
                writer = csv.writer(file)
                writer.writerows(self.data)

    def plot(self):
        """Plot the ECTS per semester"""
        self.canvas.plot(y_axis=self.ects_Plot)

    def plot_semester(self):
        """Plot the ECTS per semester"""
        self.canvas.plot_semester(x_axis=self.subjects_semester_plot, y_axis=self.ects_semester_plot)

    def semester_choose(self, item):
        """Plot the ECTS per semester"""
        self.ects_semester_plot = []
        self.subjects_semester_plot = []
        semester = item.text()
        for key, value in self.raw_ects.items():
            if key == semester:
                dumb_list = value

        for key, element in dumb_list.items():
            self.subjects_semester_plot.append(key)
            self.ects_semester_plot.append(element)

        self.canvas.plot_semester(x_axis=self.subjects_semester_plot, y_axis=self.ects_semester_plot)


        

app = QApplication([]) # Creating an application (you dont need the sys.argv if you dont want to use command line arguments, if you want to use them you need to pass them to the QApplication)
window = MainWindow() # Creating a window (in this case the window is the main window)
window.show() # Showing the window

# Start the event loop of the application. This will keep the program running until the user closes the main window or the program is terminated in another way.
app.exec()