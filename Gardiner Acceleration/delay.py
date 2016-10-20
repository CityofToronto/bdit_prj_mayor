# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:00:24 2016

@author: qwang2
"""
def getatt(row):
    if row['date'] in p1c:
        #return 'construction'
        return 1
    if row['date'] in p1n:
        #return 'normal'
        return 0
    if row['date'] in p2c:
        #return 'construction'
        return 1
    if row['date'] in p2n:
        #return 'normal'
        return 0
        
def getphase(row):
    if row['date'] in p1c:
        return 1
    if row['date'] in p1n:
        return 1
    if row['date'] in p2c:
        return 2
    if row['date'] in p2n:
        return 2

def inrixgetdirc(row):
    if '+' in row['tmc'] or 'P' in row['tmc']:
        return 'Eastbound'
    else:
        return 'Westbound'
        
import pandas as pd
import matplotlib.pyplot as plt
import datetime

street = 'Gardiner'
datasource = ''   
raw = pd.read_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/'+street+'/'+datasource+'raw.csv');

holidays = pd.read_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/holiday.csv');
#day of week mapping to type of day
daytype = {1:'Weekday', 2:'Weekday', 3:'Weekday', 4:'Weekday', 5:'Weekday', 6:'Saturday', 0:'Sunday'}
#inrix - bluetooth
intoblt = {'C09-04841':41, 'C09+04842':45, 'C09-07465':41, 'C09+04843':45, 'C09-04843':41, 'C09+04844':40, 
'C09N04844':41, 'C09P04844':40, 'C09-04844':41, 'C09+04845':40, 'C09N04845':41, 'C09P04845':40, 'C09-04845':44, 
'C09+04846':42, 'C09-04387':47, 'C09+04388':46,'C09-04388':47, 'C09+04389':46,'C09-04308':47,'C09+04309':46,
'C09N04309':47,'C09P04309':46,'C09-04309':19,'C09+04310':4,'C09N04310':19,'C09P04310':4}
condition = {0:'normal', 1:'construction'}

if datasource == 'inrix_':
    if street == 'Gardiner':
        p1c = pd.date_range('2014-04-22', '2014-06-28')
        p1n = pd.date_range('2015-04-22', '2015-06-28')
        p2c = pd.date_range('2015-08-17', '2015-09-30')
        p2n = pd.date_range('2016-08-17', '2016-09-30')
    else:
        p1c = pd.date_range('2014-04-22', '2014-06-28')
        p1n = pd.date_range('2015-04-22', '2015-06-28')
        p2c = pd.date_range('2015-08-17', '2015-09-30')
        #p2n = pd.date_range('2015-04-22', '2015-06-28')
        
    raw['hour'] = raw['time_15_continuous'] // 10
    raw['dirc'] = raw.apply(inrixgetdirc, axis = 1)
    raw.rename(columns = {'dt':'date', 'tmc':'segment_id'}, inplace = True)
    raw['travel_time'] = raw['length']/raw['avg_speed'] * 60
    del raw['length']
    del raw['avg_speed']
else:
    #set start and end date
    if street == 'Gardiner':
        p1c = pd.date_range('2014-04-22', '2014-06-28')
        p1n = pd.date_range('2015-04-22', '2015-06-28')
        p2c = pd.date_range('2015-08-17', '2015-09-30')
        p2n = pd.date_range('2016-08-17', '2016-09-30')
    else:
        p1c = pd.date_range('2014-09-20', '2014-11-20')
        p1n = pd.date_range('2015-04-22', '2015-06-28')
        p2c = pd.date_range('2015-08-17', '2015-09-30')
        p2n = pd.date_range('2016-08-17', '2016-09-30')

    #convert to date time types
    raw.timestamp = pd.to_datetime(raw.timestamp);
    holidays['dt'] = pd.to_datetime(holidays.dt).dt.date
    raw['date'] = raw.timestamp.dt.date;
    raw['hour'] = raw.timestamp.dt.hour;
    del raw['timestamp']

    #convert travel time from seconds to minutes
    raw['travel_time'] = raw['travel_time']/60;

    #add direction info
    directionmap = {46:'Eastbound', 47:'Westbound', 4:'Eastbound', 19:'Westbound',5:'Eastbound', 
                    18:'Westbound', 45:'Eastbound', 41:'Westbound', 40:'Eastbound', 44:'Westbound', 
                    42:'Eastbound', 43:'Eastbound'}
    raw['dirc'] = raw['segment_id'].map(directionmap)

#get rid of outliers
raw = raw[(raw['date'] != datetime.date(2014,4,26))]
raw = raw[(raw['date'] != datetime.date(2014,4,27)) | (raw['hour'] > 11)]
raw = raw[(raw['date'] != datetime.date(2014,6,1)) | (raw['hour'] > 14) | (raw['hour'] < 5)]
raw = raw[(raw['date'] != datetime.date(2014,10,18))]
raw = raw[(raw['date'] != datetime.date(2014,10,19)) | (raw['hour'] > 15)]

raw = raw[(raw['date'] != datetime.date(2015,5,2))]
raw = raw[(raw['date'] != datetime.date(2015,5,3)) | (raw['hour'] > 4)]
raw = raw[(raw['date'] != datetime.date(2015,6,13))]
raw = raw[(raw['date'] != datetime.date(2015,6,14))]
raw = raw[(raw['date'] != datetime.date(2015,5,31)) | (raw['hour'] > 14) | (raw['hour'] < 2)]
raw = raw[(raw['date'] != datetime.date(2015,6,18))]
raw = raw[(raw['date'] != datetime.date(2015,6,19))]
raw = raw[(raw['date'] != datetime.date(2015,6,20))]
raw = raw[(raw['date'] != datetime.date(2015,6,21))]
raw = raw[(raw['date'] != datetime.date(2015,6,22))]
raw = raw[(raw['date'] != datetime.date(2015,6,23))]

#add in day_type column
raw['day_type'] = raw['dow'].map(daytype)
del raw['dow']

#change holiday day type to Sunday
raw = pd.merge(raw, holidays, left_on = 'date', right_on = 'dt', how = 'left');
raw.loc[raw.holiday.notnull(),'day_type'] = 'Sunday'
del raw['dt'];
del raw['holiday']; 
 
#create phase and normal/construction attribute
raw['status'] = raw.apply(getatt,axis = 1)
raw['phase'] = raw.apply(getphase, axis = 1)
#plot raw data (24h profile)
i = 0
temp = raw.groupby(['dirc','status','day_type','phase','date','hour','segment_id'], as_index = False).mean()
temp = temp.groupby(['dirc','status','day_type','phase','date','hour'], as_index = False).sum()
'''
for (dirc, day_type, phase, status),group in temp.groupby(['dirc','day_type','phase','status']):
    plt.figure(i)
    #check anomalies
    if dirc =='Westbound' and day_type == 'Weekday' and phase == 1 and status == 0:
        temp3 = group
        break
    temp2 = group.groupby('hour',as_index = False).mean()
    plt.plot(list(temp2['hour']), list(temp2['travel_time']), 'y', linewidth = 10, alpha = 0.7)
    plt.title(dirc+ day_type+' phase'+ str(phase)+condition[status])
    if dirc == 'Eastbound': 
        plt.ylim(0,65)
    else:
        plt.ylim(0,50)
    for (date),group2 in group.groupby(['date']):
        plt.plot(list(group2['hour']), list(group2['travel_time']))
    i = i + 1 
    plt.savefig(dirc+ day_type+ 'phase'+ str(phase)+condition[status]+'.png')
'''
'''
#save for aakash's plots
temp  = temp.groupby(['dirc','status','day_type','phase','hour'], as_index = False).mean()
del temp['segment_id']
temp.to_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/'+street+'/tt_out.csv');
'''
#----------------------Bluetooth Data Only--------------------------------#

#aggregate based on daytype, hour, segment -> mean across different dates and 15min bins
time = raw.groupby(['day_type', 'hour', 'segment_id','phase','status','dirc'], as_index = False).mean()
    
#consolidate normal and construction time in one row
grouped = time.groupby(['status'], as_index = False)
normal = grouped.get_group(0)
del normal['status']
normal.rename(columns = {'travel_time':'normal_time'}, inplace = True)
construction = grouped.get_group(1)
construction.rename(columns = {'travel_time':'construction_time'}, inplace = True)
del construction['status']

time = pd.merge(normal, construction, on = ['day_type','hour','segment_id','phase','dirc'])

'''
#plot aggregated data
i = 0
time = time.groupby(['day_type','hour','phase','dirc'], as_index = False).sum() #sum over segments

for (dirc, day_type, phase),group in time.groupby(['dirc','day_type','phase']):
    plt.figure(i)
    plt.plot(list(group['hour']), list(group['construction_time']), 'y', linewidth = 10, alpha = 0.5)
    plt.title(dirc+ day_type+' phase'+ str(phase)+'construction')
    plt.savefig(dirc+ day_type+ 'phase'+ str(phase)+'construction.png')
    i = i + 1
    plt.figure(i)
    plt.plot(list(group['hour']), list(group['normal_time']),'y', linewidth = 10, alpha = 0.5)
    plt.title(dirc+ day_type+ ' phase'+ str(phase)+'normal')
    plt.savefig(dirc+ day_type+ 'phase'+ str(phase)+'normal.png')
    i = i + 1
'''

#read volume data
volume = pd.read_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/'+street+'/volume_hour_seg_mean.csv');
if datasource == 'inrix':
    time.rename(columns = {'segment_id':'tmc'}, inplace = True)
    time['segment_id'] = time['tmc'].map(intoblt)
    
delay = pd.merge(volume, time, on = ['hour', 'segment_id','day_type','dirc'])
delay.rename(columns = {'count':'volume'}, inplace = True)

delay['delay'] = (delay['construction_time']-delay['normal_time'])*delay['volume']/60
#sum delay over 24 hours
delay = delay.groupby(['segment_id', 'day_type', 'phase','dirc'], as_index = False).sum()
