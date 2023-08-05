import random
from PointSystem.KeepRefs import KeepRefs

class item(KeepRefs):

    def __init__(self, demand: int, price: float, supply: int, name: str, *, popular: bool = None):
        super(item, self).__init__()
        self.demand = demand
        self.price = price
        self.supply = supply
        self.multiplier = self.price / self.demand
        self.isPopular = popular
        self.name = name

    def progress(self, time: int, *, popular: bool = 0):
        x = None
        while time > 0:
            if popular == 0:
                if self.isPopular == True:
                    x = random.randint(self.demand + 10, self.demand + 30)
                elif self.isPopular == None:
                    x = random.randint(self.demand - 5, self.demand + 5)
                elif self.isPopular == False:
                    x = random.randint(self.demand - 30, self.demand - 10)
                else:
                    pass
            elif popular == True:
                self.isPopular = popular
                x = random.randint(self.demand + 10, self.demand + 30)
            elif popular == None:
                self.isPopular = popular
                x = random.randint(self.demand - 5, self.demand + 5)
            elif popular == False:
                self.isPopular = popular
                x = random.randint(self.demand - 30, self.demand - 10)
            else:
                raise TypeError("The popular argument is optional, but its value should either be True, None, or False. See this page for more info: https://github.com/Totallyahuman15/point-system/wiki/How-to-use:-Economy#the-progress-function")
            time -= 1
            if time <= 0:
                self.demand = x
                self.price = round(self.demand * self.multiplier, 2)
                self.supply -= self.demand
                if self.supply <= -1:
                    self. supply = 0
                asd = random.randint(1, 10)
                if asd == 5:
                    self.supply += int(self.demand / 2)

def econ_progress(time: int = 1):
    for i in item.get_instances():
        i.progress(time=time)
