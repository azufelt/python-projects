"""
Using Recursion to solve problems
"""

#fib to the nth is    fn = fn-1 + fn-2




fibonacci = []
f1 = 0

def fibSum(n1, n2, f1):
  n3 = n1 + n2
  fibonacci.append(n3)
  # print(n)
  # print("{}:{}".format(f1,n3))  
  n1 = n2
  n2 = n3
  f1 += 1
  fibSum(n1, n2, f1)

def fib(n):
  
  n1 = 0
  n2 = 1
  f1 = 1
  fibonacci.append(n1)
  fibonacci.append(n2)
  if f1 >= 50:
    return
  fibSum(n1, n2, f1)
  print(n, f1)
  print(fibonacci)
  print("The value of that index is: {}".format(fibonacci[n]))

def main():
  n = int(input("Enter a Fibanoocci index: "))
  fib(n)

if __name__ == "__main__":
    main()






# fibonacci = []
# f1 = 0

# def fibSum(n1, n2, f1):
#   if f1 >= 50:
#     return
#   n3 = n1 + n2
#   fibonacci.append(n3)
#   # print(n)
#   # print("{}:{}".format(f1,n3))  
#   n1 = n2
#   n2 = n3
#   f1 += 1
#   fibSum(n1, n2, f1)

# def fib(n):
#   n1 = 0
#   n2 = 1
#   f1 = 1
#   fibonacci.append(n1)
#   fibonacci.append(n2)
#   fibSum(n1, n2, f1)
#   print(n, f1)
#   print(fibonacci)
#   print("The value of that index is: {}".format(fibonacci[n]))

# def main():
#   n = int(input("Enter a Fibanoocci index: "))
#   fib(n)

# if __name__ == "__main__":
#     main()


