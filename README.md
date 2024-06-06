# garmin_run_updater
A python program to adjust workout paces and times in Garmin Connect according to progress and the weather

## Background

There is a lot to love about the Garmin ecosystem, however one area that is lacking is the ability to automatically update one's training plan which is further confounded by the lack of API access for regular users. This program is designed as a workout around to that problem. 

## How It Works

On initial use, the user provides a recent race result which is then fed into several training pace estimators which are then averaged to obtain target training paces. The program then reads in user specified workout plans and workout targets (e.g. heart rate zone or pace), and then using Selenium will log into Garmin Connect and create the workouts. On subsequent uses the program will update the workout durations, interval number, and/or pace according to whatever progression scheme the user specifies. Additionlly, if the user specifies a time of day for their run, the program will obtain meteorological data and will adjust pacing to account for wet-bulb globe temperature (WBGT) correlated performance loss, as described by Ely et al (2007).

## A Note On WBGT Adjustments And Future Project Directions

Currently, this program utilizes a simple regression fit that only considers temperature and humidity as put forth by Gagge and Nishi (1976) does not include the effects of solar radiation and wind speed. There are therefore more accurate methods for estimating WBGT, however they are significantly more complicated and the gained accuracy would yield little functional benefit for a few reasons:
1. The regression fits okay until one gets to more extreme WBGT elevations, but under such conditions training outdoors would be contraindicated.
2. It has been shown that cloud cover and solar load actually contribute very little to weather related performance differences (Ely 2007) and that weather related performance differences diminish in regards to how well trained an athlete is (Ely 2008) and the writer of this program feels fairly confident in that the group most likely to use this code would trend towards the "well trained" side of the spectrum.

But still, at some point the goal will be to update the program to use the much more comprehensive Liljegren et al methods (2008). Because they use much more detailed meteorological data this would also be a good point to add some additional functionality such as variable pacing based upon runnng route and wind direction, as well as offering optimal run time suggestions based upon factors such as allergens and air pollution.
