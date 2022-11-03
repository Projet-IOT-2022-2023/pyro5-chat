import logging

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback

from ciphered_gui import CipheredGUI

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes

from  cryptography.fernet import Fernet

import base64

class FernetGUI(CipheredGUI):

    def run_chat(self, sender, app_data)->None:
        # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)
        
        #Hash the password to get the key (Fernet needs 32 bytes key)
        h = hashes.Hash(hashes.SHA256() , backend=None)
        h.update(password.encode('utf-8'))
        hashed_password = h.finalize()
        self.key = base64.b64encode(hashed_password)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message):

        #Add padding to get 16 bytes multiple
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(bytes(message,'utf-8')) + padder.finalize()

        #Encryption with Fernel HMAC method
        ct = Fernet(self.key)
        token = ct.encrypt(padded_data)

        #Return the initialisation vector and the encrypted message
        return token
    
    def decrypt(self, message):

        try:

            #get data of ciphertext
            ciphertext = message['data']

            #Convert base64 to bytes
            ciphertext = bytes(base64.b64decode(ciphertext))
            
            #Decryption
            token = Fernet(self.key)
            pt = token.decrypt(ciphertext)

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
    client = FernetGUI()
    client.create()
    client.loop()