"""
NAME: covid_linegraphs.py
By Aditya Kelekar
Dt: 17.8.2020

PROGRAM OUTPUT:
Program displays the rise or decline of Covid-19 infections in a user-entered country.
Graphs of four other countries are also plotted. These countries, picked randomly, are 
from the same continent as the user-entered country. 
The data source for the program is EU Open Data Portal's downloadable .csv file with worldwide figures. 

PROGRAM INTERACTIVITY:
User is prompted to enter the name of a country.
If entered name is not found in database, user is prompted to try again.

GRAPH DETAILS:
A line graph showing the increase (or decresase) of cumulative number of new virus infections 
per 100000 inhabitants are plotted for any user-entered country. 
A time period of four months is taken: mid April to mid August 2020 
The cumulative number for any given day is calculated to indicate the 14 days prior to 
the compilation date of the .csv file. 
The program also shows the data for four other countries on the same plot.
The .csv file compilation date: 17.8.2020

Further Improvements:
1. GUI interface
2. Web interface
3. Creation of APIs for using this program's visualizations.

SPECIFICATIONS:
1. This program uses python 3.7 and the following libraries: 
(i) matplotlib 3.3.0
(ii) pandas 1.1.0

2. Download the latest "COVID-19 cases worldwide" .csv file from 
https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data
and save it in some folder. 
Change code line 197 to provide the file path and name of your file. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import random


def read_input():
    print("At the prompt below, enter name of a country and press enter.")
    country = input("Enter country name: ")
    return country


def input_validataion(name_country, dict_all_countries):
    """
    Function takes name_country, a string.
    It queries the population api to check if name_country exists in database
    Function returns true if name_country exists, false otherwise
    """
    for country_list in dict_all_countries.values():
        if name_country in country_list:
            return True
    return False


def fetch_all_countries(df):
    """ 
    Function finds the list of countries from all the continents
    It takes a dataframe of the input data file
    Returns a dict with keys --> continents  
                      values --> list of countries in the respective continents  
    """
    continents = ("Africa", "Europe", "America", "Oceania", "Asia")
    dict_all_countries = dict()
    for i in continents:
        df_current = df[(df["continentExp"] == i) & (df["dateRep"] == "28/07/2020")]
        dict_countries_current_continent = df_current.to_dict()
        list_countries_current_continent = list(
            dict_countries_current_continent["countriesAndTerritories"].values()
        )
        dict_all_countries[i] = list_countries_current_continent
    return dict_all_countries


def creating_date_list(df, n):
    df1 = df[df["countriesAndTerritories"] == "Afghanistan"]
    dict1_one_country = df1.to_dict()
    date_list = list(dict1_one_country["dateRep"].values())
    newlistdate_list = date_list[:n]  # take the last "n" days
    newlistdate_list.reverse()  # reverse the list, now list ends with latest date
    return newlistdate_list


def fetch_home_continent_data(df, country_sel):
    """
    Function finds the countries and cases for the home continent
    It takes (i) a dataframe of the input data file (ii) a string, country_sel
    Returns two things: (i) a list of countries 
    (ii) a dict with keys --> countries 
                   values --> list of cases for each of the days recorded since Dec 2019
    """
    # determining the continent in which the selected country is situated:
    dfc = df[
        (df["countriesAndTerritories"] == country_sel) & (df["dateRep"] == "28/07/2020")
    ]
    dict1 = dfc.to_dict()

    continent = list(dict1["continentExp"].values())
    continent = continent[0]

    # extracting the countries from the same continent as the selected country:
    df2 = df[(df["continentExp"] == continent) & (df["dateRep"] == "28/07/2020")]
    dict2_countries_of_a_continent = df2.to_dict()
    countries_list = list(
        dict2_countries_of_a_continent["countriesAndTerritories"].values()
    )

    z = len(countries_list)  # getting the number of countries

    dict_countries_cases = dict()
    for i in range(z):
        df_current = df[df["countriesAndTerritories"] == countries_list[i]]
        dict_current = df_current.to_dict()
        dict_countries_cases[countries_list[i]] = list(
            dict_current[
                "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
            ].values()
        )

    return countries_list, dict_countries_cases


def random_countries(df, list_countries, country_sel):
    """  
    Function selects 4 random countries, none of which are to be the user-selected country
    It takes (i) a dataframe of the input data file (ii) a list of countries
    (ii) a string, country_sel
    Returns a list of 4 random countries 
    """
    list_countries_random = random.sample(list_countries, 4)
    if country_sel in list_countries_random:
        while True:
            list_countries_random = random.sample(list_countries, 4)
            if country_sel not in list_countries_random:
                break  # this way we always have 5 unique countries: 4 + 1
    return list_countries_random


def fetch_five_countries_data(
    dict_countries_cases, country_sel, list_countries_random, n
):
    """
    Function creates a dict of countries and cases for 5 countries
    It takes (i) a dict of countries and cases (ii) a string, country_sel
    (iii) a list of 4 random countries 
    Returns a dict of countries and cases for 5 countries 
    """
    # creating a dict of countries and cases for the 5 countries
    dict_fivecountries = dict()
    dict_fivecountries[country_sel] = dict_countries_cases[country_sel]
    for country in list_countries_random:
        dict_fivecountries[country] = dict_countries_cases[country]

    # within the dict, "process" the list of case numbers
    for i in dict_fivecountries.keys():
        abc_real_list = dict_fivecountries[i]
        newabc_real_list = abc_real_list[:n]  # take the last "n" days
        newabc_real_list.reverse()  # reverse the list, now list ends with latest cases
        dict_fivecountries[i] = newabc_real_list

    return dict_fivecountries


# plotting countries and cases:
def plotter(newlistdate_list, dict4_random_refined):
    fig = plt.figure()
    x = newlistdate_list
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    for i in dict4_random_refined.keys():
        ax.plot(x, dict4_random_refined[i], label=i)

    ax.set_xticks(
        ["15/04/2020", "15/05/2020", "15/06/2020", "15/07/2020", "15/08/2020"]
    )
    z = ["mid-April", "mid-May", "mid-June", "mid-July", "mid-August"]
    ax.set_xticklabels(z)
    plt.ylabel("Cumulative number of new virus infections per 100000 inhabitants")
    plt.xlabel("Year 2020")
    plt.title("Covid-19 infections - Country Graphs")
    plt.legend(loc="best")
    plt.show()


def main():

    n = 130  # number of days (before data compilation date) for which graphs are found

    # NOTE: change file path as per your own file path.
    df = pd.read_csv(
        "/Users/bajya/Documents/07python_programs/08covid/EUOpenData_2020_08_17"
    )

    while True:
        country_sel = read_input()
        dict_all_countries = fetch_all_countries(df)
        if input_validataion(country_sel, dict_all_countries):
            break
        else:
            print("Country name not in database, please try again.")
            print("-----------------------------")

    list_countries, dict_countries_cases = fetch_home_continent_data(df, country_sel)

    list_countries_random = random_countries(df, list_countries, country_sel)

    dict_fivecountries = fetch_five_countries_data(
        dict_countries_cases, country_sel, list_countries_random, n
    )

    newlistdate_list = creating_date_list(df, n)

    plotter(newlistdate_list, dict_fivecountries)


main()
