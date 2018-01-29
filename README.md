# LRUPageReplacementVisualization
A small program to help visualize an LRU page replacement algorithm for a plain text file containing a reference string of pages.

## Files and Program Structure
My program consists of two python files: View.py and MemoryManager.py.

#### MemoryManager.py:
MemoryManger.py further contains two classes, MemoryManager and ProcessPCB:

**MemoryManager:** MemoryManager contains the logic behind the paging and LRU page replacement system as a whole. It is where the file is read, references are processed, and activity such as page replacement takes place. It stores various information throughout the reading of the reference string in the file:

  1.	Free-free list (freeFrames): the list of frames that are currently available for use
  2.	Number of faults (numFaults)/ number of references (numReferences) in total
  3.	Process table (processTable): a dictionary of each process in the format Process # : ProcessPCB object
  4.	Recently referenced pages (recentlyReferencedPages): a list of the 16 pages that have been used most recently. Each time a page is reference it moves to the front of the list (position 0). This list provides the basis for the LRU algorithm: whichever page is in position 15 will be the victim, because that will be the least recently used page that is currently in memory.
  5.	Frame table (frameTable): a dictionary containing the contents of physical memory in the format Frame#: Process# Page#
  6.	Items such as the current line of the file and the current victim (if applicable)

The LRU algorithm: The LRU algorithm simply checks whether or not a page needs to be replaced (if the free frame list is empty and if the page is not in the recently used pages), then chooses the 15th element of the recently referenced pages list to find the least recently used item to remove (if necessary).  If there is room in physical memory, then of course choosing a victim is not necessary and the page is simply placed in a free-frame.

 Following this, any updates to the process’ page table or any of the MemoryManager’s tracked variables are implemented (such as number of faults, any table updates, etc.).

**ProcessPCB:** ProcessPCB is my implementation of the PCB. Each process read in from the file will become its own ProcessPCB object. This object contains information on the size of process (in pages), the number of references/faults caused by this process, and the process’ page table (containing mappings from page numbers to frame numbers).

#### View.py
The View file contains functionality for the GUI, as well as control of a MemoryManagement object. It is from this file that the full program is started up using Python’s “main” (if __name__ == '__main__'). 

First, a pop-up box will appear to the user, in order for them to choose a file containing the reference string. Then, if a valid file is provided, the GUI will start up and the user has the choice of going through the program by clicking a “next” button, a button to run until the next fault, and a button to run fully to completion. Throughout the running of the file, the user can track statistics and physical memory contents, such as:

  1.    The number of faults/references in total
  2.     The current process/page being referenced
  3.     The current victim (if applicable)
  4.     The contents of physical memory (in the format: Frame #: Process Page)
  5.      The contents of the processes' "PCB"s: their page tables (in the format: Page#: Frame#), number of faults/references, and sizes of the process (in pages). A process can be chosen to view by selecting it from the drop-down box.
  
Once the file is finished being read, then the buttons disable and the user can finish viewing any statistics of interest.
