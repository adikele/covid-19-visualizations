# covid-19-visualizations
By Aditya Kelekar, dt:1.8.2020, rev: 17.8.2020

PROJECT PLAN:
Stage 1 (completed 1.8.2020): covid19CountriesAndCases.py 
Country bar graphs for a fixed date 

Stage 2 (completed 12.8.2020): covid_bargraphs.py
Country bar graphs for a fixed date: reformatted version of covid19CountriesAndCases.py with functions performing specific tasks 

Stage 3 (completed 17.8.2020): covid_linegraphs.py
Country line graphs the rise or decline of Covid-19 infections in a user-entered country + 4 other random countries

Stage 4 (in the works): 
(i) Country plots showing growth/decline of cases reported over for user-entered time period 
(ii) A GUI interface
(iii) APIs for this project

PROJECT DESCRIPTION:
Programs to display Covid-19 data taking its source from a .csv file with worldwide figures. 

1. covid_bargraphs.py
A bar graph showing the cumulative number of new virus infections per 100000 inhabitants 
is plotted for any user-entered country. 
The cumulative number is during the 14 days prior to the compilation date of the .csv file. 
The program also shows the data for four other countries, picked randomly, 
from the same continent as the user-entered country. 

2. covid_linegraphs.py
A line graph showing the increase (or decresase) of cumulative number of new virus infections 
per 100000 inhabitants are plotted for any user-entered country. 
A time period of four months is taken: mid April to mid August 2020 
The cumulative number for any given day is calculated to indicate the 14 days prior to 
the compilation date of the .csv file. 
The program also shows the data for four other countries on the same plot.
The .csv file compilation date: 17.8.2020

SPECIFICATIONS:
1. This program uses python 3.7 and the following libraries: 
(i) matplotlib 3.3.0
(ii) pandas 1.1.0
2. Download the latest "COVID-19 cases worldwide" .csv file from 
https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data
and save it in some folder. 
Change code line 49 to provide the file path and name of your file. 

TESTS:
1. Tested for different countries by running program and manually checking ouput. 
(One bug found and corrected. Now tests run OK)

HOW TO GET IN TOUCH:
Please write to me at Adityakelekar@yahoo.com for contributions and suggestions.
Thank you!
