import logging


from fernet_gui import FernetGUI

from cryptography.hazmat.primitives import padding

from  cryptography.fernet import Fernet

import base64


class TimeFernetGUI(FernetGUI):
    
    def decrypt(self, message):

        try:

            #get data of ciphertext
            ciphertext = message['data']

            #Convert base64 to bytes
            ciphertext = bytes(base64.b64decode(ciphertext))
            
            #Decryption
            token = Fernet(self.key)
            pt = token.decrypt(token=ciphertext, ttl=60)

            #Remove padding
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(pt) + unpadder.finalize()
            
            #Return the uncrypted message
            return data.decode('utf-8')

        except:
            return None
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()