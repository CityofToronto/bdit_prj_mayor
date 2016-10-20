# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 16:29:44 2016

@author: qwang2
"""
import pandas as pd
import matplotlib.pyplot as plt
street = 'Gardiner'
            
def flatten(items, seqtypes=(list, tuple)):
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i+1] = items[i]
    return items
    
volumes = pd.read_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/'+street+'/volume.csv');

segnamelookup = {40:'L Ellis to Dufferin Eastbound', 41:'L Dufferin to Ellis Westbound', 42:'L Dufferin to Strachan Eastbound', 
                 43:'L Strachan to Bay Eastbound', 44:'L Strachan to Dufferin Westbound', 45:'L Grand to Ellis Eastbound', 
                 46:'G Grand to Dufferin Eastbound', 47:'G Dufferin to Grand Westbound', 4:'G Dufferin to Spadina Eastbound', 
                 19:'G Spadina to Dufferin Westbound',5:'G Spadina to Parliament Eastbound', 18:'G Parliament to Spadina Westbound'}
#add numerical time information
volumes['hour'] = pd.to_datetime(volumes['time_count']).dt.hour

#add in bluetooth data segment info
segcodelookup = {835:[45], 843: [45], 2779:[40], 853:[41], 851:[42,43], 2784:[42,43], 852:[44], 
                 850:[44], 37507:[2,3,46], 37509:[2,3,46], 25987:[2,3,46], 3179:[2,3,46], 
                 23992:[2,3,46], 3180:[20,21,47], 37508:[20,21,47], 37506:[20,21,47], 3191:[4], 
                 25984:[4], 3168:[4],23989:[4], 3169:[19], 3192:[19], 23988:[19], 23990:[19],
                 3170:[5], 3193:[5], 23985:[5],3186:[5], 3189:[5],3187:[18],3195:[18],3194:[18],
                 3190:[18],3171:[18],3185:[18]}
segmentids = pd.DataFrame(list(set(flatten(list(segcodelookup.values())))),columns = ['segment_id'])
segmentids['key'] = 1
volumes['key'] = 1
volumes = pd.merge(volumes, segmentids, on = 'key')
grouped = volumes.groupby(['segment_id', 'arterycode'])
for (segment, artery), group in grouped:
    if segment not in segcodelookup[artery]:
        volumes = volumes.drop(grouped.get_group((segment,artery)).index)
del volumes['key']
del volumes['arterycode']

#take median across count stations in one segment
volumes = volumes.groupby(['count_date','time_count','segment_id','dow'], as_index = False).median()

#sum up 15min bins to hourly
grouped = volumes.groupby(['count_date','hour','segment_id','dow'], as_index = False);
for (date, hour, segment, dow), group in grouped:
    if (len(group) != 4):
        volumes = volumes.drop(grouped.get_group((date,hour,segment,dow)).index)
volumes = grouped.sum();

#day of week mapping to type of day
daytype = {1:'Weekday', 2:'Weekday', 3:'Weekday', 4:'Weekday', 5:'Weekday', 6:'Saturday', 0:'Sunday'}
#add in day_type column
volumes['day_type'] = volumes['dow'].map(daytype)
del volumes['dow']
#change holiday day type to Sundayday
holidays = pd.read_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/holiday.csv');
volumes = pd.merge(volumes, holidays, left_on = 'count_date', right_on = 'dt', how = 'left');
volumes.loc[volumes.holiday.notnull(),'day_type'] = 'Sunday'
del volumes['dt'];
del volumes['holiday'];

# take median of all the dates for one segment at one hour on each day type
del volumes['count_date']
grouped = volumes.groupby(['hour','segment_id','day_type'], as_index = False);
result = grouped.median();

directionmap = {46:'Eastbound', 47:'Westbound', 4:'Eastbound', 5:'Eastbound', 18:'Westbound',19:'Westbound',
                45:'Eastbound', 41:'Westbound', 40:'Eastbound', 44:'Westbound', 42:'Eastbound', 43:'Eastbound'}
result['dirc'] = result['segment_id'].map(directionmap)

for (daytype,dirc), group in result.groupby(['day_type','dirc']):
    print(daytype, dirc)
    plt.figure(figsize = [10,5])
    plt.ylim(0, 7000);
    plt.title(street + daytype + dirc)
    for (seg), group2 in group.groupby('segment_id'):
        plt.plot(list(group2['hour']), list(group2['count']), label = segnamelookup[seg])   
    plt.legend(loc = 'upper left')
    plt.savefig(street + daytype + dirc + '.png')
    plt.show()


result.to_csv('C:/Users/qwang2/Documents/Gardiner Acceleration/'+street+'/volume_hour_seg_mean.csv', index = False)
#result.groupby(['segment_id', 'day_type','hour'],as_index = False).mean().groupby(['segment_id', 'day_type'], as_index = False).sum()