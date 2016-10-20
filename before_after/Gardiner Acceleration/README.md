# Gardiner Acceleration Delay Savings

## Construction Timeline

Phase|Start Date    |Proposed End Date|Accelerated End Date|Segment             |Condition                  |
-----|--------------|-----------------|--------------------|--------------------|---------------------------|
1    |April 28,2014 |June 29, 2015    |April 22, 2015      |Park Lawn to Jarvis |1 lane closed per direction|
2    |August 19,2015|October 24, 2016 |June 21, 2016       |Jameson to Strachan |1 lane closed per direction|

Study Period: (chosen to control seasonality)  

Phase|Road Name|Construction                  |Normal                        |
-----|---------|------------------------------|------------------------------|
1    |Gardiner |April 28,2014 - June 28, 2014 |April 22, 2015 - June 28, 2015|
1    |Lakeshore|Sept 20,2014 - Nov 20, 2014*  |April 22, 2015 - June 28, 2015|
2    |Gardiner |August 19,2015 - Sept 30, 2015|June 22, 2016 - Sept 30, 2016 |
2    |Lakeshore|August 19,2015 - Sept 30, 2015|June 22, 2016 - Sept 30, 2016 |
*compromised dates because of data availability

## Travel Times
There are two sources of travel time data available: Bluetooth and Inrix. 
In this case, bluetooth data is used for delay calculations because of its availability. At the point when this analysis is done, Inrix data is updated till end of June 2016.

Segments under analysis:  

Road     |Segment             |Direction|
---------|--------------------|---------|
Gardiner |Grand - Dufferin    |EB,WB    |
		 |Dufferin - Spadina  |EB,WB    |
		 |Spadina - Parliament|EB,WB    |
Lakeshore|Grand - Ellis       |EB       |
		 |Ellis - Dufferin    |EB,WB    |
		 |Dufferin - Strachan |EB,WB    |
		 |Strachan - Bay      |EB       |

the headings are as follows:  

segment_id|timestamp|travel_time|dow|
----------|---------|-----------|---|

segment travel times are collected as average times of 15min bins. 
travel time hourly profiles are constructed for both phases and for construction and normal travel conditions. Mean travel times are calculated instead of median across dates and 4 15min bins in an hour to reflect reliability.

Dates where Gardiner/Lakeshore are closed for special events are taken out of consideration.

## Volume
the headings are as follows:  

arterycode|count_date|time_count|count|dow|
----------|----------|----------|-----|---|

Volume data are collected from loop detectors to reflect traffic volume under normal conditions. 
Gardiner: April 22, 2012 to June 28, 2012*
Lakeshore: April 22, 2015 to June 28, 2015
*Gardiner detectors are taken away during first half of 2015 and data does not exist for the same period in 2013.

Volume is stored in the database as counts in 15min bins at point locations. 
Volume count stations (identified by arterycode) is matched up to segments defined by the segmentation of travel time dataset. For a particular segment on a particular date and 15min bin, the median of all locations is taken as the volume.
15min bins are then summed into hourly bins. Hourly volume is taken as the median volume of the identified dates stated above. 

## Delay

Delay for each segment is calculated as (normal travel time - construction travel time) * volume and has the unit of vehicle-hours. 
