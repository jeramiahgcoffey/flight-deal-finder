from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime as dt

ORIGIN_CITY_IATA = "AUS"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

# Update IATA Code in sheets
needs_destination_update = False
for row in sheet_data:
    if row["iataCode"] == "":
        needs_destination_update = True
        row["iataCode"] = flight_search.get_city_code(row["city"])
        print(row["city"])

if needs_destination_update:
    data_manager.destination_data = sheet_data
    data_manager.update_destination_data()
    needs_destination_update = False
pprint(sheet_data)

tomorrow = (dt.datetime.now() + dt.timedelta(days=1)).strftime("%d/%m/%Y")
six_months_from_now = (dt.datetime.now() + dt.timedelta(days=(6 * 30))).strftime("%d/%m/%Y")

for destination in sheet_data:
    flight = flight_search.flight_search(
        departure_location=ORIGIN_CITY_IATA,
        destination_location=destination["iataCode"],
        minimum_flight_date=tomorrow,
        maximum_flight_date=six_months_from_now
    )
    if flight:
        if flight.price < destination["lowestPrice"]:
            notification_manager = NotificationManager(flight)
