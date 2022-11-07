import logging


from fernet_gui import FernetGUI

from  cryptography.fernet import Fernet, padding

import base64


class TimeFernetGUI(FernetGUI):
    
    def decrypt(self, message):

        try:

            #get data of ciphertext
            cipher_text = message['data']

            #Convert base64 to bytes
            cipher_text = bytes(base64.b64decode(cipher_text))
            
            #Decryption with a time limit of 60 seconds
            token = Fernet(self.key)
            pt = token.decrypt(token=cipher_text, ttl=60)

            #Remove padding
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(pt) + unpadder.finalize()
            
            #Return the uncrypted message
            return data.decode('utf-8')

        except Exception as e:
            self._log.error("Error while decrypting message")
            self._log.error(e)
            return None
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()