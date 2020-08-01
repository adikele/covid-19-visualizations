"""
NAME: Covid-19 - Country-cases Bar Plots
By Aditya Kelekar, dt:1.8.2020

TESTS:
1. Tested for different countries. (One bug found and corrected. Now tests run OK)

PROGRAM DESCRIPTION:
Program displays Covid-19 data taking its source from a .csv file with worldwide figures. 
A bar graph showing the cumulative number of new virus infections per 100000 inhabitants 
is plotted for any user-entered country. 
The cumulative number is during the 14 days prior to the compilation date of the .csv file. 
The program also shows the data for four other countries, picked randomly, 
from the same continent as the user-entered country. 

SPECIFICATIONS:
1. This program uses python 3.7 and the following libraries: 
(i) matplotlib 3.3.0
(ii) pandas 1.1.0

2. Download the latest "COVID-19 cases worldwide" .csv file from 
https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data
and save it in some folder. 
Change code line 49 to provide the file path and name of your file. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import random


def read_input():
    print("Program plots the number of Covid-19 infections of a user-entered country")
    print(
        "(the cumulative number of cases per 100000 inhabitants recorded during the 14 days.."
    )
    print("prior to the compilation date of the .csv file)")
    print(".csv file compilation date: 30.7.2020")
    print("------------------------------------------------------")
    print("At the prompt below, enter name of a country and press enter.")
    name_country = input("Enter country name: ")
    return name_country


country_sel = read_input()

# NOTE: change file path as per your own file path.
df = pd.read_csv(
    "/Users/bajya/Documents/07python_programs/10pyqtgraph/corona_2020_07_30"
)

# determining the continent in which the selected country is situated:
dfc = df[
    (df["countriesAndTerritories"] == country_sel) & (df["dateRep"] == "28/07/2020")
]
dict1 = dfc.to_dict()
continent = dict1["continentExp"].values()

# could there be a simpler way to recover continent name?
# the continent name is in dict1 ["continentExp"].values()
continent_name = []
for i in continent:
    continent_name.append(i)
continent_string = continent_name[0]

# extracting the countries from the same continent as the selected country:
df2 = df[(df["continentExp"] == continent_string) & (df["dateRep"] == "28/07/2020")]
dict2_countries_of_a_continent = df2.to_dict()
list_countries = dict2_countries_of_a_continent["countriesAndTerritories"].values()

# extracting the number of Covid cases for the countries from the same continent:
list_cases = dict2_countries_of_a_continent[
    "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
].values()

# putting the countries with their respective number of cases in a dict
dict3_countries_and_cases = dict(zip(list_countries, list_cases))

# converting the list_countries (which are actually not in a list form) to a list
countries_list = []
for i in list_countries:
    countries_list.append(i)

# taking 4 random countries, none of which should be the selected country:
list_countries_random = random.sample(countries_list, 4)
if country_sel in list_countries_random:
    while True:
        list_countries_random = random.sample(countries_list, 4)
        if country_sel not in list_countries_random:
            break  # this way we always have 5 unique countries: 4 + 1

# creating a dict of countries and cases for the 5 countries
dict4_random = dict()
dict4_random[country_sel] = dict3_countries_and_cases[country_sel]
for country in list_countries_random:
    dict4_random[country] = dict3_countries_and_cases[country]

x = dict4_random.keys()
y = dict4_random.values()

# plotting countries and cases:
def plotting(countries, cases):
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color="blue")
    plt.xlabel("")
    plt.ylabel("Persons infected in last 14 days")
    plt.title("Cumulative number (14 days) of COVID-19 cases per 100000")
    plt.xticks(x_pos, x)
    plt.show()


plotting(x, y)
