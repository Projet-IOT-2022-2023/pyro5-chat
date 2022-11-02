import logging

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback

from basic_gui import BasicGUI

#import cryptography

import os, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf import pbkdf2
from cryptography.hazmat.primitives import hashes

# default values used to populate connection window
DEFAULT_VALUES = {
    "host" : "127.0.0.1",
    "port" : "6666",
    "name" : "foo",
    "password" : ""
}

class CipheredGUI(BasicGUI):
    def __init__(self, key=None):
        self.key = key
        super().__init__()
    
    def _create_connection_window(self):
        # windows about connexion
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            
            for field in ["host", "port", "name", "password"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
                    
            dpg.add_button(label="Connect", callback=self.run_chat)

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
        #self._client.register(password)
        #derivation of the key
        self.key = pbkdf2.PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=100000,
        ).derive(password.encode('utf-8'))

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message):

        #Create initialisation vector
        iv = os.urandom(16)

        #Add padding to get 16 bytes multiple
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(bytes(message,'utf-8')) + padder.finalize()

        #Encryption
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()

        #Return the initialisation vector and the encrypted message
        return (iv, ct)
    
    def decrypt(self, message):

        #Get initialisation vector and encrypted message
        iv, ciphertext = message
        #decode base64
        ciphertext = base64.b64decode(ciphertext)
        print("iv : ", iv)
        iv = bytes(iv,'utf-8')
        
        #Decryption
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        pt = decryptor.update(ciphertext) + decryptor.finalize()

        #Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(pt) + unpadder.finalize()
        
        #Return the uncrypted message
        return data.decode('utf-8')
        
    def send(self, text)->None:
        # function called to send a message to all (broadcasting)
        self._client.send_message(self.encrypt(text))

    def recv(self)->None:
        # function called to get incoming messages and display them
        if self._callback is not None:
            for user, message in self._callback.get():
                self.update_text_screen(f"{user} : {self.decrypt(message)}")
                self._callback.clear()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()