#! /usr/bin/env python

from MemoryManager import MemoryManager
import sys
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QApplication, QWidget, QPushButton, QInputDialog, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

'''
This file contains the control and view functionalities. It first starts out by asking the user for a file
containing the reference string. The GUI then shows:
1. number of faults/references total
2. the current process/page being referenced
3. the current victim (if applicable)
4. the contents of physical memory
5. the contents of the processes' "PCB"s: their page tables, number of faults/references, and sizes

The GUI design is driven by mouse clicks to buttons (to run to completion, to next fault, or next line of code),
as well as clicks to select the process to display. 

@author Kim Steffens
@version 30 November 2017
'''
class View(QWidget):

    # set up basic window
    def __init__(self):

        super().__init__()
        self.title = 'LRU Page Replacement Visualization'

        # size the window
        self.left =100
        self.top = 100
        self.width = 1500
        self.height = 900

        # ask user for file
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter the file to use:')
        self.filename = text
        self.memManager = MemoryManager(self.filename)
        self.initUI()

        windowLayout = QVBoxLayout()

        self.setLayout(windowLayout)

    # create the GUI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # lables for references/faults/current line in file/ victim
        self.total_refs_label = QLabel('Total References:       ', self)
        self.total_refs_label.move(15, 10)

        self.total_faults_label = QLabel('Total Faults:       ', self)
        self.total_faults_label.move(15, 40)

        self.current_proc_label = QLabel('Current Process/Page:                            ', self)
        self.current_proc_label.move(15, 70)

        self.victim_label = QLabel('Victim:                  ', self)
        self.victim_label.move(500, 70)


        # show physical memory contents at all times
        self.physical_mem_label = QLabel("Physical Memory Contents:", self)
        self.physical_mem_label.move(500, 170)
        self.frame0_label = QLabel('Frame 0:                      ', self)
        self.frame0_label.move(500, 200)
        self.frame1_label = QLabel('Frame 1:                      ', self)
        self.frame1_label.move(500, 230)
        self.frame2_label = QLabel('Frame 2:                      ', self)
        self.frame2_label.move(500, 260)
        self.frame3_label = QLabel('Frame 3:                       ', self)
        self.frame3_label.move(500, 290)
        self.frame4_label = QLabel('Frame 4:                       ', self)
        self.frame4_label.move(500, 320)
        self.frame5_label = QLabel('Frame 5:                       ', self)
        self.frame5_label.move(500, 350)
        self.frame6_label = QLabel('Frame 6:                        ', self)
        self.frame6_label.move(500, 380)
        self.frame7_label = QLabel('Frame 7:                        ', self)
        self.frame7_label.move(500, 410)
        self.frame8_label = QLabel('Frame 8:                        ', self)
        self.frame8_label.move(500, 440)
        self.frame9_label = QLabel('Frame 9:                        ', self)
        self.frame9_label.move(500, 470)
        self.frame10_label = QLabel('Frame 10:                       ', self)
        self.frame10_label.move(500, 500)
        self.frame11_label = QLabel('Frame 11:                        ', self)
        self.frame11_label.move(500, 530)
        self.frame12_label = QLabel('Frame 12:                        ', self)
        self.frame12_label.move(500, 560)
        self.frame13_label = QLabel('Frame 13:                        ', self)
        self.frame13_label.move(500, 590)
        self.frame14_label = QLabel('Frame 14:                         ', self)
        self.frame14_label.move(500, 620)
        self.frame15_label = QLabel('Frame 15:                         ', self)
        self.frame15_label.move(500, 650)

        # combo box for processes that may be displayed
        self.combo_box_label = QLabel("Choose Process to display:", self)
        self.combo_box_label.move(50, 170)
        self.combo_box = QComboBox(self)
        self.combo_box.move(50, 200)
        self.combo_box.activated[str].connect(self.showProcessPCB)

        # text area to display "PCB" of a process (select process from combo box)
        self.processPCB = QPlainTextEdit(self)
        self.processPCB.insertPlainText("Process PCB and Table: \n")
        self.processPCB.setReadOnly(True)
        self.processPCB.move(250, 170)
        self.processPCB.resize(200, 500)

        # button to run to completion
        self.run_to_completion_button = QPushButton('To Completion', self)
        self.run_to_completion_button.setToolTip('Run through all references')
        self.run_to_completion_button.move(100, 100)
        self.run_to_completion_button.clicked.connect(self.run_through_end)

        # button to go to next line in file
        self.run_to_next_button = QPushButton('Next', self)
        self.run_to_next_button.setToolTip('Read next reference')
        self.run_to_next_button.move(260, 100)
        self.run_to_next_button.clicked.connect(self.run_next)

        # button to run until a fault
        self.run_to_fault_button = QPushButton('Next Fault', self)
        self.run_to_fault_button.setToolTip('Read until a page fault')
        self.run_to_fault_button.move(420, 100)
        self.run_to_fault_button.clicked.connect(self.run_to_fault)

        self.show()

    # displays the contents of the process' "PCB"
    def showProcessPCB(self):
        self.processPCB.clear()
        # process to use
        myProc = str(self.combo_box.currentText())

        # basic stats
        self.processPCB.insertPlainText("Process PCB and Table: \n")
        self.processPCB.insertPlainText("Size in pages: " + str(self.memManager.processTable[myProc].size))
        self.processPCB.insertPlainText("\nNumber of References: " + str(self.memManager.processTable[myProc].numReferences))
        self.processPCB.insertPlainText("\nNumber of Faults: " + str(self.memManager.processTable[myProc].numFaults))

        # print out the page table dictionary
        self.processPCB.insertPlainText("\nPage Table: \n Page\tFrame\n ")
        for key, value in self.memManager.processTable[myProc].pageTable.items():
            self.processPCB.insertPlainText(str(key) + "\t" + str(value) + "\n")

    # to be run at eof. Disables buttons.
    def endAll(self):
        self.run_to_fault_button.setEnabled(False)
        self.run_to_next_button.setEnabled(False)
        self.run_to_completion_button.setEnabled(False)

    # updates the UI with new stats
    def updateUI(self):

        # set combo box options
        self.combo_box.clear()
        for proc in self.memManager.processTable:
            self.combo_box.addItem(str(proc))

        self.showProcessPCB()

        # set basic stats
        self.total_refs_label.setText("Total References: " + str(self.memManager.numReferences)+ "     ")
        self.total_refs_label.repaint()
        self.total_faults_label.setText("Total Faults: " + str(self.memManager.numFaults)+ "     ")
        self.total_faults_label.repaint()

        self.current_proc_label.setText("Current Process/Page: " + str(self.memManager.currentLine) + "            ")
        self.current_proc_label.repaint()
        self.victim_label.setText("Victim: " + str(self.memManager.victim) + "      ")
        self.victim_label.repaint()

        # set physical memory contents
        self.frame0_label.setText("Frame 0: " + str(self.memManager.frameTable[0])+ "     ")
        self.frame1_label.setText("Frame 1: " + str(self.memManager.frameTable[1])+ "     ")
        self.frame2_label.setText("Frame 2: " + str(self.memManager.frameTable[2])+ "     ")
        self.frame3_label.setText("Frame 3: " + str(self.memManager.frameTable[3])+ "     ")
        self.frame4_label.setText("Frame 4: " + str(self.memManager.frameTable[4])+ "     ")
        self.frame5_label.setText("Frame 5: " + str(self.memManager.frameTable[5])+ "     ")
        self.frame6_label.setText("Frame 6: " + str(self.memManager.frameTable[6])+ "     ")
        self.frame7_label.setText("Frame 7: " + str(self.memManager.frameTable[7])+ "     ")
        self.frame8_label.setText("Frame 8: " + str(self.memManager.frameTable[8])+ "     ")
        self.frame9_label.setText("Frame 9: " + str(self.memManager.frameTable[9])+ "     ")
        self.frame10_label.setText("Frame 10: " + str(self.memManager.frameTable[10])+ "     ")
        self.frame11_label.setText("Frame 11: " + str(self.memManager.frameTable[11])+ "     ")
        self.frame12_label.setText("Frame 12: " + str(self.memManager.frameTable[12]) + "     ")
        self.frame13_label.setText("Frame 13: " + str(self.memManager.frameTable[13]) + "     ")
        self.frame14_label.setText("Frame 14: " + str(self.memManager.frameTable[14]) + "     ")
        self.frame15_label.setText("Frame 15: " + str(self.memManager.frameTable[15]) + "     ")


    # button click actions for run to completion
    @pyqtSlot()
    def run_through_end(self):
        self.memManager.runToEnd()
        self.updateUI()
        self.endAll()

    # button click actions for run to next line of code
    @pyqtSlot()
    def run_next(self):
        if not self.memManager.readLine():
            self.endAll()
        self.updateUI()

    # button click actions for run until a page fault
    @pyqtSlot()
    def run_to_fault(self):
        if not self.memManager.runUntilFault():
            self.endAll()
        self.updateUI()


# begins the program
if __name__ == '__main__':

    app = QApplication(sys.argv)
    begin = View()
    sys.exit(app.exec_())
