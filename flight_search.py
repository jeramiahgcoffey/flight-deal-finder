import os

import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_KEY = os.environ["TEQUILA_KEY"]


class FlightSearch:
    # Method for updating IATA Code
    def get_city_code(self, city):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey": TEQUILA_KEY,
        }
        params = {
            "term": city,
            "location_types": "city",
        }
        with requests.get(
            url=location_endpoint,
            params=params,
            headers=headers
        ) as response:
            print(response.status_code)
            print(response.text)
            data = response.json()
            return data["locations"][0]["code"]

    # Method for getting flights available
    def flight_search(self, departure_location, destination_location, minimum_flight_date, maximum_flight_date):
        flight_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": TEQUILA_KEY
        }
        params = {
            "fly_from": departure_location,
            "fly_to": destination_location,
            "date_from": minimum_flight_date,
            "date_to": maximum_flight_date,
            "nights_in_dst_from": 5,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "adults": 1,
            "children": 0,
            "curr": "USD",
            "one_for_city": 1,
            # Controls stopovers or direct flights only
            # "max_stopovers": 0
        }

        with requests.get(
            url=flight_endpoint,
            params=params,
            headers=headers
        ) as response:
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"No flights found for {destination_location}.")
                return None
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["local_departure"].split("T")[0],
                return_date=data["local_departure"].split("T")[0],
                link=data["deep_link"]
            )
            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
