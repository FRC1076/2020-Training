num1 = input("What is the first number? ")
op = input("What is the operator? ")
num2 = input("What is the number? ")

try:
    num1 = float(num1)
except ValueError:
    print("First value is not a number!")
    quit()

try:
    num2 = float(num2)
except ValueError:
    print("Second value is not a number!")
    quit()

ans = ''

op = op.strip() # Removes all trailing spaces from the string
if op is "*":
    ans = num1 * num2
if op is "+":
    ans = num1 + num2
if op is "-":
    ans = num1 - num2
if op is "/":
    ans = num1 / num2

try:
    if(ans % 1 == 0):
        ans = int(ans)
except Exception:
    print("Operator is invalid!")
    quit()


print(ans)