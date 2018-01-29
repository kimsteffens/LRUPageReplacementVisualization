#! /usr/bin/env python
import collections

'''
This file contains the model functionality. It provides the logic behind the
LRU replacement system. There are two classes:
processPCB: the object used to house information about a process (page table, size, etc.)

memoryManager: the driving force behind the paging system. It contains the main functionality of placing pages into
physical memory and how to decide when/how to replace them.

@author Kim Steffens
@version 30 November 2017
'''

# A processPCB objects simulates a sort of "PCB" that stores information for the process.
# Here, the page table is store, size, number of faults/references, and the process' number is stored.
class ProcessPCB(object):

    def __init__(self, processName):
        # stores size of the process (in number of pages). Max is 64.
        self.size = 0

        # stores number of faults caused by pages of this process
        self.numFaults = 0

        # stores number of references to pages in this process
        self.numReferences = 0

        # stores the process number (i.e. if P1, myNum = P1)
        self.myName = processName

        # page table is a dictionary in the form page#:frame#
        self.pageTable = {}

    # insert a page into the page table
    def insertPage(self, page):
        self.pageTable[page] = None
        self.size = self.size + 1
        if self.size > 64:
            print("Warning! Process is over recommended size.")

    # give a frame # to a page
    def insertFrame(self, page, frame):
        self.pageTable[page] = frame

    # take away a frame from a page
    def removeFrame(self, page):
        self.pageTable[page] = None

    # increment references for this process
    def reference(self):
        self.numReferences = self.numReferences + 1

    # increment faults for this process
    def incrementFaults(self):
        self.numFaults = self.numFaults + 1

# The primary functionality behind the LRU simulation
class MemoryManager(object):

    def __init__(self, fileName):

        # stores whether a fault has just occured
        self.isFault = False

        # stores current victim
        self.victim = None

        # stores current line of the file
        self.currentLine = None

        # counters for faults/references
        self.numFaults = 0
        self.numReferences = 0

        # an array containing all processes' PCBs. In format pid:PCB
        self.processTable = {}

        # free-frame list: initially all frames are free
        self.freeFrames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        # queue of recently referenced pages
        self.recentlyReferencedPages = []

        # frame table is dictionary of arrays of the format frame#:[process# page#]
        self.frameTable = {}.fromkeys([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        # open the file for reading
        self.referenceString = open(fileName, "r")

    # read line of file and act upon it
    def readLine(self):

        my_line = self.referenceString.readline()

        # if line is empty, eof is reached
        if my_line == "":
            self.closeFile()
            return False

        # get process name (all text up until ':")
        my_process = my_line.partition(":")[0]


        # get page
        myPage = "".join(my_line.partition(":")[2].split())
        self.currentLine = my_process + ": " + myPage

        # reference the page
        self.referencePage(my_process, myPage)

        return True

    # reference a page
    def referencePage(self, process, page):

        # add this process to the process table if neccessary
        if process not in self.processTable:
            self.processTable[process] = ProcessPCB(process)

        # add page to process' page table if necessary
        if page not in self.processTable[process].pageTable:
            self.processTable[process].insertPage(page)

        # increment references
        self.processTable[process].reference()
        self.numReferences = self.numReferences + 1

        # storage format in recentlyReferencedPages etc.
        processStr = "" + process + " " + page

        #  check if faulted and if need to find a victim, or if can just reference normally
        if processStr in self.recentlyReferencedPages:
            self.victim = None
            # move to front of queue
            self.recentlyReferencedPages.insert(0, self.recentlyReferencedPages.pop(
                self.recentlyReferencedPages.index(processStr)))
        else:
            self.numFaults = self.numFaults + 1
            self.processTable[process].incrementFaults()

            # check if free-frame list is empty, take a used frame if necessary
            if not self.freeFrames:
                self.replaceVictim(process, page)

            # give the frame to this page
            myFrame = self.freeFrames[0]
            self.freeFrames.pop(0)
            self.processTable[process].insertFrame(page, myFrame)
            self.frameTable[myFrame] = "" + process + " " + page
            self.recentlyReferencedPages.insert(0, processStr)

    # choose a victim to remove from physical memory
    def replaceVictim(self, process, page):

        # delete back of recentlyReferencedPages
        deleted_page = self.recentlyReferencedPages.pop(15)
        self.victim = deleted_page
        deleted_frame = None

        # find frame to be used for new process/page
        for myKey, myEntry in self.frameTable.items():
            if deleted_page == myEntry:
                deleted_frame = myKey

        self.freeFrames.append(deleted_frame)
        self.processTable[deleted_page.split(" ")[0]].removeFrame(deleted_page.split(" ")[1])

    # closes file
    def closeFile(self):
        self.referenceString.close()

        # print some last items for verification purposes
        print("Free-frame list: ", self.freeFrames)
        print("Recently used pages: ", self.recentlyReferencedPages)
        print("Process Table: ", self.processTable)
        print("Frame table: ", self.frameTable)

    # run until a fault is encountered.
    def runUntilFault(self):
        my_faults = self.numFaults
        while self.numFaults == my_faults:

            # if eof
            if not self.readLine():
                return False
        return True


    # run all the way through the file, no stopping
    def runToEnd(self):

        while self.readLine():
            pass

