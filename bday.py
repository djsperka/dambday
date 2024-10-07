'''
Created on Jul 16, 2024

@author: dan
'''




import argparse
import datetime
from operator import itemgetter
import calendar
from csv import reader
from os import getcwd
from pathlib import Path
from tkinter import Tk,Button,Label,Grid,filedialog as fd
from tkcalendar import Calendar, DateEntry

def bdayHTML(membersfile, startdate, enddate):
    # check input file
    nMembers = 0
    bdays=[]
    with open(membersfile, newline='') as f:
        rdr = reader(f)
        next(rdr, None)      # skip header line
        for row in rdr:
            nMembers = nMembers+1
            
            # form name
            if len(row[1]) > 0:
                mname = row[1] + " " + row[2]
            else:
                mname = row[0] + " " + row[2]
                
            # Replace year in birthday with the year of startdate.
            # If that date is before the startdate, then use the year AFTER the year of startdate.
            # The result is the next birthday after the start date.
            if len(row[3]) > 0:
                bdtest = datetime.datetime.strptime(row[3], '%m/%d/%Y %H:%M:%S').date()
                
                # watch out for birthdays on 2/29
                if bdtest.month == 2 and bdtest.day == 29:
                    if calendar.isleap(startdate.year):
                        bdtest = bdtest.replace(year=startdate.year)
                    else:
                        bdtest = bdtest.replace(day=28, year=startdate.year)
                else:
                    bdtest = bdtest.replace(year=startdate.year)
                #print('%s\n', bdtest)
                if bdtest < startdate:
                    bdtest = bdtest + datetime.timedelta(days=365)
                    
                if bdtest >= startdate and bdtest < enddate:
                    bdays.append((mname, bdtest))
                    #print('%s: %s' % (mname, bdtest))
                
            
    #print('Found %d members' % (nMembers))
    if len(bdays)>0:
        bdays.sort(key=itemgetter(1))
    buffer='<table style="width:100%">\n'
    for item in bdays:
        #print('<tr><td>%s</td><td>%s, %s %d</td></tr>' % (item[0], calendar.day_name[item[1].weekday()], calendar.month_name[item[1].month], item[1].day))
        buffer += '<tr><td>%s</td><td>%s, %s %d</td></tr>\n' % (item[0], calendar.day_name[item[1].weekday()], calendar.month_name[item[1].month], item[1].day)
    buffer += '</table>\n'
    return buffer

def bdayDialog():

    # define button action
    def get_table():
        d0 = datetime.datetime.strptime(startCal.get(), "%Y-%m-%d").date()
        d1 = datetime.datetime.strptime(endCal.get(), "%Y-%m-%d").date()
        fname = fileNameLabel.cget("text")
        print(f"Start date: {d0}")
        print(f"end date: {d1}")
        buffer = bdayHTML(fname, d0, d1)
        print(buffer)
        
        
    def select_file():
        filetypes = (
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        )
    
        inidir = Path.home()
        membersFilename = fd.askopenfilename(
            title='Select members database file',
            initialdir=inidir,
            filetypes=filetypes)
        
        if membersFilename:
            fileNameLabel.config(text=membersFilename)
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
    fileNameLabel = Label(root, text='None selected')
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
    btn = Button(root, text="Get HTML table", command=get_table).grid(row=4, column=1)
    root.mainloop()

    
    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-m", "--members", help='csv file with member list and birthdays')
    parser.add_argument('-s', "--startdate",
        help="The Start Date - format YYYY-MM-DD",
        type=datetime.date.fromisoformat)
    parser.add_argument('-e', "--enddate",
        help="The End Date format YYYY-MM-DD (Exclusive)",
        type=datetime.date.fromisoformat)
    args = parser.parse_args()
    argsdict = vars(args)
    
    # if all args supplied
    haveAllArgs = True
    
    if argsdict['startdate'] is not None:
        startdate = argsdict['startdate']
    else:
        haveAllArgs = False
    if argsdict['enddate'] is not None:     
        enddate = argsdict['enddate']
    else:
        haveAllArgs = False
    if argsdict['members'] is not None:
        membersfile = argsdict['members']
    else:
        haveAllArgs = False
        
    if haveAllArgs:
        
        print('start date %s' % (argsdict['startdate']))
        print('end date %s' % (argsdict['enddate']))
        print('members file %s\n' % (membersfile))
        
        html = bdayHTML(membersfile, startdate, enddate)
        print(html)
    
    else:
    
        bdayDialog()
