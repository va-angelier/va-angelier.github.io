def add(x, y): 
 """Add x to y"""
 return x + y

def subtract(x, y): 
  """Subtract x from y"""
  return x - y
def multiply(x, y): 
 """Multiply x by y"""
 return x * y 
def divide(x, y): 
 """Divide x by y """
 return x / y
print("Select operation.")
"""Prints Select operation."""
print("1.Add") 
"""Prints 1.Add"""
print("2.Subtract") 
"""Prints 2.Substract"""
print("3.Multiply") 
"""Prints 3.Multiply"""
print("4.Divide") 
"""Prints 4.Divide"""
while True:
 """Runs while true, read user input.""" 
 choice = input("Enter choice(1/2/3/4): ")  
 if choice in ('1', '2', '3', '4'): 
    num1 = float(input("Enter first number: ")) 
    num2 = float(input("Enter second number: ")) 
 if choice == '1': print(num1, "+", num2, "=", add(num1, num2)) 
 elif choice == '2': print(num1, "-", num2, "=", subtract(num1, num2)) 
 elif choice == '3': print(num1, "*", num2, "=", multiply(num1, num2)) 
 elif choice == '4': print(num1, "/", num2, "=", divide(num1, num2)) 
 next_calculation = input("Let's do next calculation? (yes/no): ")
 if next_calculation == 'no': 
  break
 else: print("Invalid Input")
