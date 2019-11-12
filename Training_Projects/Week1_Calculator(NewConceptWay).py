num1 = input("What is the first number?")
op = input("What is the operator?")
num2 = input("What is the number?")

command = "print(" + num1+op+num2 + ")"
ans = exec(command)