'''
Created on Jul 16, 2024

@author: dan
'''




import argparse
import datetime
from operator import itemgetter
import calendar
from csv import reader

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-m", "--members", required=True, help='csv file with member list and birthdays')
    parser.add_argument('-s', "--startdate",
        help="The Start Date - format YYYY-MM-DD",
        required=True,
        type=datetime.date.fromisoformat)
    parser.add_argument('-e', "--enddate",
        help="The End Date format YYYY-MM-DD (Exclusive)",
        required=True,
        type=datetime.date.fromisoformat)
    args = parser.parse_args()
    argsdict = vars(args)
    
    # check dates
    startdate = argsdict['startdate']
    enddate = argsdict['enddate']
    
    print('start date %s month %d day %d' % (argsdict['startdate'], argsdict['startdate'].month, argsdict['startdate'].day))
    print('end date %s month %d day %d' % (argsdict['enddate'], argsdict['enddate'].month, argsdict['enddate'].day))

    ordStart = argsdict['startdate'].toordinal()
    ordEnd = argsdict['enddate'].toordinal()
    
    # check input file
    nMembers = 0
    bdays=[]
    with open(argsdict['members'], newline='') as f:
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
                bdtest = datetime.datetime.strptime(row[3], '%m/%d/%Y %H:%M:%S').date().replace(year=argsdict['startdate'].year)
                #print('%s\n', bdtest)
                if bdtest < argsdict['startdate']:
                    bdtest = bdtest + datetime.timedelta(days=365)
                    
                if bdtest >= argsdict['startdate'] and bdtest < argsdict['enddate']:
                    bdays.append((mname, bdtest))
                    #print('%s: %s' % (mname, bdtest))
                
            
    print('Found %d members' % (nMembers))
    if len(bdays)>0:
        bdays.sort(key=itemgetter(1))
    for item in bdays:
        print('<tr><td>%s</td><td>%s, %s %d</td></tr>' % (item[0], calendar.day_name[item[1].weekday()], calendar.month_name[item[1].month], item[1].day))

