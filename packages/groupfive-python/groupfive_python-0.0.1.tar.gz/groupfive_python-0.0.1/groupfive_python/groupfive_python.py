class FoodSupplies :
    def __init__(self, name, food = 0.0):
        self.name = name
        self.food = food
    def deposit(self, food):
        self.food += food
    def withdraw(self, food):
        self.food -= food
    def check_food(self):
        print("All Food is {} piece".format(self.food))
