#ifndef PRIME_NUMS
#define PRIME_NUMS

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

/**
 * @brief Power modulus operation.
 * @param base Base of the power operation.
 * @param exp Exponent of the power operation.
 * @param mod Modulus used on the result of the power operation.
 * @return (base ^ exp) % mod
 */
uint64_t modPow(uint64_t, uint64_t, uint64_t);

#endif /* PRIME_NUMS */
