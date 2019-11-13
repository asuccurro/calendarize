#!/usr/bin/python3
#**************************************
#**    author: Antonella Succurro    **
#**email:asuccurro[AT]protonmail.com **
#**                                  **
#**    created:       2019/02/05     **
#**    last modified: 2019/02/05     **
#************************************

import json
import argparse
import csv
import random
import string
import datetime

BEGIN0='BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\n'
END0='END:VCALENDAR\n'


def main():

    args = options()
    verbose = args.verbose
    listpeople = args.listpeople.split(' ')
    
    if len(listpeople) > 1:
        splittask(args)

    return


def splittask(args):
    '''
    '''
    verbose = args.verbose
    listpeople = args.listpeople.split(' ')
    startdate = datetime.datetime.strptime(args.startdate, '%Y%m%d').date()
    enddate = datetime.datetime.strptime(args.enddate, '%Y%m%d').date()
    timerange = enddate - startdate
    period = datetime.timedelta(days=int(args.period))
    skipdates = []
    today = datetime.date.today().strftime("%Y%m%d")

    if verbose:
        print(startdate, enddate)

    for d in args.skip.split(' '):
        skipdates.append(datetime.datetime.strptime(d, '%Y%m%d').date())

    recurrentskip = eval(args.recurrentskip)
    for d in recurrentskip:
        d1 = datetime.datetime.strptime(d[0], '%Y%m%d').date()
        while d1 < enddate:
            skipdates.append(d1)
            print(d1)
            d1 = d1 + datetime.timedelta(days=d[1])
        
    if args.peopleperiod:
        period = datetime.timedelta(days=len(listpeople))

    ofiles = {}

    for p in listpeople:
        ofiles[p] = open(args.outfilename.replace('NAME', p), 'w')
        ofiles[p].write(BEGIN0)
        
    #tottasks = timerange.days - len(skipdates)

    t = 0
    while t < timerange.days:
        for p in listpeople:
            pdate, dt = checkdate(startdate + datetime.timedelta(days=t), skipdates)
            t = t + 1 + dt
            strdate = pdate.strftime("%Y%m%d")
            ofiles[p].write(f'BEGIN:VEVENT\nDTSTART;VALUE=DATE:{strdate}\nDTEND;VALUE=DATE:{strdate}\nDTSTAMP:{today}T120000\nUID:\nCREATED:{today}T120000\nDESCRIPTION:\nLOCATION:\nSEQUENCE:0\nSTATUS:CONFIRMED\nSUMMARY:{args.taskname}\nTRANSP:TRANSPARENT\nEND:VEVENT\n')

    for p in ofiles.values():
        p.write(END0)
        p.close()
        
    return

def checkdate(d, s):
    i = 0
    while d in s:
        i += 1
        d = d + datetime.timedelta(days=1)
    return d, i

def options():
    '''in-line arguments read by the parser'''
    parser = argparse.ArgumentParser(description='Parsing options')
    parser.add_argument('-V', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-P', '--peopleperiod', help='The task is equally split among the list of people', action='store_true')
    parser.add_argument('-o', '--outfilename', help='Output file name', default='../output/NAME.ics')
    parser.add_argument('-l', '--listpeople', help='List of people to share task in format "Name1 Name2"', default='Tizio Caio')
    parser.add_argument('-s', '--startdate', help='Start date in format YearMonthDay', default='20191109')
    parser.add_argument('-e', '--enddate', help='End date in format YearMonthDay', default='20191231')
    parser.add_argument('-p', '--period', help='Period for repeating task', default='7')
    parser.add_argument('-n', '--taskname', help='Name of task', default='My task')
    parser.add_argument('-r', '--recurrentskip', help='Dates to skip with recurrence in days, list of tuple format "[("YearMonthDay",14)]""', default='20191208 20191225')
    parser.add_argument('-k', '--skip', help='Dates to skip, string in format "YearMonthDay YearMonthDay"', default='20191208 20191225')
    args = parser.parse_args()
    if args.verbose:
        print('Verbosity ON')
        print(args)
    return args

if __name__=="__main__":
    main()
