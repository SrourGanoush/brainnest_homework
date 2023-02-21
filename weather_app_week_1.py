from io import BytesIO
from tkinter import *
import requests
from PIL import Image, ImageTk
import json
import datetime
# To use decorator for exception handling
from functools import wraps


# Put here the openweathermap API's token
API_KEY = ""

# For temperature in Celsius use units=metric
API_UNITS = "metric"

def catch_all_error_and_write_on_widget(f):
    """
    I used decorator to catch all errors and reduce the code size. I kept it simple by writing 
    the exception on the weather summary Text widget 
    """

    # Text widget as global variable to update it inside other functions
    global weather_summary_tk_text

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.HTTPError as err: 
            weather_summary_tk_text.insert('1.0',"Http Error\n") 

        except requests.exceptions.ConnectionError as err:
            weather_summary_tk_text.insert('1.0',"Error Connecting\n")
        except requests.exceptions.Timeout as err:
            weather_summary_tk_text.insert('1.0',"Timeout Error\n")
        except requests.exceptions.RequestException as err:
            weather_summary_tk_text.insert('1.0',"Request error\n")
        # Catch all the remaining errors
        except Exception as err:
            weather_summary_tk_text.insert('1.0',f"{err}\n")
            
    return decorated

@catch_all_error_and_write_on_widget
def get_weather_json_dict_from_api(city_name):

    # Requesting weather information  of the specified city from openweathermap "Current weather data" API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={API_UNITS}"
    api_response = requests.get(url)
    # Using loads method in json module to deserialize the response's json string to python dictionary
    json_dict = json.loads(api_response.text)

    return json_dict


@catch_all_error_and_write_on_widget
def get_weather_icon_by_id(icon_id):

    # Icon_id is from weather json data, to show the current weather status by icon
    url = f'https://openweathermap.org/img/wn/{icon_id}.png'
    icon = requests.get(url)
    # Using BytesIO to create file like object in the memory
    return Image.open(BytesIO(icon.content))

@catch_all_error_and_write_on_widget
def get_weather_info_from_json_dict(weather_json_dict):

    # Extract the required values from the dictionary and return string 
    if weather_json_dict['cod'] == 200: # Successful response for the queried city name
        temp = weather_json_dict['main']['temp']
        min_temp = weather_json_dict['main']['temp_min']
        max_temp = weather_json_dict['main']['temp_max']
        pressure = weather_json_dict['main']['pressure']
        humidity = weather_json_dict['main']['humidity']
        cloudy = weather_json_dict['clouds']['all']
        description = weather_json_dict['weather'][0]['description']

        return f"\nTemperature: {temp}°\nMin Temp: {min_temp}°\nMax Temp: {max_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nCloud: {cloudy}%\nInfo: {description}"
    else:
        # API's response: {"cod":"404","message":"city not found"}
        return "City not found"

@catch_all_error_and_write_on_widget
def get_weather_when_click_button():

    # Get a new weather data when clicking "Get Weather" button

    # To access and manipulate the global variables' values inside the function
    global city_name_value
    global weather_summary_tk_text
    global weather_icon_tk_label

    # Check the entered name is not empty
    if city_name_value.get():
        # Requesting the weather data for the entered city_name from openweathermap "Current weather data" api endpoint
        weather_json_dict = get_weather_json_dict_from_api(city_name_value.get())

        # Check if the returned value is not None
        if weather_json_dict is not None:
            # Extract the required values from the dictionary and return string
            weather_info = get_weather_info_from_json_dict(weather_json_dict)
            # Check if the city is found
            if weather_info == "City not found":
                # Raise exception to handled by decorator to write it in the Text widget
                raise Exception("City not found")
            else:
                # icon_id represent the status of the weather
                icon_id = weather_json_dict['weather'][0]['icon']

                # Getting the icon that shows the weather status 
                icon_data = get_weather_icon_by_id(icon_id)

                # Pillow library's' Tkinter-compatible PhotoImage widget
                weather_status_icon = ImageTk.PhotoImage(icon_data)

                # To show the weather icon in the screen
                weather_icon_tk_label.configure(image=weather_status_icon, bg='#fff')
                weather_icon_tk_label.image = weather_status_icon

                # To show the weather information in the label widget on the screen
                # Clear the text widget
                weather_summary_tk_text.delete('1.0', END)
                # Add the weather info in the text widget
                weather_summary_tk_text.insert(END, weather_info)
    else:
        # Raise exception for empty name
        raise Exception("City name is empty")
@catch_all_error_and_write_on_widget
def main():

    # Define global variables to be changed in other functions

    global city_name_value
    global weather_summary_tk_text
    global weather_icon_tk_label

    #Initialize Window
    screen = Tk()
    # Window's size
    screen.geometry("300x250")
    # Window's title
    screen.title('Weather App')

    # Using StringVar to help us manage the value of the city_name_textField widget
    city_name_value = StringVar()
    
    # Using grid to align widgets in the same row, and using pady and padx to add padding 
    city_label = Label(screen, text='Enter City').grid(
        columnspan=4, pady=10,)

    # textField and button in the same row
    city_name_textField = Entry(screen, textvariable=city_name_value).grid(
        row=1, column=0, columnspan=3)
    # Call "get_weather_when_click_button" function when we press the button. Sticky E to stick the widget in right side of cell 
    Button(screen, command=get_weather_when_click_button, text="Get Weather",
           bg='#fff').grid(row=1, column=1, columnspan=3, sticky=E)

    # Get the current time and date
    current_date_time = datetime.datetime.now()
    # Show the current date and time in a label widget. The string format  YEAR-MONTH-DAY HOURs:MINUTES:SECONDS
    current_datetime_label = Label(
        screen, text=f"Current date and time: {current_date_time.strftime('%Y-%m-%d %H:%M:%S')}").grid(columnspan=4, pady=10,)

    # Empty widgets to be changed when we press GET Weather button 
    weather_summary_tk_text = Text(screen,height=8, width=17, font=('Arial', 9))
    weather_summary_tk_text.grid(row=3, column=1, pady=10, padx=20, columnspan=3)
    weather_icon_tk_label = Label(screen)
    weather_icon_tk_label.grid(row=3, column=0, pady=10,
                            columnspan=3, padx=20, sticky=W)

    mainloop()


if __name__ == "__main__":
    main()
