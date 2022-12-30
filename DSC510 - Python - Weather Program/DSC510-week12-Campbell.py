# DSC 510
# Week 12
# Programming Assignment Week 12: Final Project
# Author: Julie Campbell
# 11/10/2022
# Display weather data by zip code or city

# Change#: 1
# Change(s) Made: Provided pretty format for weather data and print current date/time
# Date of Change: 11/13/2022

# Change#: 2
# Change(s) Made: Use specific exceptions for try blocks
# Date of Change: 11/14/2022

# Change#: 3
# Change(s) Made: Add error handling for city and cloudiness
# Date of Change: 11/17/2022

import requests
import time


# Determine temperature method
def temperatureType(temperature):
    tempType = ""
    tempSymbol = ""
    tempValid = False
    if temperature.upper() == "FAHRENHEIT" or temperature.upper() == 'F':
        tempType = "imperial"
        tempSymbol = "F"
        tempValid = True
    elif temperature.upper() == "CELSIUS" or temperature.upper() == 'C':
        tempType = "metric"
        tempSymbol = "C"
        tempValid = True
    elif temperature.upper() == "KELVIN" or temperature.upper() == 'K':
        tempSymbol = "K"
        tempValid = True

    return tempType, tempSymbol, tempValid


# Collect weather data
def currentWeather(lat, lon, tempType, tempSymbol):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?"
        querystring = {"appid": "415c1442518d899547d32991fc3dea9f",
                       "lat": lat,
                       "lon": lon,
                       "units": tempType}
        response = requests.request("GET", url, params=querystring)
        response.raise_for_status()
    except requests.ConnectionError:
        print("Program did not connect successfully to the OpenWeatherMap API.")
    except requests.HTTPError:
        print("No weather data was found for the location.")
    except Exception as e:
        print(e)
    else:
        weatherJSON = response.json()
        prettyPrint(weatherJSON, tempSymbol)


# Get latitude and longitude of zip
def zipWeather(zipCode, tempType, tempSymbol):
    try:
        url = "http://api.openweathermap.org/geo/1.0/zip?"
        querystring = {"appid": "415c1442518d899547d32991fc3dea9f",
                       "zip": zipCode + ",US"}
        response = requests.request("GET", url, params=querystring)
        response.raise_for_status()
    except requests.ConnectionError:
        print("Program did not connect successfully to the OpenWeatherMap API.\n")
    except requests.HTTPError:
        print("No weather data found for that zip code.\n")
    except Exception as e:
        print(e)
    else:
        geoJSON = response.json()
        lat = geoJSON['lat']
        lon = geoJSON['lon']
        currentWeather(lat, lon, tempType, tempSymbol)


# Get latitude and longitude of city
def cityWeather(city, state, tempType, tempSymbol):
    try:
        url = "http://api.openweathermap.org/geo/1.0/direct?"
        querystring = {"appid": "415c1442518d899547d32991fc3dea9f",
                       "q": city + "," + state + ",US"}
        response = requests.request("GET", url, params=querystring)
        response.raise_for_status()
    except requests.ConnectionError:
        print("Program did not connect successfully to the OpenWeatherMap API.")
    except requests.HTTPError:
        print("No weather data found for that city and state.\n")
    except Exception as e:
        print(e)
    else:
        geoJSON = response.json()
        if geoJSON:
            lat = geoJSON[0]['lat']
            lon = geoJSON[0]['lon']
            currentWeather(lat, lon, tempType, tempSymbol)
        else:
            print("No weather data found for that city and state.\n")


# Print weather data in readable format
def prettyPrint(weatherJSON, tempSymbol):
    # Parse weather JSON
    weather = weatherJSON['weather']
    wMain = weatherJSON['main']
    wind = weatherJSON['wind']
    visibility = weatherJSON['visibility'] / 1000
    clouds = weatherJSON['clouds']
    # Print weather data
    print("\n")
    print("Current weather conditions for", weatherJSON['name'])
    print(str(round(wMain['temp'])) + "°" + tempSymbol)
    print('Feels like {}°{}. {}.'.format(round(wMain['feels_like']), tempSymbol, str.capitalize(
        weather[0]['description'])))
    print('-' * 30)
    print('{:12}{:<1}°{}'.format('Low Temp:', round(wMain['temp_min']), tempSymbol))
    print('{:12}{:<1}°{}'.format('High Temp:', round(wMain['temp_max']), tempSymbol))
    print('{:12}{:<1}mph'.format('Wind:', round(wind['speed'])))
    print('{:12}{:<1}%'.format('Humidity:', wMain['humidity']))
    print('{:12}{:<1}hPa'.format('Pressure:', wMain['pressure']))
    print('{:12}{:<1}km'.format('Visibility:', visibility))
    print('{:12}{:<1}%'.format('Cloudiness:', clouds['all']))
    print('-' * 30)
    print('As of', time.ctime(time.time()))
    print("\n")


def main():
    print("Welcome! Let's look at the weather forecast. Enter 'Q' at any time to exit.")
    location = input("Do you want to search by zip code or city? ")
    # While user wants to run
    while location.upper() != 'Q':
        # check if valid location type
        if location.upper() == 'ZIP CODE' or location.upper() == 'ZIP' or location.upper() == 'CITY':
            # user input temperature type
            temperature = input("What temperature type do you want (Fahrenheit, Celsius, Kelvin)? ")
            tempType, tempSymbol, tempValid = temperatureType(temperature)
            if tempValid:
                # if lookup by zip
                if location.upper() == 'ZIP CODE' or location.upper() == 'ZIP':
                    # Check if zip code is valid format
                    while True:
                        zipCode = input("Please enter a zip code: ")
                        if len(zipCode) == 5 and zipCode.isnumeric():
                            zipWeather(zipCode, tempType, tempSymbol)
                            break
                        else:
                            print('Not a valid zip. Please enter a 5 digit zip code.')
                            continue
                # if lookup by city
                elif location.upper() == 'CITY':
                    city = input("Please enter a city: ")
                    # Check if state is valid format
                    while True:
                        if city != "" and city != " " and city.isalpha():
                            state = input("Please enter a state in abbreviation form (ex: AL) ")
                            if len(state) == 2 and state.isalpha():
                                cityWeather(city, state, tempType, tempSymbol)
                                break
                            else:
                                print('Not a valid state. Please enter an abbreviated state.')
                                continue
                        else:
                            print("City entered was invalid. Please enter a valid city.")
                            city = input("Please enter a city: ")
            else:
                print('Please enter in a valid temperature type.')
                continue
        else:
            print('That is not a valid location type. Please try again.')
        location = input("Do you want to search another location by zip code or city? ")
    print('Weather program has exited.')


# run program
if __name__ == "__main__":
    main()
