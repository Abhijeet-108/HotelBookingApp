import pandas
from datetime import datetime

hotelList = pandas.read_csv("hotels.csv")


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = hotelList.loc[hotelList["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        hotelList.loc[hotelList["id"] == self.hotel_id, "available"] = "no"
        hotelList.to_csv("hotels.csv", index=False)

    def available(self):
        availability = hotelList.loc[hotelList["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        now = datetime.now().strftime("%d-%m-%y  %H.%M.%S")
        content = f"""
        Thank you for your resevation!!
        Here are your booking data:
        {now}
        Name: {self.customer_name}
        HotelName: {self.hotel.name}
        """
        return content


print("Namaste!! Welcome to ours Hotel booking App....")
print(hotelList)
hotel_ID = int(input("Enter the id of Hotel:  "))
hotel = Hotel(hotel_ID)

if hotel.available():
    hotel.book()
    name = input("Enter your Name: ")
    reservation = ReservationTicket(customer_name=name, hotel_object=hotel)
    print(reservation.generate())
else:
    print("Hotel is not free..")

print("Danyawad!! Visit again....")
