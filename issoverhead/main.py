import requests
from datetime import datetime
import smtplib
import time

my_email = "kunj1766@gmail.com"
password = "1234"

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT <= iss_latitude <= 56 and MY_LONG <= iss_longitude <= 0:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


while True:
    time.sleep(60)
    if is_iss_overhead and is_night:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky.")
