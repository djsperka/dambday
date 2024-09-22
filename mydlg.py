'''
Created on Sep 17, 2024

@author: dan
'''

#Import tkinter library
from tkinter import *
from tkcalendar import Calendar, DateEntry

if __name__ == '__main__':

    from tkinter import Tk,Button
    from tkcalendar import DateEntry
    def get_date():
        selected_date = cal.get()
        print(f"Selected date: {selected_date}")
    root = Tk()
    startLabel = Label(root, text="Start").grid(row=0, column=0)
    startCal = DateEntry(root, date_pattern="yyyy-mm-dd").grid(row=0, column=1)
    endLabel = Label(root, text="End").grid(row=1, column=0)
    endCal = DateEntry(root, date_pattern="yyyy-mm-dd").grid(row=1, column=1)
    btn = Button(root, text="Click Here To Return a Date ", command=get_date).grid(row=2)
    root.mainloop()
