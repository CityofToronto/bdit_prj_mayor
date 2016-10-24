# Gardiner Acceleration Delay Savings
## Overall Methodology
Total delay cost savings are calculated as a function of three parameters:
* Total vehicle-hours saved (detailed below);
* Vehicle occupancy (assumed to be 1.365 persons/vehicle) based off of the 2011 Transportation Tomorrow Survey
* Value of time (assumed to be $15/hr based on values used in recent Metrolinx studies ($15.54/hr and $16.71/hr))

Significant efforts were made to control for time-of-day and seasonality effects in comparisons between traffic conditions during construction and “normal” periods, where possible.

* Segment __time-of-day delay profiles__ were derived using the difference in average travel times during construction conditions and normal conditions.
* Segment __volume delay profiles__ were derived using traffic count data from periods of normal conditions extracted from the City’s traffic volume database, where available.
* An estimate for daily vehicle-hours saved was calculated using __time-of-day delay__ and __volume profiles__ (by hour) for each segment within the study area, for three different day types (Weekday, Saturday, and Sunday/Holiday).
* __Daily vehicle-hours__ saved estimates were then expanded to overall vehicle-hours saved using the frequency of each day type in the period opened up under the accelerated schedule.

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

## Time of day delay profiles
There are two sources of travel time data: Bluetooth and Inrix. 
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

* Segment travel times are collected as average times of 15min bins. 
* Travel time hourly profiles are constructed for both phases and for construction and normal travel conditions. Mean travel times are calculated instead of median across dates and 4 15min bins in an hour to reflect reliability.
* Time of day delay profile was derived using difference in the averages in construction and normal conditions.
* Dates where Gardiner/Lakeshore are closed for special events are taken out of consideration.

## Volume
the headings are as follows:  

arterycode|count_date|time_count|count|dow|
----------|----------|----------|-----|---|

Volume data are collected from loop detectors to reflect traffic volume under normal conditions. 
* Gardiner: April 22, 2012 to June 28, 2012*
* Lakeshore: April 22, 2015 to June 28, 2015

*Gardiner detectors are taken away during first half of 2015 and data does not exist for the same period in 2013.

* Volume is stored in the database as counts in 15min bins at point locations. 
* Volume count stations (identified by arterycode) is matched up to segments defined by the segmentation of travel time dataset. For a particular segment on a particular date and 15min bin, the median of all locations is taken as the volume.
* 15min bins are then summed into hourly bins. Hourly volume is taken as the median volume of the identified dates stated above. 

