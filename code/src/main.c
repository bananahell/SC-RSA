#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "prime_nums.h"
#include "rsa.h"

/*
 * Following tutorials:
 * https://www.youtube.com/watch?v=rLR8WcXy03Q
 * https://www.youtube.com/watch?v=oOcTVTpUsPQ
 *
 * p and q = random primes
 * n = p * q
 * fi_n = ammount of numbers coprime with n
 */

int main() {
  uint64_t bitSize = 4;
  uint64_t p1 = getPrime(bitSize);
  uint64_t q1 = getPrime(bitSize);
  uint64_t n1 = p1 * q1;
  uint64_t fi_n1 = (p1 - 1) * (q1 - 1);
  uint64_t pubKey1 = getHighestCoprime(p1, q1);
  uint64_t prvKey1;
  uint64_t p2 = getPrime(bitSize);
  uint64_t q2 = getPrime(bitSize);
  uint64_t n2 = p2 * q2;
  uint64_t fi_n2 = (p2 - 1) * (q2 - 1);
  uint64_t pubKey2 = getHighestCoprime(p2, q2);
  uint64_t prvKey2;
  uint64_t msg = getPrime(bitSize);
  uint64_t sent[2];
  uint64_t i;
  printf("\n");
  srand(time(NULL));

  printf("Sender:\n\n");

  printf("p1 = %lu\nq1 = %lu\nn1 = %lu\nfi_n1 = %lu\n\n", p1, q1, n1, fi_n1);

  printf("getHighestCoprime(%lu, %lu) = %lu\n\n", p1, q1, pubKey1);

  printf("available private keys [1-5] (picking last always):\n");
  for (i = 1; i < 6; i++) {
    prvKey1 = (fi_n1 * i) - 1;
    printf("private key: (%lu * %lu) - 1 = %lu\n", fi_n1, i, prvKey1);
  }

  printf("\nReceiver:\n\n");

  printf("p2 = %lu\nq2 = %lu\nn2 = %lu\nfi_n2 = %lu\n\n", p2, q2, n2, fi_n2);

  printf("getHighestCoprime(%lu, %lu) = %lu\n\n", p2, q2, pubKey2);

  printf("available private keys [1-5] (picking last always):\n");
  for (i = 1; i < 6; i++) {
    prvKey2 = (fi_n2 * i) - 1;
    printf("private key: (%lu * %lu) - 1 = %lu\n", fi_n2, i, prvKey2);
  }

  printf("\nSending %lu:\n\n", msg);

  sent[0] = modPow(msg, pubKey2, n2);
  printf("encrypt: modPow(%lu, %lu, %lu) = %lu\n", msg, pubKey2, n2, sent[0]);
  sent[0] = modPow(sent[0], prvKey2, n2);
  printf("decrypt: modPow(sent[0], %lu, %lu) = %lu\n\n", prvKey2, n2, sent[0]);

  sent[1] = modPow(msg, prvKey1, n1);
  printf("verification sent: modPow(%lu, %lu, %lu) = %lu\n", msg, prvKey1, n1,
         sent[1]);
  sent[1] = modPow(sent[1], pubKey1, n1);
  printf("verification received: modPow(sent[1], %lu, %lu) = %lu\n\n", pubKey1,
         n1, sent[1]);

  if (sent[0] == sent[1]) {
    printf("decryption and verification matched!\n");
  } else {
    printf("something went wrong...");
  }

  printf("\n");
  return 0;
}
