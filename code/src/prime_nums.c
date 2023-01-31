#include "prime_nums.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

uint8_t isPrime(uint64_t number) {
  uint64_t i;
  uint64_t half;
  if (number < 2) {
    return 1;
  }
  half = number >> 1;
  if (half >= 2) {
    if (number % 2 == 0) {
      return 1;
    }
  }
  for (i = 3; i < half; i += 2) {
    if (number % i == 0) {
      return 1;
    }
  }
  return 0;
}

uint8_t isPrimeMiller(uint64_t number, unsigned int accuracy) {
  unsigned int k = 0;
  uint64_t m = number-1;
  uint64_t a, b;

  // printf("Checked Number = %ld\n", number);

  if (number < 2) {
      // printf("%ld is composite\n", number);
      return 0;
  }
  if (number % 2 == 0 && number != 2) {
      // printf("%ld is composite\n", number);
      return 0;     
  }

  while(m % 2 == 0) {
    m /= 2;
    k++;
  }
  // printf("Miller [%ld]: k = %d, m = %ld\n", number,k,m);
  for (unsigned int i = 0; i < accuracy; i++) {
    a = rand() % (number - 1) + 1;
    // printf("Miller: a = %ld\n",a);
    b = modPow(a,m,number);
    // printf("b = %ld\n", b);
    if (b == 1 || b == (number - 1)) {
      // printf("First Test - Probaly prime\n");
      continue;
    }
    for (unsigned int j = 0; j < k; j++) {
      b = modPow(b,2,number);
      if (b == 1) {
        // printf("Composite 0\n");
        return 0;
      }
      if (b == (number - 1)) {
        // printf("Second Test - Probaly prime\n");
        break;
      }
    }
    if (b != (number - 1)) {
      // printf("Composite 1\n");
      return 0;
    }
  }
  printf("%ld is probaly a prime.\n",number);
  return 1;
}

uint64_t getRandBits(uint8_t bits) {
  uint8_t i;
  uint64_t number = 0;
  for (i = 0; i < bits; i++) {
    if (rand() % 2 == 1) {
      number |= 1;
    }
    number <<= 1;
  }
  number >>= 1;
  return number;
}

uint64_t getPrime(uint8_t bits) {
  uint64_t number;
  printf("-----------------------------------------\n");
  while (1) {
    number = getRandBits(bits);
    number |= (uint64_t)(pow(2, bits - 1)) | 1;
    // printf("testing prime... %ld\n", number);
    // if (isPrime(number) == 0) {
    if (isPrimeMiller(number,5) == 1) {
      break;
    }
    // printf("finished testing prime...\n");
  }
  printf("prime number = %ld\n", number);
  return number;
}

uint64_t mulmod(uint64_t a, uint64_t b, uint64_t mod) {
    uint64_t x = 0,y = a % mod;
    while (b > 0) {
        if (b % 2 == 1) {    
            x = (x + y) % mod;
        }
        y = (y * 2) % mod;
        b /= 2;
    }
    return x % mod;
}

uint64_t modPow(uint64_t base, uint64_t exp, uint64_t mod) {
  uint64_t number = 1;
  base = base % mod;
  if (base == 0) return 0;
  while (exp) {
    if (exp & 1) {
      number = mulmod(number,base,mod); //(number * base) % mod;
    }
    exp >>= 1;
    base = mulmod(base,base,mod); //(base * base) % mod;
  }
  return number;
}
