# Dependencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn
import requests
import json
import random
from citipy import citipy
from config import weather_api_key

# Function to generate cities list
def generate_cities_list(num):
    city_list = []
    for i in range(num):
        random_latitude = random.randrange(-90,90)
        random_longitude = random.randrange(-180,180)
        city = citipy.nearest_city(random_latitude, random_longitude).city_name
        city_list.append(city)
    return city_list

# Function to preform API calls
def getWeather(city_list):
    i = 1
    weather_data = []
    for city in city_list:
        # Save config information
        url = "http://api.openweathermap.org/data/2.5/weather?"
        city_link = city.replace(" ","%20")

        # Build query URL
        query_url = url + "appid=" + weather_api_key + "&units=" + 'Imperial'+ "&q=" + city_link

        # Print log of each city as it's being processed
        print(f"#{i}: {city} {query_url}")
        
        # Get weather data
        weather_response = requests.get(query_url)
        weather_json = weather_response.json()

        try:
            name = weather_json['name']
        
            # Get the latitude, temperature (F), humidity(%), cloudiness(%), and wind speed data from the json response
            latitude = weather_json['coord']['lat']
            longitude = weather_json['coord']['lon']
            prox = np.abs(float(latitude))
            #print(prox)
            temp = weather_json['main']['temp']
            humidity = weather_json['main']['humidity']
            clouds = weather_json['clouds']['all']
            wind_speed = weather_json['wind']['speed']
            weather_data.append({"City":name, 
                                 "Latitude":latitude, 
                                 "Longitude":longitude,
                                 "Proximity to Equator":prox,
                                 "Temperature (F)":temp, 
                                 "Humidity (%)":humidity, 
                                 "Cloudiness (%)":clouds, 
                                 "Wind Speed (mph)":wind_speed})
        except:
            pass
        
        i += 1
        
    return weather_data

# Functions to generate new plots
def plot_tempvslat(weather_df):
    # Temperature (F) vs. Latitude scatterplot
    weather_df.plot(kind='scatter', x="Latitude", y="Temperature (F)")

    # Plot attributes
    plt.suptitle("Temperature (F) vs. Latitude")
    plt.grid(alpha=0.25)
    plt.axvline(0, color="black", alpha=0.5, lw=1)

    # Save plot as png
    plt.savefig("temp_vs_lat.png")

def plot_humidityvslat(weather_df):
    # * Humidity (%) vs. Latitude scatterplot
    weather_df.plot(kind='scatter', x="Latitude", y="Humidity (%)")
    # weather_df.plot(kind='scatter', x="Proximity to Equator", y="Humidity (%)")

    # Plot attributes
    plt.suptitle("Humidity (%) vs. Latitude")
    plt.grid(alpha=0.25)
    plt.axvline(0, color="black", alpha=0.5, lw=1)

    # Save plot as png
    plt.savefig("humidity_vs_lat.png")

def plot_cloudvslat(weather_df):
    # * Cloudiness (%) vs. Latitude scatterplot
    weather_df.plot(kind='scatter', x="Latitude", y="Cloudiness (%)")
    # weather_df.plot(kind='scatter', x="Proximity to Equator", y="Cloudiness (%)")

    # Plot attributes
    plt.suptitle("Cloudiness (%) vs. Latitude")
    plt.grid(alpha=0.25)
    plt.axvline(0, color="black", alpha=0.5, lw=1)

    # Save plot as png
    plt.savefig("cloud_vs_lat.png")

def plot_windvslat(weather_df):
    # * Wind Speed (mph) vs. Latitude scatterplot
    weather_df.plot(kind='scatter', x="Latitude", y="Wind Speed (mph)")
    # weather_df.plot(kind='scatter', x="Proximity to Equator", y="Wind Speed (mph)")

    # Plot attributes
    plt.suptitle("Wind Speed (mph) vs. Latitude")
    plt.grid(alpha=0.25)
    plt.axvline(0, color="black", alpha=0.5, lw=1)

    # Save plot as png
    plt.savefig("wind_vs_lat")

# Main function
def main():
    cities = generate_cities_list(600)
    data = getWeather(cities)
    df = pd.DataFrame(data)
    
    # Export data to csv
    df.to_csv("cities.csv")

    # Generate plots
    plot_tempvslat(df)
    plot_humidityvslat(df)
    plot_cloudvslat(df)
    plot_windvslat(df)

