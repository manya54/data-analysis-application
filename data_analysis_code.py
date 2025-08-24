"""

domain: Electricity Consumption and Production

The Energy Consumption Data Analysis Application is a user-friendly desktop application designed to help users visualize and analyze
energy consumption data. 
The application provides a graphical user interface (GUI) that allows users to load a CSV file containing energy consumption data, 
display the data in a tabular format, and generate various plots to analyze the data.

"""



import sys #importing the sys module
import pandas as pd #importing the pandas library
import matplotlib.pyplot as plt #importing matplotlib
from PyQt5.QtCore import * #importing Core non-GUI classes used by other modules
from PyQt5.QtGui import * #importing Graphical user interface components
from PyQt5.QtWidgets import * #importing all the widgets under QtWidgets

class MainWindow(QWidget): #declaring a class for the main window that inherits from the Qwidget class
    def __init__(self):  #__init__ method in Python is used to initialize(assign values) objects of a class.
        super(MainWindow, self).__init__() #calls the __init__ method of the parent class (QWidget) within the mainWindow class.

        self.setStyleSheet("background-color: #BACFFA;") #background colour
        #self.setStyleSheet("background-color: #BACFFA;") #background colour

        self.setGeometry(1000,200,2000,1500) #setting the x-position, y-position, x-dimension and y-dimension of the window
        self.setWindowTitle("Electricity Consumption and Production Analysis") #setting window title

        self.layout = QVBoxLayout() #the layout of the window will be vertical, the widgets will be added vertically

        self.create_menu()  #adding the menu bar by calling upon the create_men method

        self.label = QLabel(self) #displaying text
        self.label.setText("Electricity Consumption and Production Analysis") #writing the text
        font = QFont() #using the Qfont class
        font.setFamily("Times New Roman") #setting the font
        font.setPointSize(14) #setting font size
        self.label.setFont(font) #applying the font to the Qlable widget
        self.label.setAlignment(Qt.AlignCenter)  # Center the text horizontally and vertically
        self.layout.addWidget(self.label)  # add the label to the layout

        self.label = QLabel(self) #displaying text
        self.label.setText("Open CSV file to start:") #writing the text
        font = QFont() #using the Qfont class
        font.setFamily("Calibri") #setting the font
        font.setPointSize(10) #setting font size
        self.label.setFont(font) #applying the font to the Qlable widget
        self.layout.addWidget(self.label)  # add the label to the layout

        self.plot_button = QPushButton("Generate Plot", self) #creating a button for generating the plot.
        self.plot_button.clicked.connect(self.generate_plot) #the generate_plot method is called upon when the button is clicked.
        self.layout.addWidget(self.plot_button) #adds the button to the main window
        self.plot_button.setEnabled(False) #disables the "Generate Plot" button when it is initially created.
        self.plot_button.setStyleSheet("background-color: #000000; color: white;") #background colour

        self.table_button = QPushButton("Load File",self) #creates a push button using the QPushButton widget with the label "load file"
        self.table_button.clicked.connect(self.open_file)  #the open_file method is called upon when the button is clicked
        self.layout.addWidget(self.table_button) #adds the button to the main window
        self.table_button.setStyleSheet("background-color: #000000; color: white;") #background colour

        self.table = QTableWidget(self) #creates a table using the QTableWidget widget
        self.table.setStyleSheet("background-color: #fbfcfc;") #background colour
        self.layout.addWidget(self.table) #adds the table to the main window
        
        #horizontal layout at the bottom:
        bottom_layout = QHBoxLayout()

        # Create the QListWidget with updated size and font
        self.list_widget = QListWidget()# creating a list widget
        #adding items to the list:
        self.list_widget.addItem("Line Graph - Consumption & Production")
        self.list_widget.addItem("Scatter Graph - Consumption vs Production")
        self.list_widget.addItem("Box Graph - Production Variability by Type")
        self.list_widget.setFixedHeight(200)  # height of the list
        self.list_widget.setMaximumWidth(900)  # width of the list
        self.list_widget.setFont(QFont('Calibri', 10))  # font and foct size of the list
        self.list_widget.setStyleSheet("background-color: #000000; color: white;")#bg colour
        bottom_layout.addWidget(self.list_widget) #the list_widget is added ti the bottom_layout and will be displayed according to the QHBoxLayout

        # Adding stretch factor to allow the list to expand if necessary
        bottom_layout.addStretch()


        self.radio_layout = QVBoxLayout()  # vertical layout for radio buttons
        self.line_radio = QRadioButton("Line Graph") #radio button for line graph witht the label Line Graph.
        self.line_radio.setChecked(True)  # selected by default
        self.radio_layout.addWidget(self.line_radio) #adds the button to the main window

        self.scatter_radio = QRadioButton("Scatter Plot") #radio button for scatter graph
        self.radio_layout.addWidget(self.scatter_radio) #adds the button to the main window

        self.box_radio = QRadioButton("Box Plot") #radio button for box plot
        self.radio_layout.addWidget(self.box_radio)#adds the button to the main window

        bottom_layout.addLayout(self.radio_layout)# adds the radio_layout which contains the radio buttons to the bottom_layout
        self.layout.addLayout(bottom_layout)  # Add radio buttons to the main layout


        self.setLayout(self.layout)  #organises the widgets according to the layout set at the start using QVBoxLayout

        self.content = None #variable to store data loaded from the CSV file assigned a none value

    def create_menu(self): #method for creating the menu
        menubar = QMenuBar(self) #using the QMenuBar class to initialize the menu bar
        menubar.setStyleSheet("QMenuBar { background-color: white; }")  # Set the menu bar background to white
        file_menu = menubar.addMenu('File') #using the addmenu method to add a file menu to the menu bar

        #adding actions to the file menu
        
        #save_action = QAction('Save', self) #creates a new action called save
        save_action = QAction(QIcon("icons/save_icon.png"), 'Save', self)
        save_action.triggered.connect(self.save_file) #when the save_action is triggered the save_file method will be called
        file_menu.addAction(save_action) #adds the action to the menu
        
        exit_action = QAction('Exit', self) #creates a new action called exit
        exit_action.triggered.connect(QApplication.quit) #when the exit_action is triggered the quit method of the QApplication class will be called
        file_menu.addAction(exit_action)#adds the action to the menu
        
        self.layout.setMenuBar(menubar) #setting the menu bar layout

    def open_file(self): #method for loading a file from the user 
        fname, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)") 
        #opens a file dialog that lets the user select a file from their file system to return a tuple with the file path and filter.
        # the _ is used to ignore the second value fo the tuple, the filter since we only need the first value i.e, the path
        if fname: #if the file is opened, i.e, fname is not empty
            try:
                self.content = pd.read_csv(fname) #the content dataframe(a dataframe is returned by default) now stores the contents of the file opened using pandas
                #pd.read_csv is a Pandas function specifically designed to read CSV files and return a DataFrame.
                self.tabular_data() #calling upon the tabular_data() method to display the file data that has been read in a table
                self.plot_button.setEnabled(True)  # Enable the plot button after loading the file
            except FileNotFoundError: #if the file does not open the FileNotFoundError is raised
                QMessageBox.critical(self, "Error", "File not found") #an icon indicating that the message represents a critical problem
            except pd.errors.EmptyDataError: #if the file has no data
                QMessageBox.critical(self, "Error", "No data: Empty CSV file")
            except pd.errors.ParserError: #incase of parsing error: Parsing errors can occur due to various reasons, such as malformed CSV content, incorrect delimiters, or unexpected end of data.
                QMessageBox.critical(self, "Error", "Parsing error: Invalid CSV file")

    def save_file(self): #method for saving the file in tabular format
            if self.content is not None:#if there is data read and stored from the csv file in the self.content dataframe.
                fname, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)") 
                #opens a file dialog that lets the user choose a location and name for saving the file
                if fname:#if the file is opened, i.e, fname is not empty
                    self.content.to_csv(fname, index=False) #saves the content dataframe to the file path specified by fname
                    # index=False specifies that the index of the DataFrame should not be written to the CSV file.
            else:
                QMessageBox.warning(self, "Warning", "No data to save")

    def tabular_data(self): #defines a method for creating the table
        if self.content is not None: #if there is data read and stored from the csv file in the self.content dataframe.
            #self.table calles upon the QTableWidget
            #self.content.shape returns a tuple containing the number of rows and columns in the dataframe resepctively.
            self.table.setRowCount(self.content.shape[0]) #the 0th index of the tuple gives the number of rows, this no. is used in the table,
            # its set using setRowCount.
            self.table.setColumnCount(self.content.shape[1]) #the 1st index of the tuple gives the number of columns, 
            #this no. is used in the table, its set using setColumnCount.

            self.table.setHorizontalHeaderLabels(self.content.columns) #setting the column headers in the table horizontally.

            #The iterrows() method generates an iterator object of the DataFrame, allowing us to iterate each row in the DataFrame.
            """Outer Loop: Iterating Over Rows"""
            for i, row in self.content.iterrows(): #iterrows iterates over the dataframe's rows and produces index and row pairs as a series.
                #i is the row index, and row is a Series object representing the row's data.
                """Inner Loop: Iterating Over Values in the Row"""
                for j, value in enumerate(row): #enumerate is used on the Series object (row) to get the column index (j) and the value
                    # at that column.
                    self.table.setItem(i, j, QTableWidgetItem(str(value))) #creates a new table widget item with the string 
                    #representation of the value
                    #places the item in the QTableWidget at the row i and column j.


    def generate_plot(self): #method for generating plot
        if self.content is not None: 
            if self.line_radio.isChecked(): #if the line graph button is selected
                self.content.set_index('DateTime')[['Consumption', 'Production']].plot() #datetime is set as the index. 
                #only.plot() is used as it is the default graph
                #a plot of comsumption and production is produced using the pandas plot function.
                plt.ylabel('MegaWatts') #the y axis label
                plt.title('Consumption and Production Over Time') #title of the plot
            elif self.scatter_radio.isChecked(): #if the scatter graph button is selected
                plt.scatter(self.content['Consumption'], self.content['Production']) #using plt.scatter because the scatter plot function is not built into the pandas plot method directly.
                plt.xlabel('Consumption (MW)') #x axis heading
                plt.ylabel('Production (MW)')
                plt.title('Consumption vs Production')
            elif self.box_radio.isChecked(): #if the box graph button is selected
                #plot of all the columns
                #specifiying the kind of plot within the .plot property
                self.content[['Nuclear', 'Wind', 'Hydroelectric', 'Oil and Gas', 'Coal', 'Solar', 'Biomass']].plot(kind='box') 
                plt.ylabel('MW')
                plt.title('Production Variability by Type')
            plt.show() #displays the plot in a window using Matplotlib's show function.



def main(): #defines a function called main
    app = QApplication(sys.argv) #creating an instance of the QApplication class. 
    #It is responsible for initializing the underlying GUI library and handling the main event loop of the application.
    # the sys.argv list is passed to QApplication
    ex = MainWindow() #creates an instance of the main window class
    ex.show() #makes the main window visible on the screen.
    sys.exit(app.exec_()) #app.exec_() keeps the application running, sys.exit() ensures the application exits cleanly when the event loop finishes.

if __name__ == '__main__': #checks if the script is being run as the main module (not imported as a module). 
    main() #If so, it calls the main class to start the application
