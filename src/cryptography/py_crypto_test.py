# from Crypto.Cipher import AES
# Encryption
# encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")

# Decryption
# decrypt# ion_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# plain_text = decryption_suite.decrypt(cipher_text)

import hashlib
md5 = hashlib.md5()
# md5.update('Python rocks!')

# md5.update(b'Python rocks!')
# md5.digest()

sha = hashlib.sha1(b'Hello Python').hexdigest()
print(sha)
