import pandas as pd
from datetime import datetime

# Read CSV files
hotelList = pd.read_csv("hotels.csv")
cards = pd.read_csv("cards.csv")
card = pd.read_csv("cards.csv").to_dict(orient="records")
card_security = pd.read_csv("card_security.csv")


# Hotel class definition
class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = hotelList.loc[hotelList["id"] == self.hotel_id, "name"].squeeze()
        self.price = hotelList.loc[hotelList["id"] == self.hotel_id, "price"].squeeze()

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
        return availability == "yes"


# ReservationTicket class definition
class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        now = datetime.now().strftime("%d-%m-%y     %H.%M.%S")
        phn_number = int(input("Enter your Phone Number: "))
        current_price = self.hotel.price + (self.hotel.price*18)/100
        content = f"""\n
                      INVOICE
                HOTEL BOOKING APP
                (mb78 Ak23 2155587)  
        \n             {now}              \n
        Thank you for your reservation!!
        
        Name: {self.customer_name}                Mobile Number: {phn_number}
        
        Here are your booking details:
        
        Hotel Name: {self.hotel.name} | Price:  ₹{self.hotel.price}/- | GST charge: 18 % | Price(Inclusive TAX.):  ₹{current_price}/-
        
        """
        return content


# SpaReservationTicket class definition
class SpaReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate_ticket(self):
        print()
        now = datetime.now().strftime("%d-%m-%y  %H.%M.%S")
        content = f"""
        Thank you for your spa reservation!!
        Here are your booking details:
        {now}
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """
        return content


# CreditCard class definition
class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}
        for card_info in card:
            if (card_info["number"] == self.number and
                    card_info["expiration"] == expiration and
                    card_info["holder"] == holder and
                    card_info["cvc"] == cvc):
                return True
        return False

    def pay(self, amount):
        for card_info in card:
            if card_info["number"] == self.number:
                if card_info["amount"] >= amount:
                    card_info["amount"] -= (amount + ((amount * 18) / 100))
                    cards_df = pd.DataFrame(card)
                    cards_df.to_csv("cards.csv", index=False)
                    return True
                else:
                    print("!! Transaction Unsuccessful !!")
        return False


# SecureCreditCard class definition
class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = card_security.loc[card_security["number"] == self.number, "password"].squeeze()
        return password == given_password


# Main code
print("           Namaste!! Welcome to our Hotel Booking App           \n")
print(hotelList)
hotel_ID = int(input("\nEnter the id of the Hotel: "))
hotel = Hotel(hotel_ID)

if hotel.available():
    further = input("\nDo you want to pay the rent(y/n): ").lower()
    if further == "y":
        card_number = int(input("\nEnter your Credit card number: "))
        expire_date = input("Enter card expiry date (MM/YY): ")
        holder_name = input("Enter the card holder name: ")
        cvv_number = int(input("Enter the CVV number: "))
        credit_card = SecureCreditCard(number=card_number)
        if credit_card.validate(expiration=expire_date, holder=holder_name, cvc=cvv_number):
            given_password = input("Enter your card password: ")
            if credit_card.authenticate(given_password=given_password):
                if credit_card.pay(hotel.price):
                    hotel.book()
                    name = input("Enter your Name: ")
                    reservation = ReservationTicket(customer_name=name, hotel_object=hotel)
                    print(reservation.generate())
                    print(f"Thanks for choosing our hotel {hotel.name}")
                    spa = input("Do you want to book a spa package? ").lower()
                    if spa == "yes":
                        spa_reservation = SpaReservationTicket(customer_name=name, hotel_object=hotel)
                        print(spa_reservation.generate_ticket())
                else:
                    print("Insufficient funds on the credit card.")
            else:
                print("Credit card authentication failed.")
        else:
            print("Problem with your payment card")
    else:
        print("Payment process was not completed. Please try again.")
else:
    print("Hotel is not available.")

print("\n\n_____________________________________________________")

print("\nDanyawad!! Visit again....")
