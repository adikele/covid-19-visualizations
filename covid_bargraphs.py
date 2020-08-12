"""
NAME: covid_bargraphs.py
By Aditya Kelekar
Dt: 12.8.2020

PROGRAM OUTPUT:
Program displays Covid-19 data taking its source from a .csv file with worldwide figures. 

User is prompted to enter the name of a country.
If entered name is not found in database, user is prompted to try again.

A bar graph showing the cumulative number of new virus infections per 100000 inhabitants 
is plotted for any user-entered country. 
The cumulative number is during the 14 days prior to the compilation date of the .csv file. 
The program also shows the data for four other countries, picked randomly, 
from the same continent as the user-entered country. 
The .csv file compilation date: 12.8.2020

Further Improvements:
1. GUI interface
2. Use of Open Data's APIs for fetching Covid-19 data
3. Web interface

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
    print("At the prompt below, enter name of a country and press enter.")
    country = input("Enter country name: ")
    return country

def input_validataion(name_country, dict_all_countries):
    '''
    Function takes name_country, a string.
    It queries the population api to check if name_country exists in database
    Function returns true if name_country exists, false otherwise
    '''
    for country_list in dict_all_countries.values():
        if name_country in country_list:
            return True
    return False


def fetch_all_countries(df): 
    ''' 
    Function finds the list of countries from all the continents
    It takes a dataframe of the input data file
    Returns a dict with keys --> continents  
                      values --> list of countries in the respective continents  
    '''
    continents = ('Africa', 'Europe', 'America', 'Oceania', 'Asia')
    dict_all_countries = dict ()
    for i in continents:
        df_current = df[(df["continentExp"] == i) & (df["dateRep"] == "28/07/2020")]
        dict_countries_current_continent = df_current.to_dict()
        list_countries_current_continent = list (dict_countries_current_continent["countriesAndTerritories"].values())
        dict_all_countries[i] = list_countries_current_continent
    return dict_all_countries


def fetch_home_continent_data(df, country_sel): 
    '''
    Function finds the countries and cases for the home continent
    It takes (i) a dataframe of the input data file (ii) a string, country_sel
    Returns two lists: (i) a list of countries (ii) a list of cases
    '''
    # determining the continent in which the selected country is situated
    dfc = df[
        (df["countriesAndTerritories"] == country_sel) & (df["dateRep"] == "28/07/2020")
    ]
    dict1 = dfc.to_dict()
    continent = list (dict1["continentExp"].values())
    continent = continent[0]

    # getting the list of countries from the same continent
    df2 = df[(df["continentExp"] == continent)  & (df["dateRep"] == "28/07/2020")]
    dict2_countries_of_a_continent = df2.to_dict()
    list_countries = list (dict2_countries_of_a_continent["countriesAndTerritories"].values())

    # extracting the number of Covid cases for the countries from the same continent
    list_cases = dict2_countries_of_a_continent[
        "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
    ].values()

    return (list_countries, list_cases)

def random_countries(df, list_countries, country_sel): 
    '''  
    Function selects 4 random countries, none of which are to be the user-selected country
    It takes (i) a dataframe of the input data file (ii) a list of countries
    (ii) a string, country_sel
    Returns a list of 4 random countries 
    '''
    list_countries_random = random.sample(list_countries, 4)
    if country_sel in list_countries_random:
        while True:
            list_countries_random = random.sample(list_countries, 4)
            if country_sel not in list_countries_random:
                break  # this way we always have 5 unique countries: 4 + 1
    return list_countries_random

def fetch_five_countries_data(dict_countries_cases, country_sel, list_countries_random): 
    '''
    Function creates a dict of countries and cases for 5 countries
    It takes (i) a dict of countries and cases (ii) a string, country_sel
    (iii) a list of 4 random countries 
    Returns a dict of countries and cases for 5 countries 
    ''' 
    dict_fivecountries = dict()
    dict_fivecountries[country_sel] = dict_countries_cases[country_sel]

    for country in list_countries_random:
        dict_fivecountries[country] = dict_countries_cases[country]

    return dict_fivecountries

# plotting countries and cases:
def plotting(countries, cases):
    x_pos = [i for i, _ in enumerate(countries)]
    plt.bar(x_pos, cases, color="blue")
    plt.xlabel("")
    plt.ylabel("Persons infected in last 14 days")
    plt.title("Cumulative number (14 days) of COVID-19 cases per 100000")
    plt.xticks(x_pos, countries)
    plt.show()

def main():
    # NOTE: change file path as per your own file path.
    df = pd.read_csv(
        "/Users/bajya/Documents/07python_programs/08covid/EUOpenData_2020_08_12"
    )

    while (1):
        country_sel = read_input()
        dict_all_countries = fetch_all_countries (df)
        if input_validataion(country_sel, dict_all_countries):
            break
        else:
            print("Country name not in database, please try again.")
            print("-----------------------------")

    list_countries, list_cases = fetch_home_continent_data(df, country_sel)

    dict_continent = dict(zip(list_countries, list_cases)) 

    list_countries_random = random_countries(df, list_countries, country_sel)

    dict_fivecountries = fetch_five_countries_data(dict_continent, country_sel, list_countries_random)

    x = dict_fivecountries.keys()
    y = dict_fivecountries.values()

    plotting(x, y)


main()
