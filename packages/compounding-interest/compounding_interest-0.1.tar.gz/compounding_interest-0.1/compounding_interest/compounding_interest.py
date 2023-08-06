class compounding:
    intial = int(input("Enter the intial amount : "))
    percentage1 = int(input("Enter the percentage per trade : "))
    percentage = percentage1/100
    trades = int(input("Enter the number of trades : "))
    profit = 0
    for i in range(trades):
        profit = intial * percentage
        intial += profit
    print(intial)

def compound():
    {
        object1 := compounding()
    }