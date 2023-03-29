import simpy 
from random import random, seed


defaultNoOfCustomers = 5
defaultOpeningDuration = 78
totalServedCustomers = 0
arrivalTime = []
startOfServiceTime = []
waitingTime = []
departureTime = []

def customer(env, name, restaurant, **duration):
    global totalServedCustomers
    while True:
        yield env.timeout(round(random()*10)) # There is a new customer between 0 and 10 minutes
        print(f"{name} enters the restaurant and wait for the waiter to come at {round(env.now, 2)}")
        arrivalTime.append(round(env.now, 2))
        with restaurant.request() as req:
            yield req
            print(f"Sits are available. {name} get sitted at {round(env.now, 2)}")
            startOfServiceTime.append(round(env.now, 2))
            if round(env.now) >= (int(openingDuration) - 1):
                print("NO MORE CUSTOMERS")
                print("Total Served Customers {}".format(totalServedCustomers))
                print("Total Not Served Customers {}".format(int(noOfCustomers) - totalServedCustomers))
            yield env.timeout(duration['get_sitted'])
            print(f"{name} starts looking at the menu at {round(env.now, 2)}")
            yield env.timeout(duration['choose_food'])

            print(f'Waiters start getting the order from {name} at {round(env.now, 2)}')
            yield env.timeout(duration['give_order'])

            print(f'{name} starts waiting for food at {round(env.now, 2)}')
            yield env.timeout(duration['wait_for_food'])

            print(f'{name} starts eating at {round(env.now, 2)}')
            yield env.timeout(duration['eat'])

            print(f'{name} starts paying at {round(env.now, 2)}')
            yield env.timeout(duration['pay'])

            print(f'{name} leaves at {round(env.now, 2)}')
            departureTime.append(round(env.now, 2))
            totalServedCustomers=totalServedCustomers+ 1


seed(1)
env = simpy.Environment()
restaurant = simpy.Resource(env, capacity=4)
durations = {'get_sitted': 1, 'choose_food': 10, 'give_order': 5, 'wait_for_food': 20, 'eat': 30, 'pay': 10}
print("Service Durations: Get Sitted {} mins, Choose Food {} mins, Give Order {} mins, Wait for Food {} mins, Eat {} mins, Pay {} mins.".format(durations['get_sitted'], durations['choose_food'], durations['give_order'], durations['wait_for_food'], durations['eat'], durations['pay']))
print("Total Time for Each Customer without waiting {} mins".format((durations['get_sitted']+ durations['choose_food']+durations['give_order']+durations['wait_for_food']+durations['eat']+durations['pay'])))

noOfCustomers = input("Please enter the number of customers: ") or defaultNoOfCustomers
openingDuration = input("Please enter the resturant opening duration in mins: ") or defaultOpeningDuration


for i in range(int(noOfCustomers)):
    env.process(customer(env, f'Customer {i+1}', restaurant, **durations))

env.run(until=int(openingDuration))
waitingTime = [a_i - b_i for a_i, b_i in zip(startOfServiceTime, arrivalTime)]
serviceTime = [a_i - b_i for a_i, b_i in zip(departureTime, arrivalTime)]

print("Waiting Time for Each Customer",waitingTime)
print("Average Waiting Time for Each Customer", (sum(waitingTime)/len(waitingTime)))
print("Service Time for Each Customer",serviceTime)
print("Average Service Time for Each Customer", (sum(serviceTime)/len(serviceTime)))