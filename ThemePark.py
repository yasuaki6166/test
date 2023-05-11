#
# A tentative multi-agent simulation for Congestion problem of a themepark
# coded by Yasuaki Hirano
#

import numpy as np
import random as r
import matplotlib.pyplot as plt

class Global():
    Spot       =     25    # no. spots
    Customer   =  20000    # no. customers
    Period     =    720    # operating minutes in a day

class Spot():
    def __init__(self,id,capacity,serviceTime):
        self.id = id
        self.capacity = capacity
        self.serviceTime = serviceTime
        self.queue = []
        self.status = 0
        self.users = []
        self.noTime = 0
        self.waitTime = 0

class Customer():
    def __init__(self,id,arrival,desirable):
        self.id = id
        self.arrival = arrival
        self.vacancy = 1
        self.desirable = desirable
        self.nvtime = 0
        self.satisfaction = 0
        self.fatigue = 0

###############################################################

if __name__ == "__main__":


    d = 1
    vr = 0
    x = [0]
    y = [120000000]
    passedTime = []
    max_patience = []
    while True:
        x.append(x[-1] + d)
        if x[-1] == 7200:
            break
    for cnt in x[1:]:
        if vr > 12500:#416.7分の時
            vr =vr+5.7
            y.append(y[-1] - vr)
        else:
            vr = vr+3
            y.append(y[-1] - vr)
    for i in x:
        passedTime.append(i/10)
    for i in y:
        max_patience.append(i/1000000)

    spots = []
    for i in range(Global.Spot):
        capacity = 30
        serviceTime = 10
        spot = Spot(i,capacity,serviceTime)
        spots.append(spot)

    customers = []
    for i in range(Global.Customer):
        arrival = r.choice(range(int(Global.Period/2)))  
        desirable = r.sample(spots,8)
        customer = Customer(i,arrival,desirable)
        customers.append(customer)

    Period = []
    spot_number = [1,9,12,20]
    noTimelists = {}
    waitTimelists = {}
    for i in spot_number:
        noTimelists[i] = []
    for i in spot_number:
        waitTimelists[i] = []
    
    for nowtime in range(Global.Period):
        for customer in customers:
            #if nowtime == 600:
                #print(max_patience[10*(nowtime-customer.arrival)])
            if customer.arrival > nowtime:
                continue
            if customer.vacancy == 0:
                continue
            if len(customer.desirable) == 0:
                continue
            cnt = 0
            for option in customer.desirable:
                cnt += 1
                if option.waitTime > max_patience[10*(nowtime-customer.arrival)]:
                    continue
                else:
                    go = customer.desirable[cnt-1]
                    customer.desirable.pop(cnt-1)
                    go.queue.append(customer)
                    customer.vacancy = 0
                    break
        for spot in spots:
            if spot.status == 1:
                if spot.noTime > nowtime:
                    continue
                for user in spot.users:
                    user.satisfaction += 1
                    user.vacancy = 1
                spot.users = []
                spot.status = 0
            while(len(spot.users) < spot.capacity):
                if len(spot.queue) > 0:
                    customer = spot.queue[0]
                    spot.queue.pop(0)
                    spot.users.append(customer)
                else:
                    break        
            spot.status = 1
            spot.noTime = nowtime + spot.serviceTime
            spot.waitTime = (len(spot.queue) / spot.capacity)* spot.serviceTime

        Period.append(nowtime)
        for i in spot_number:
            noTimelists[i].append(len(spots[i].queue))
        for i in spot_number:
            waitTimelists[i].append(spots[i].waitTime)
    
      
    plt.plot(Period,waitTimelists[1])
    plt.xlabel('time passed after theme park opening hours[minutes]')
    plt.ylabel('waiting time for spot 1[minutes] ')
    plt.savefig('waitingtime')
    plt.show()
    plt.plot(Period,noTimelists[1])
    plt.xlabel('time passed after theme park opening hours[minutes]')
    plt.ylabel('number of customers waiting for spot 1')
    plt.savefig('numberofqueue')
    plt.show()
                
                
                
            
