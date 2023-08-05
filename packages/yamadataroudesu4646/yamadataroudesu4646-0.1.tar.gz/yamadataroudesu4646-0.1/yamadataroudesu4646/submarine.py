class Submarine:
    '''
        ---------------------------
        Test Documentation

        นี่คือโปรแกรมสำหรับเรือดำน้ำ
        ---------------------------
    '''
    def __init__(self,price,budget):
        self.captain = 'Prawit'
        self.sub_name = 'PVV001'
        self.price = price # million
        self.kilo = 0
        self.budget = budget
        self.totalcost = 0

    def Missile(self):
        print('We are Department of Missile')

    def CalCommission(self):
        pc = 10 #10%
        percent = self.price * (pc/100)
        print('Boom! You got commission : {} Million Baht'.format(percent))
        
    def Goto(self,enemypoint,distance):
        print('Let\'s go to {},Distance : {} Km'.format(enemypoint,distance))
        #.format or can fill in {} but this version can't
        self.kilo = self.kilo + distance
        #self.kilo +=distance
        self.Fuel()

    def Fuel(self):
        diesel = 20 #20Baht/Litre
        cal_fuel_cost = self.kilo * diesel
        print('Current fuel cost : {:,d} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

    @property
    def BudgetRemaining(self):
        remaining = self.budget - self.totalcost
        print('Budget ramaining : {:,.2f} Baht'.format(remaining))
        return remaining

class ElectricSubmarine(Submarine):
    def __init__(self,price,budget):
        self.sub_name = 'PVV002'
        self.battery_distance = 100000 # Submarine can go 100000 km/100%
        super().__init__(price,budget) # copy function from...

    def Battery(self):
        allbattery = 100
        calculate = (self.kilo / self.battery_distance) * 100
        print('We have Battery Remaining: {}%'.format(allbattery-calculate))

    def Fuel(self):
        kilowatt = 5 #Baht
        cal_Fuel_cost = self.kilo * kilowatt
        print('Current power cost : {:,d} Baht'.format(cal_Fuel_cost))
        self.totalcost += cal_Fuel_cost

if __name__ == '__main__':
        
    tesla = ElectricSubmarine(40000,2000000)
    print(tesla.captain)
    print('We have budget: {:,d} Baht'.format(tesla.budget))
    tesla.Goto('Japan',10000)
    print(tesla.BudgetRemaining)
    tesla.Battery()

    print('------------------')

    armyground = Submarine(40000,2000000)
    print(armyground.captain)
    print('We have budget: {:,d} Baht'.format(armyground.budget))
    armyground.Goto('Japan',10000)
    print(armyground.BudgetRemaining)

#if manual     
#sub = ['Srivara','PVV02',5000]
#print(sub[0])
#print(sub[1])
#print(sub[2])
'''
armywater = Submarine(10000)
print('Water\nCaptain is :',armywater.captain)
print('Sub name is :',armywater.sub_name)
#print('Price is :',armywater.price,'Million')
#armywater.CalCommission()
print('Total distance :',armywater.kilo)
armywater.Goto('China',7000)
print('Total distance :',armywater.kilo)
armywater.Fuel()
current_budget = armywater.BudgetRemaining
print('Current budget : {:,d} Baht'.format(current_budget))
print('')
#-----------------------------------
armyground = Submarine(70000)
print('Ground\nCaptain is :',armyground.captain)
armyground.captain = 'Srivara'
print('But he died...\nthen New captain is :',armyground.captain)
print('Price is :',armyground.price,'Million')
armyground.CalCommission()
'''

