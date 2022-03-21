import datetime
from datetime import timedelta, timezone
import string
import random
from pprint import pprint
import requests
import wget
from io import BytesIO

from flask import Flask, request, jsonify

app = Flask(__name__)

city_airport_map = {
    'Torino': 'Caselle',
    'Milano': 'Malpensa',
    'Roma': 'Fiumicino',
    'Napoli': 'Internazionale',
    'Cosenza': 'Sant Anna',
    'Bologna': 'Marconi',
    'Bari': 'Karol Wojtyla',
    'Firenze': 'Vespucci',
    'Brindisi': 'Salento',
    'Cagliari': 'Elmas',
    'Venezia': 'Marco Polo',
    'Bergamo': 'Orio al Serio'
}

city = ['Torino',
        'Milano',
        'Roma',
        'Napoli',
        'Cosenza',
        'Bologna',
        'Bari',
        'Firenze',
        'Brindisi',
        'Cagliari',
        'Venezia',
        'Bergamo']


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def add_durata(departure_date, hours):
    # date=datetime.datetime.now()

    # hours=1
    hours_added = datetime.timedelta(hours=hours)
    arrival_date = departure_date + hours_added
    return arrival_date


@app.route('/generate')
def generate_flights():
    result = []

    durata = [1, 2, 3, 4]
    prezzo = [100, 40, 50, 70, 65, 75, 120, 130, 180, 200]

    # date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    andata = random.sample(range(0, 11), 6)

    part = []
    arr = []
    for i in andata:
        dep = city[i]
        part.append(dep)

    for i in city:
        if i not in part:
            arr.append(i)

    i = 0

    while i < 6:
        d1 = datetime.datetime.strptime('5/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.datetime.strptime('10/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')

        departure_date = random_date(d1, d2)

        m = random.randrange(0, 3)
        dur = durata[m]
        arrival_date = add_durata(departure_date, dur)

        # print(departure_date,arrival_date)
        departure_city = part[i]
        arrival_city = arr[i]
        departure_airport = city_airport_map[departure_city]
        arrival_airport = city_airport_map[arrival_city]
        f = random.randrange(0, 9)
        price = prezzo[f]
        dd = departure_date.replace(tzinfo=timezone.utc)
        departure_date = dd.isoformat()
        ad = arrival_date.replace(tzinfo=timezone.utc)
        arrival_date = ad.isoformat()
        type = 'SMALL'

        result.append({
            "departureDate": departure_date,
            "arrivalDate": arrival_date,
            "departureCity": departure_city,
            "arrivalCity": arrival_city,
            "departureAirport": departure_airport,
            "arrivalAirport": arrival_airport,
            "price": price,
            "type": type
        })
        i += 1

    return jsonify(result)



if __name__ == '__main__':
    app.run()
