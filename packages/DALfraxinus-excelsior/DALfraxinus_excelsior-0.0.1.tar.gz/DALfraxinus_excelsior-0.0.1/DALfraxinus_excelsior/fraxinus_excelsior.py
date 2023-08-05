class BankOnline:
    # constructor
    def __init__(self, name, money = 0.0):
        self.name = name
        self.money = money
    # ฝาก
    def deposit(self, money):
        self.money += money
    # ถอน
    def withdraw(self, money):
        self.money -= money
    # ตรวจสอบเงินคงเหลือ
    def check_money(self):
        print("current money is {} baht".format(self.money))
