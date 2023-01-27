#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "prime_nums.h"

/*
 * Following tutorial:
 * https://www.youtube.com/watch?v=rLR8WcXy03Q
 */

int main() {
  uint64_t bobPublic = 571;
  uint64_t bobPrivate = 835;
  uint64_t bobMod = 1073;
  uint64_t alicePublic = 103;
  uint64_t alicePrivate = 647;
  uint64_t aliceMod = 2059;
  uint64_t msg = 331;
  uint64_t number[2];
  printf("\n");
  srand(time(NULL));

  printf("%lu is a random prime number with 20 bits!\n\n", getPrime(20));

  printf("Bob's public key: %lu\n", bobPublic);
  printf("Bob's private key: %lu\n", bobPrivate);
  printf("Bob's mod key: %lu\n\n", bobMod);
  printf("Alice's public key: %lu\n", alicePublic);
  printf("Alice's private key: %lu\n", alicePrivate);
  printf("Alice's mod key: %lu\n\n", aliceMod);

  number[0] = modPow(msg, bobPublic, bobMod);
  printf("encrypt: modPow(%lu, %lu, %lu) = %lu\n", msg, bobPublic, bobMod,
         number[0]);
  number[0] = modPow(number[0], bobPrivate, bobMod);
  printf("decrypt: modPow(number[0], %lu, %lu) = %lu\n\n", bobPrivate, bobMod,
         number[0]);

  number[1] = modPow(msg, alicePrivate, aliceMod);
  printf("verification sent: modPow(%lu, %lu, %lu) = %lu\n", msg, alicePrivate,
         aliceMod, number[1]);
  number[1] = modPow(number[1], alicePublic, aliceMod);
  printf("verification received: modPow(number[1], %lu, %lu) = %lu\n\n",
         alicePublic, aliceMod, number[1]);

  if (number[0] == number[1]) {
    printf("decryption and verification matched!\n");
  } else {
    printf("something went wrong...");
  }
  printf("\n");
  return 0;
}
