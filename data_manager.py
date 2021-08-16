import requests


SHEETY_ENDPOINT = "https://api.sheety.co/71bc7b155fe051bcc963ca24178a55d0/flightDeals/prices"


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        with requests.get(url=SHEETY_ENDPOINT) as response:
            data = response.json()
            self.destination_data = data["prices"]
            return self.destination_data

    def update_destination_data(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            with requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            ) as response:
                print(response.text)
