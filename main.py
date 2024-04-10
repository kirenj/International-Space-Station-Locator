import requests
from datetime import datetime
import smtplib
import time

EMAIL = "*****@*****.com"
PASS = "***************"

MY_LAT = -25
MY_LONG = -134


def is_iss_overhead():
    request = requests.get(url= "http://api.open-notify.org/iss-now.json")

    # if request.status_code == 404:
    #     raise Exception("That resource does not exist!")

    request.raise_for_status()

    data = request.json()

    # The below values need to be changed to float type
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    print(iss_latitude)
    print(iss_longitude)
    # # Turning the above into a tuple
    # sat_position = (iss_longitude, iss_latitude)

    if (MY_LAT + 5 >= iss_latitude >= MY_LAT - 5) and (MY_LONG + 5 >= iss_longitude >= MY_LONG - 5):
        return True
    else:
        return False


def is_it_night_time():
    # The parameters for the API should be in a python dictionary format.
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    response_data = response.json()
    # print(data)
    sunrise = int(response_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(response_data["results"]["sunset"].split("T")[1].split(":")[0])
    # print(sunrise)

    # Shortened the below splits into a single line as shown above
    # split_sunrise = sunrise.split("T")
    # print(split_sunrise)
    # split_sunrise_hours = split_sunrise[1].split(":")
    # print(split_sunrise_hours)

    time_now = datetime.now().hour
    # the .hour makes 'time_now' into an integer hence the below logic becomes valid
    # print(time_now)

    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False


# is_iss_overhead()
# is_it_night_time()


while True:
    time.sleep(20)
    if is_iss_overhead() is True and is_it_night_time() is True:
        with smtplib.SMTP("smtp.*****.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASS)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs="*****@*****.com",
                msg="Subject: Look up !!\n\nThe International Space station is passing by."
            )