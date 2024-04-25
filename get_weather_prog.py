import requests
import datetime
import json
from geopy.geocoders import Nominatim
from requests.exceptions import RequestException  # Import the RequestException

while True:
    choice = input("Please type: \n1. for existing wether info.\n2. Other weather news:\n3. to Exit\n")
    if choice == "1" :
        try:
                with open ("weather.txt", "r") as weather_file:
                    data_loaded = json.load(weather_file)
                print(data_loaded)
        except FileNotFoundError:
                print("file not found, type 2 if you want to proceed, or 3 to 'Exit' ")
                
    elif choice =="2":
                
                def is_valid_date(date_string, format="%Y-%m-%d"):
                    try:
                        datetime.datetime.strptime(date_string, format)
                        return True
                    except ValueError:
                        return False
            # Define the function to get coordinates
                def get_coordinates(city):
                    geolocator = Nominatim(user_agent="get_weather_prog")
                    location = geolocator.geocode(city)
                    if location:
                        return location.latitude, location.longitude
                    else:
                        print("Location not found.")
                        return None

                city = input("Enter a city name: ")
                coordinates = get_coordinates(city)
                if coordinates:
                    latitude, longitude = coordinates
                    print(f"The latitude and longitude of {city} are: {latitude}, {longitude}")
                else:
                    
                    continue  # go back to the main menu again

                # Get the start and end dates
                print("\n\nchoose the start and end date, and if you leave it blank it will defaulted to next day date!\n\n")
                start_date = input("What is the date in this format please: yyyy-mm-dd: ")
                end_date = input("What is the end date in this format please: yyyy-mm-dd: ")

                
                if is_valid_date(start_date, end_date):
                    try:
                       # Construct the URL for the API request
                        if start_date and end_date:
                            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={start_date}&end_date={end_date}"
                        else:
                            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={tomorrow}&end_date={tomorrow}"

                        # Send the API request
                        response = requests.get(url)
                        response.raise_for_status()  # Raise an exception for HTTP errors .
                        response_dict = response.json()
                        precipitation_data = response_dict.get("daily", {}).get("precipitation_sum", [])
                        time_data = response_dict.get("daily", {}).get("time", [])
                        
                        # Print the weather information
                        for sum, t in zip(precipitation_data, time_data):
                            if sum > 0:
                                print(f"On {t}, it will be raining in {city} and precipitation sum will be {sum} mm")
                            else:
                                print(f"There's no rain in {city} on {t}")
                        
                        # Write weather info to a file
                        with open("weather.txt", "w") as weather_file:
                            json.dump({"city": city, "precipitation": precipitation_data, "time": time_data}, weather_file)

                    except RequestException as e:  # Handle network-related errors
                        print("Failed to fetch weather data from the API:", e)
                    
                    except json.JSONDecodeError:
                        print("Failed to decode JSON response from the API.")
                else:
                    print(f"{start_date} is not a valid date.")
                    continue

    elif choice == "3":
         exit()

