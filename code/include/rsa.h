#ifndef RSA_H
#define RSA_H

#include <stdint.h>

extern const uint64_t PRIMES10K[1229];

uint64_t keyGen(uint64_t, uint64_t);
uint64_t getHighestCoprime(uint64_t, uint64_t);

#endif /* RSA_H */
