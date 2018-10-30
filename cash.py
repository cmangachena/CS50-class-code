from cs50 import get_float

# To get change from user
change = get_float("Change required: ")
# To ensure correct usage
while change < 0:
    change = get_float("Change required: ")
# To convert change to a whole number
change_required = round(change*100)
# To get how many quarters are required
quarters = change_required//25
# To get how many dimes are required
dimes = (change_required - quarters*25)//10
# To get how many nickels are required
nickels = (change_required - (quarters*25 + dimes*10))//5
# To get how many pennies are required
pennies = (change_required - (quarters*25 + dimes*10 + nickels*5))
# To get total number of coins required
total = (quarters + dimes + nickels + pennies)
print("Coins required = ", total)