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

class NestedEncoder(SimpleEncoder):
    def __init__(self, passphrase,fields):
        super().__init__(passphrase)
        self.fields = [field.split("/") for field in fields]
        self.know_paths = []
        self.unknow_paths = [field[1] if field[0] == "*" else self.know_paths.append(field) for field in self.fields]

    def encrypt_dict(self,dict_to_encrypt: dict):
        encripted_data = self._search_unknow_path_in_dict(dict_to_encrypt.copy(),mode="encrypt")
        encripted_data = self._search_know_paths(encripted_data,mode="encrypt")
        return encripted_data

    def decrypt_dict(self,dict_to_decrypt: dict):
        decripted_data = self._search_unknow_path_in_dict(dict_to_decrypt.copy(),mode="decrypt")
        decripted_data = self._search_know_paths(decripted_data,mode="decrypt") 
        return decripted_data
    
    def encrypt_list(self,list_to_encrypt: list):
        for index,value in enumerate(list_to_encrypt):
            if isinstance(value,list):
                list_to_encrypt[index] = self.encrypt_list(value)
            if isinstance(value,dict):
                list_to_encrypt[index] = self.encrypt_dict(value)
            if isinstance(value,(str,int,float)):
                list_to_encrypt[index] = self.encrypt_str(value)
        
        return list_to_encrypt

    def decrypt_list(self,list_to_decrypt: list):
        for index,value in enumerate(list_to_decrypt):
            if isinstance(value,list):
                list_to_decrypt[index] = self.decrypt_list(value)
            if isinstance(value,dict):
                list_to_decrypt[index] = self.decrypt_dict(value)
            if isinstance(value,(str,int,float)):
                list_to_decrypt[index] = self.decrypt_str(value)
        
        return list_to_decrypt

    def _check_and_execute(self,value,mode):
        if isinstance(value,(str,int,float)):
            value = self._execute_str(str(value),mode)
        if isinstance(value,list):
            value = self._execute_in_list(value,mode)
        if isinstance(value,dict):
            value = self._execute_in_dict(value,mode)

        return value

    def _execute_in_list(self,lists,mode):
        for n,value in enumerate(lists):
            if isinstance(value,list):
                value = self._execute_in_list(value,mode)
            elif isinstance(value,dict):
                value = self._execute_in_dict(value,mode)
            else:
                lists[n] = self._execute_str(str(value),mode)
        return lists

    def _execute_in_dict(self,dic,mode):
        for value in dic.keys():
            if isinstance(dic[value],list):
                dic[value] = self._execute_in_list(dic[value],mode)
            elif isinstance(dic[value],dict):
                dic[value] = self._execute_in_dict(dic[value],mode)
            else:
                dic[value] = self._execute_str(dic[value],mode)
        return dic

    def _search_unknow_path_in_dict(self,data,mode):
        for field in data.keys():
            if field in self.unknow_paths:
                data[field] = self._check_and_execute(data[field],mode)
            elif isinstance(data[field],dict):
                self._search_unknow_path_in_dict(data[field],mode)
            elif isinstance(data[field],list):
                self._search_unknow_path_in_list(data[field],mode)
            elif data[field] == None:
                data[field] = "None"
        return data
        
    def _search_unknow_path_in_list(self,data,mode):
        for field in data:
            if isinstance(field,dict):
                self._search_unknow_path_in_dict(field,mode)
            elif isinstance(field,list):
                self._search_unknow_path_in_list(field,mode)
            elif field == None:
                field = "None"
        return data

    def _search_know_paths(self,data,mode):
        for path in self.know_paths:
            last = path[-1]
            new_data = data
            for level in path:
                if level is last:
                    new_data[level] = self._check_and_execute(new_data[level],mode)
                else:
                    new_data = new_data[level]

        return data