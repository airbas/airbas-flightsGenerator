import datetime
from datetime import timedelta, timezone
import random
from flask import Flask, jsonify

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
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


@app.route('/generate')
def generate_flights():
    flights, n = [], 100
    hours, price = [1, 2, 3, 4], [100, 40, 50, 70, 65, 75, 120, 130, 180, 200]
    routes = [(part, dest) for part in city for dest in city if part != dest]

    for i in range(n):
        route = routes[random.randint(0, len(routes)-1)]

        date_start = datetime.datetime.strptime('5/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
        data_end = datetime.datetime.strptime('10/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
        departure_date = random_date(date_start, data_end)
        flight_time = hours[random.randrange(0, len(hours))]
        arrival_date = departure_date + datetime.timedelta(hours=flight_time)

        flights.append({
            "departureDate": departure_date.replace(tzinfo=timezone.utc).isoformat(),
            "arrivalDate": arrival_date.replace(tzinfo=timezone.utc).isoformat(),
            "departureCity": route[0],
            "arrivalCity": route[1],
            "departureAirport": city_airport_map[route[0]],
            "arrivalAirport": city_airport_map[route[1]],
            "price": price[random.randrange(0, len(price))],
            "type": 'SMALL'
        })

    return jsonify(flights)


if __name__ == "__main__":
    app.run(debug=True)
