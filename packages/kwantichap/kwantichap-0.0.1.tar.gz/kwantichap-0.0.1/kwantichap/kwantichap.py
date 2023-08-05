class BankOnline:
    def __init__(self, name, money = 0.0):
        self.name = name
        self.money = money
    def deposit(self, money):
        self.money += money
    def withdraw(self. money):
        self.money -= money
    def check_money(self):
        print(f"current money is {self.money} baht.")
