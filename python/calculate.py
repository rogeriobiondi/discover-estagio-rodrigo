#Exercise Page 57 - Python Succinctly.pdf [30/05/2017]

cost_day = 24*1.02
cost_mon = 30*cost_day
budget = 1836


print("Cost per day: {}".format(str(cost_day)))
print("Cost per month: {}".format(str(cost_mon)))

print("Cost of [20] Servers/Day: {}".format(str(cost_day*20)))
print("Cost of [20] Servers/Mon: {}".format(str(cost_mon*20)))

print("The Single Server Instance can operate with your budget(${0:.2f}) for {1:.0f} days!".format(budget, budget/cost_day ))