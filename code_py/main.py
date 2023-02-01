import key_gen

# if key_gen.isPrime(42,5): print('PRIMO')
# else: print('NAO PRIMO')

def main():

    keys = key_gen.genKeys()
    print(keys)

    enc = pow(5,keys['privateKey'][0],keys['privateKey'][1])
    print("enc: ", enc)
    msg = pow(enc,keys['publicKey'][0],keys['publicKey'][1])
    print("msg: ", msg)

main()