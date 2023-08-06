from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SimpleEncoder:
    def __init__(self,passphrase):
        self.key = self._generate_key(passphrase.encode("utf-8"))
    
    def _generate_key(self,passphrase):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=passphrase,
            iterations=100000,
            backend=default_backend()
        )
        return urlsafe_b64encode(kdf.derive(passphrase)) 
        
    def encrypt_str(self,str_to_encrypt: str):
        return self._execute_str(str_to_encrypt,mode="encrypt")
    
    def decrypt_str(self,str_to_decrypt: str):
        return self._execute_str(str_to_decrypt,mode="decrypt")

    def _execute_str(self,field,mode):
        encrypter = Fernet(self.key)
        if mode == "encrypt":
            return encrypter.encrypt(field.encode("utf-8")).decode("utf-8")
        if mode == "decrypt":
            return encrypter.decrypt(field.encode("utf-8")).decode("utf-8")