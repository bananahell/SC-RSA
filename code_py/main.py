
import sys
import keyGen
import signature
    
def main():

    if (len(sys.argv) != 3 or (sys.argv[1] != '-s' and sys.argv[1] != '-v')):
       print("Comando invalido.")
       print("'-s file': assinar mensagem")
       print("'-v file': verificar assinatura")
       return
    if (sys.argv[1] == '-s'):
       privateKey, publicKey = keyGen.genKeys()
       print('Chaves geradas ----------------------------------')
       print(f'privateKey (e,N) = {privateKey}\n')
       print(f'publicKey (d,N) = {publicKey}\n')
       signature.signMsg(sys.argv[2],publicKey,privateKey)
    elif (sys.argv[1] == '-v'):
       signature.verifySignature(sys.argv[2])

    # enc, encBytes = RSAOAEPEnc(privateKey,'Rapadura eh doce mas nao eh mole nao','')
    # RSAOAEPDec(publicKey,enc,'')
    
if __name__ == "__main__":
    main()