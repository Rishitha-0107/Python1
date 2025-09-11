class BankAccount:
    def __init__(self):
        self.__balance=0 
    def deposit(self,amount):
        self.__balance+=amount
        print(f"Deposited {amount}")
    def withdraw(self,amount):
        if amount<=self.__balance:
            self.__balance-=amount
            print(f"Withdrew {amount}")
        else:
            print("Insufficient balance!")
    def get_balance(self):
        return self.__balance
a=BankAccount()
a.deposit(5000)
a.withdraw(2000)
print("Final Balance:",a.get_balance())
