'''
Created on Sep 17, 2024

@author: dan
'''

from os import getcwd
from pathlib import Path
from tkinter import Tk,Button,Label,Grid,filedialog as fd
from tkcalendar import Calendar, DateEntry

if __name__ == '__main__':

    
    # Load ini file if it exists in current dir.
    print("Current working dir %s\n" % getcwd())
    lastMembersFile='None selected'
    
    # starting point 
    membersFile = lastMembersFile


    # define button action
    def get_date():
        d=startCal.get()
        print(f"Start date: {d}")
        print(f"end date: {endCal.get()}")
        
    def select_file():
        filetypes = (
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        )
    
        inidir = Path.home()
        filename = fd.askopenfilename(
            title='Select members database file',
            initialdir=inidir,
            filetypes=filetypes)
        
        if filename:
            fileNameLabel.config(text=filename)
        else:
            print("No file selected.\n")
    
    # build dialog
    root = Tk()
    
    root.geometry("400x200")
    Grid.rowconfigure(root, 0, weight=1)
    Grid.rowconfigure(root, 1, weight=1)
    Grid.rowconfigure(root, 2, weight=1)
    Grid.rowconfigure(root, 3, weight=1)
    Grid.rowconfigure(root, 4, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 1, weight=4)
    
    fileLabel = Label(root, text="Members")
    fileLabel.grid(row=1,column=0)
    fileNameLabel = Label(root, text=membersFile)
    fileNameLabel.grid(row=1,column=1)
    startLabel = Label(root, text="Start")
    startLabel.grid(row=2, column=0)
    startCal = DateEntry(root, date_pattern="yyyy-mm-dd")
    startCal.grid(row=2, column=1)
    endLabel = Label(root, text="End")
    endLabel.grid(row=3, column=0)
    endCal = DateEntry(root, date_pattern="yyyy-mm-dd")
    endCal.grid(row=3, column=1)


    btn = Button(root, text="Select members file", command=select_file).grid(row=4, column=0)
    btn = Button(root, text="Get HTML table", command=get_date).grid(row=4, column=1)
    root.mainloop()
