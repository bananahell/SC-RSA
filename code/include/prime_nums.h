#ifndef PRIME_NUMS_H
#define PRIME_NUMS_H

#include <stdint.h>

#define FERMAT_PRIME 65537

/**
 * @brief Check if is prime.
 * @param number Number to be checked.
 * @return Zero if prime, one otherwise.
 */
uint8_t isPrime(uint64_t);

/**
 * @brief Gets random number with bit size.
 * @param bits Ammount of bits.
 * @return Random number with bit size.
 */
uint64_t getRandBits(uint8_t);

/**
 * @brief Gets random prime number.
 * @param bits Ammount of bits.
 * @return A random prime number with bit size.
 */
uint64_t getPrime(uint8_t);

uint64_t mulmod(uint64_t a, uint64_t b, uint64_t mod);

/**
 * @brief Power modulus operation.
 * @param base Base of the power operation.
 * @param exp Exponent of the power operation.
 * @param mod Modulus used on the result of the power operation.
 * @return (base ^ exp) % mod
 */
uint64_t modPow(uint64_t, uint64_t, uint64_t);

uint8_t isPrimeMiller(uint64_t number, unsigned int accuracy);

#endif /* PRIME_NUMS_H */
