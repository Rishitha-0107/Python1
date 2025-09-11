class Payment:
    def pay(self,amount):
        print("Payment method not specified") 
class CashPayment(Payment):
    def pay(self,amount):
        print(f"Paid ₹{amount} in cash")
class CardPayment(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} using credit/debit card")
class UPIPayment(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} using UPI")
payments=[CashPayment(),CardPayment(),UPIPayment()]
for p in payments:
    p.pay(1000)
