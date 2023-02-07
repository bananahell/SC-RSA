import hashlib
import os
import key_gen

# if key_gen.isPrime(42,5): print('PRIMO')
# else: print('NAO PRIMO')

def byte_xor(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

def MGF(z,l):
    hashFunc = hashlib.sha1()
    hLen = hashFunc.digest_size
    if (l > pow(2,32)*hLen):
       print("Mask too long!")
       exit()
    T = b''
    i = 0
    while (len(T) < l):
        c = int.to_bytes(i,4,'big')
        hashFunc.update(z+c)
        T += hashFunc.digest()
        i += 1

    return T[:l]


def RSAOAEPEnc(key,message,label):
    hashFunc = hashlib.sha1()
    msgEncode = message.encode()
    mLen = len(msgEncode)
    hLen = hashFunc.digest_size #tamanho do hash em bytes
    k = (key[1].bit_length() + 7) // 8 #tamanho da chave em bytes
    emLen = k-1 #tamanho da encoded message em bytes

    if (len(label) > pow(2,61)-1):
       print("RSAOAEP: Label too long!")
       exit()
    if (mLen > emLen - 2*hLen - 1):
       print("RSAOAEP: Message too long!")
       exit()
    
    ps = bytes(emLen - mLen - 2*hLen - 1)

    hashFunc.update(label.encode())
    lHash = hashFunc.digest()

    print(f'k: {k}, mLen: {mLen}, hLen: {hLen}, emLen: {emLen}')
    print(f'ps: {ps}')
    print(f'ps length: {len(ps)}')
    print(f'lHash: {lHash}')
    print(f'hash len: {hashFunc.digest_size}, {len(lHash)}')
    print(f'msg: {msgEncode}')

    db = lHash + ps + int.to_bytes(0X01,1,'big') + msgEncode
    print(f'db: {db}')
    print(f'dbLen: {len(db)}')

    seed = os.urandom(hLen)
    dbMask = MGF(seed,emLen-hLen)
    maskedDB = byte_xor(db,dbMask)

    print(f'seed: {seed}, seedLen: {len(seed)}')
    print(f'dbMask: {dbMask}, dbMaskLen: {len(dbMask)}')
    print(f'maskedDB: {maskedDB}, maskedDBLen: {len(maskedDB)}')

    seedMask = MGF(maskedDB,hLen)
    maskedSeed = byte_xor(seed,seedMask)

    print(f'seedMask: {seedMask}, seedMaskLen: {len(seedMask)}')
    print(f'maskedSeed: {maskedSeed}, maskedSeedLen: {len(maskedSeed)}')

    em = maskedSeed + maskedDB

    print(f'em: {em}, emLen: {len(em)}')

    intEM = int.from_bytes(em,'big')
    enc = pow(intEM,key[0],key[1])

    print(f'intEM: {intEM}')
    print(f'enc: {enc}')

    return enc

def RSAOAEPDec(key,encEM,label):
    hashFunc = hashlib.sha1()
    hLen = hashFunc.digest_size #tamanho do hash em bytes
    k = (key[1].bit_length() + 7) // 8 #tamanho da chave em bytes
    emLen = k-1 #tamanho da encoded message em bytes

    decEM = pow(encEM,key[0],key[1])
    em = int.to_bytes(decEM,emLen,'big')

    if (len(label) > pow(2,61)-1):
       print("RSAOAEP: Label too long!")
       exit()
    if (emLen < 2*hLen + 1):
       print("RSAOAEP: Decoding error")

    maskedSeed = em[0:hLen]
    maskedDB = em[hLen:]
    seedMask = MGF(maskedDB,hLen)
    seed = byte_xor(maskedSeed,seedMask)
    dbMask = MGF(seed,emLen-hLen)
    db = byte_xor(maskedDB,dbMask)

    print(f'maskedSeed: {maskedSeed}, maskedSeedLen: {len(maskedSeed)}')
    print(f'maskedDB: {maskedDB}, maskedDBLen: {len(maskedDB)}')

    print(f'seedMask: {seedMask}, seedMaskLen: {len(seedMask)}')
    print(f'seed: {seed}, seedLen: {len(seed)}')

    print(f'dbMask: {dbMask}, dbMaskLen: {len(dbMask)}')
    print(f'db: {db}')
    print(f'dbLen: {len(db)}')

    hashFunc.update(label.encode())
    lHash = hashFunc.digest()

    print(f'lHash: {lHash}')
    print(f'hash len: {hashFunc.digest_size}, {len(lHash)}')

    lHashEnc = db[0:hLen]

    print(f'lHashEnc: {lHashEnc}')
    print(f'hashEnc len: {len(lHashEnc)}')

    if (lHashEnc != lHash): 
       print('RSAOAEP: Decoding error, diffent hashes')
       exit()

    i = hLen
    while (db[i:i+1] == b'\x00'):
        i += 1
    
    message = db[i+1:]

    print(f'message: {message} {message.decode()}')
    
    


def main():

    privateKey, publicKey = key_gen.genKeys()
    # print('privateKey = ', privateKey)
    # print('publicKey = ', publicKey)

    k = (publicKey[1].bit_length() + 7) // 8 #tamanho da chave em bytes
    emLen = k-1 #tamanho da encoded message em bytes

    # enc = pow(5,privateKey[0],privateKey[1])
    # print("enc: ", enc)
    # msg = pow(enc,publicKey[0],publicKey[1])
    # print("msg: ", msg)

    enc = RSAOAEPEnc(privateKey,'Rapadura eh doce mas nao eh mole nao','')
    # dec = pow(enc,publicKey[0],publicKey[1])
    # emDec = int.to_bytes(dec,emLen,'big')
    # print(f'dec: {dec}')
    # print(f'emDec: {emDec}')

    # if (emDec == em):
    #     print("EH IGUAL")

    RSAOAEPDec(publicKey,enc,'')
    

main()