from twilio.rest import Client
import os

TWILIO_ACCT = "AC4442dbd8d3d3cc5bfb535ac0fda3d4fa"
TWILIO_TOKEN = os.environ["TWILIO_TOKEN"]


class NotificationManager:
    def __init__(self, flight):
        self.price = flight.price
        self.departure_city = flight.origin_city
        self.departure_airport = flight.origin_airport
        self.arrival_city = flight.destination_city
        self.arrival_airport = flight.destination_airport
        self.outbound_date = flight.out_date
        self.inbound_date = flight.return_date
        self.booking_link = flight.link
        self.notify()

    def notify(self):

        notification = f"Flight Deal Alert: {self.departure_city}-{self.departure_airport} to {self.arrival_city}-" \
                       f"{self.arrival_airport} on {self.outbound_date} to {self.inbound_date} for ${self.price}.\n" \
                       f"Here's the booking link: {self.booking_link}"

        client = Client(TWILIO_ACCT, TWILIO_TOKEN)
        message = client.messages.create(
            body=notification,
            from_="+17029860727",
            to='+15129688615'
        )
        print(message.status)
