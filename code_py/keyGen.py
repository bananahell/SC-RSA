import random

def getGCD(number1, number2):
    while (number1 != 0 and number2 != 0):
        if (number1 > number2): 
           number1 %= number2
        else:
           number2 %= number1
    return max(number1,number2)

def genPrimeNumber(bits):
    while (1):
        number = random.getrandbits(bits)
        number = number | ((1 << bits - 1) | 1)
        # print(number);
        if (isPrime(number,5)):
           return number

def isPrime(number, accuracy):
    if (number < 2): 
       return False
    if (number % 2 == 0 and number != 2):
       return False
    
    k = 0
    m = number - 1
    while (m % 2 == 0):
       m //= 2
       k += 1

    i = 0
    for i in range(accuracy):
        a = random.randint(1,number-1)
        b = pow(a,m,number)
        if (b == 1 or b == (number - 1)):
            continue
        
        for j in range(k):
            b = pow(b,2,number)
            if (b == 1):
               return False
            if (b == (number - 1)):
               break
        if (b != (number - 1)):
           return False
    
    return True

def genKeys():
    p = genPrimeNumber(1024);
    while (1):
      q = genPrimeNumber(1024);
      if (q != p): break
    N = p*q
    fi_N = (p-1)*(q-1)

    for e in range(fi_N-1, -1, -1):
      if (e % p != 0 and e % q != 0):
         if (getGCD(e,fi_N) == 1):
            break

   #  print(getGCD(e,fi_N))
   #  print(getGCD(e,N))

    d = (fi_N * 5) - 1
   #  print((d*e)%fi_N)

    print('Gerando chaves ----------------------------------')
    print("Numeros primos escolhidos: ")
    print(f"p: {p}\n")
    print(f"q: {q}\n")
    print(f"p*q = N: {N}\n")
    print(f"fi_N: {fi_N}\n")

    return (e,N), (d,N)
      

    

