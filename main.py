import pandas

df = pandas.read_csv("hotels.csv")


class Hotel:
    def __init__(self):
        pass

    def book(self):
        pass

    def available(self):
        pass


class ReservationTicket:
    def __init__(self, coustomer_name, hotel_object):
        pass

    def generate(self):
        pass


print(df)
id = input("Enter the id of Hotel:  ")
hotel = Hotel(id)

if hotel.available():
    hotel.book()
    name = input("Enter your Name: ")
    reservation = ReservationTicket(name, hotel)
    print(reservation.generate())
else:
    print("Hotel is not free..")