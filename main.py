import pandas
from datetime import datetime

hotelList = pandas.read_csv("hotels.csv")
card = pandas.read_csv("cards.csv").to_dict(orient="records")
card_security = pandas.read_csv("card_security.csv")

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = hotelList.loc[hotelList["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        try:
            capacity_index = hotelList.loc[hotelList["id"] == self.hotel_id].index
            capacity = hotelList.loc[capacity_index, "capacity"].squeeze()
            if capacity == 0:
                hotelList.loc[hotelList["id"] == self.hotel_id, "available"] = "no"
            else:
                new_capacity = capacity - 1
                hotelList.at[capacity_index[0], "capacity"] = new_capacity
                if new_capacity == 0:
                    hotelList.loc[hotelList["id"] == self.hotel_id, "available"] = "no"
            hotelList.to_csv("hotels.csv", index=False)
        except FutureWarning:
            pass

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

class SpaReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_names = customer_name
        self.hotels = hotel_object

    def generateTicket(self):
        now = datetime.now().strftime("%d-%m-%y  %H.%M.%S")
        content = f"""
                Thank you for your resevation!!
                Here are your booking data:
                {now}
                Name: {self.customer_names}
                HotelName: {self.hotels.name}
                """
        return content


class CredictCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in card:
            return True
        else:
            return False

    def pay(self):
        pass


class SecureCreditCard(CredictCard):
    def authenticate(self, given_password):
        password = card_security.loc[card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print("Namaste!! Welcome to ours Hotel booking App....")
print(hotelList)
hotel_ID = int(input("Enter the id of Hotel:  "))
hotel = Hotel(hotel_ID)

if hotel.available():
    further = input("Do you pay the rent: ").lower()
    if further == "yes":
        card_number = int(input("Enter your Credit card number: "))
        expire_date = input("Enter card expire date: ")
        holder_name = input("Enter the card holder name: ")
        cvv_number = int(input("Enter the cvv number: "))
        credit_card = SecureCreditCard(number=card_number)
        if credit_card.validate(expiration=expire_date, holder=holder_name, cvc=cvv_number):
            if credit_card.authenticate(given_password="mypass"):
                hotel.book()
                name = input("Enter your Name: ")
                reservation = ReservationTicket(customer_name=name, hotel_object=hotel)
                print(reservation.generate())
                print(f"Thanks for choosing our hotel {hotel.name}")
                spa = input("Do you want to book a spa package? ").lower()
                if spa == "yes":
                    spa_reservation = SpaReservationTicket(customer_name=name, hotel_object=hotel)
                    print(spa_reservation.generateTicket())
            else:
                print("Credit card authentication failed.")
        else:
            print("Problem with your payment card")
    else:
        print("Something problem in the payment server.., Go back and pay again")

else:
    print("Hotel is not free..")

print("\n\n_____________________________________________________")

print("\nDanyawad!! Visit again....")
