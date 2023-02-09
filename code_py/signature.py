import hashlib
import os
import sys
import base64

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
    msgEncode = message
    if (type(message) == str):
        msgEncode = msgEncode.encode()
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

    # Informacoes do algoritmo OAEP
    # print(f'k: {k}, mLen: {mLen}, hLen: {hLen}, emLen: {emLen}')
    # print(f'ps: {ps}')
    # print(f'ps length: {len(ps)}')
    # print(f'lHash: {lHash}')
    # print(f'hash len: {hashFunc.digest_size}, {len(lHash)}')
    # print(f'msg: {msgEncode}')

    db = lHash + ps + int.to_bytes(0X01,1,'big') + msgEncode
 
    # print(f'db: {db}')
    # print(f'dbLen: {len(db)}')

    seed = os.urandom(hLen)
    dbMask = MGF(seed,emLen-hLen)
    maskedDB = byte_xor(db,dbMask)

    # print(f'seed: {seed}, seedLen: {len(seed)}')
    # print(f'dbMask: {dbMask}, dbMaskLen: {len(dbMask)}')
    # print(f'maskedDB: {maskedDB}, maskedDBLen: {len(maskedDB)}')

    seedMask = MGF(maskedDB,hLen)
    maskedSeed = byte_xor(seed,seedMask)

    # print(f'seedMask: {seedMask}, seedMaskLen: {len(seedMask)}')
    # print(f'maskedSeed: {maskedSeed}, maskedSeedLen: {len(maskedSeed)}')

    em = maskedSeed + maskedDB

    # print(f'em: {em}, emLen: {len(em)}')

    intEM = int.from_bytes(em,'big')
    enc = pow(intEM,key[0],key[1])

    # print(f'intEM: {intEM}')
    # print(f'enc: {enc}')

    encBytes = int.to_bytes(enc,(enc.bit_length() + 7) // 8,'big')
    # print(f'encBytes: {encBytes} len: {len(encBytes)}')

    print(f'Mensagem com o padding OAEP: {em}\n')

    return enc, encBytes

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

    # print(f'maskedSeed: {maskedSeed}, maskedSeedLen: {len(maskedSeed)}')
    # print(f'maskedDB: {maskedDB}, maskedDBLen: {len(maskedDB)}')
    # print(f'seedMask: {seedMask}, seedMaskLen: {len(seedMask)}')
    # print(f'seed: {seed}, seedLen: {len(seed)}')
    # print(f'dbMask: {dbMask}, dbMaskLen: {len(dbMask)}')
    # print(f'db: {db}')
    # print(f'dbLen: {len(db)}')

    hashFunc.update(label.encode())
    lHash = hashFunc.digest()

    # print(f'lHash: {lHash}')
    # print(f'hash len: {hashFunc.digest_size}, {len(lHash)}')

    lHashEnc = db[0:hLen]

    # print(f'lHashEnc: {lHashEnc}')
    # print(f'hashEnc len: {len(lHashEnc)}')

    if (lHashEnc != lHash): 
       print('RSAOAEP: Decoding error, diffent label hashes')
       exit()

    i = hLen
    while (db[i:i+1] == b'\x00'):
        i += 1
    
    message = db[i+1:]

    # print(f'message: {message}')

    return message #retorna hash da mensagem no caso da assinatura
    
def signMsg(file,publicKey,privateKey):
    print('Assinatura da mensagem ----------------------------------')

    f = open(file, "r")
    message = f.read()
    print(f'Menssagem: {message}\n')

    hashFunc = hashlib.sha3_512()
    hashFunc.update(message.encode())
    hashMsg = hashFunc.digest()
    sign, signBytes = RSAOAEPEnc(privateKey,hashMsg,'')
    print(f"Hash da mensagem [H(m)]: {hashMsg}\n")

    signBase64 = base64.b64encode(signBytes)
    dSize = (publicKey[0].bit_length() + 7) // 8 #tamanho do parametro d da chave publica em bytes
    nSize = (publicKey[1].bit_length() + 7) // 8 #tamanho do parametro n da chave publica em bytes
    dBase64 = base64.b64encode(int.to_bytes(publicKey[0],dSize,'big'))
    nBase64 = base64.b64encode(int.to_bytes(publicKey[1],nSize,'big'))

    print(f"Assinatura do hash com OAEP em base64 [RSA(OAEP(H(m)))]: {signBase64}\n")

    f = open("signature.txt", "w")
    f.write(base64.b64encode(message.encode()).decode())
    f.write('\n')
    f.write(dBase64.decode())
    f.write('\n')
    f.write(nBase64.decode())
    f.write('\n')
    f.write(signBase64.decode())
    f.close()
    
def verifySignature(file):
    print('Verificacao da assinatura da mensagem ----------------------------------')

    f = open(file, "r")
    messageB64 = f.readline().rstrip('\n')      
    publicKey = (f.readline().rstrip('\n'), f.readline().rstrip('\n')) #read (d,n)
    sign = f.readline().rstrip('\n')
    # print('messageB64: ', messageB64)
    # print('publicKey: ', publicKey)
    # print('sign: ', sign)

    publicKey = (int.from_bytes(base64.b64decode(publicKey[0].encode()),'big'),
                 int.from_bytes(base64.b64decode(publicKey[1].encode()),'big'))
    sign = int.from_bytes(base64.b64decode(sign.encode()),'big')

    hashMsgSign = RSAOAEPDec(publicKey,sign,'')

    message = base64.b64decode(messageB64.encode())
    hashFunc = hashlib.sha3_512()
    hashFunc.update(message)
    hashMsg = hashFunc.digest()
    #print('message: ', message)

    print(f"Hash retirado da assinatura, com o OAEP desfeito: {hashMsgSign}\n")    
    print(f"Hash da mensagem original: {hashMsg}\n")    

    if (hashMsgSign == hashMsg):
       print('Assinatura válida.')
    else:
       print('Assinatura não válida.')