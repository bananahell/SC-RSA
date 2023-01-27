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

uint64_t getRandBits(uint8_t bits) {
  uint8_t i;
  uint64_t number = 0;
  for (i = 0; i < bits; i++) {
    if (rand() % 2 == 1) {
      number |= 1;
    }
    number <<= 1;
  }
  return number;
}

uint64_t getPrime(uint8_t bits) {
  uint64_t number;
  while (1) {
    number = getRandBits(bits);
    number |= (uint64_t)(pow(2, bits)) | 1;
    if (isPrime(number) == 0) {
      break;
    }
  }
  return number;
}

uint64_t modPow(uint64_t base, uint64_t exp, uint64_t mod) {
  uint64_t number = 1;
  while (exp) {
    if (exp & 1) {
      number = (number * base) % mod;
    }
    exp >>= 1;
    base = (base * base) % mod;
  }
  return number;
}
