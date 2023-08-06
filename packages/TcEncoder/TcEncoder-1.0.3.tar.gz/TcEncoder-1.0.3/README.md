<div id="logos">
    <p align="center">
        <img src="https://i.ibb.co/WPjgQwc/logo-2.png" width="150" height="150">
        <img src="https://tc.com.br/wp-content/themes/tradersclub/img/tc-out.png" width="150" height="150">
    </p>
</div>   
<br>

<h1 align="center">TcEncoder</h1>
<h2 align="center">This lib was created to encrypt and decrypt data more easiely.</h2>
<br>
<br>

<h1 align="left">Import</h1>

```py
from TcEncoder import SimpleEncoder,NestedEncoder
```

<br>

<h2 align="left">SimpleEncoder</h2>
We have to set a password to encrypt, the same password must to be passed when you want to decrypt.
<br>
<br>

```py
password = "some_pass"
se = SimpleEncoder(password)

string = "some_word"

# encrypting ...
encrypted = se.encrypt_str(string)
print(encrypted)

# decrypting ...
decrypted = se.decrypt_str(encrypted)
print(decrypted)

```
result:
```sh
# encrypted
$ gAAAAABhXvHQK{...}i9oHlgMZlv9SzLyfw==
# {...} was used to shorten the string length

# decrypted
$ some_word
```

<h2 align="left">NestedEncoder</h2>

The Nested encoder is a class based in SimpleEncoder class, so it can do the same as SimpleEncoder plus further encrypt and decrypt `list` or `dict`.

We have to set two paramns:
- A password to encrypt/decrypt.
- A list of fields we want encrypt/decrypt. [See how set fields here](https://github.com/tradersclub/TCPythonUtils/blob/main/TcEncoderLib/NESTED_EXAMPLES.md)
<br>
<br>

```py
password = "some_pass"
list_fields = ["encrypt"]

se = NestedEncoder(password,list_fields)

dict_example = {
    "encrypt": {
        "value1": "value",
        "value2": "value"
    },
    "dont_encrypt": {
        "value1": "value",
        "value2": "value"
    }
}

encrypted =  se.encrypt_dict(dict_example)
print(encrypted)

decrypted = se.decrypt_dict(encrypted)
print(decrypted)
```

```
$ {'encrypt': {'value1': 'gAAAAAB{...}apuFA==','value2': 'gAAAAAB{...}tBBkg=='},'dont_encrypt': {'value1': 'value','value2': 'value'}}


$ {'encrypt': {'value1': 'value','value2': 'value'},'dont_encrypt': {'value1': 'value','value2': 'value'}}
```

