
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from getpass import getpass

class ICrypto:

    def get_algorithm_mappping(self, algorithm, sig=None):
        algorithm_mappping = {
            'AES': '01',
            'DES': '02',
            'DES3': '03',
            'Blowfish': '04',
            'Camellia': '05',
            'CAST5': '06',
            'IDEA': '07',
            'RC2': '08',
            'RC4': '09',
            'RC5': '0a',
        }
        if sig:
            for k, v in algorithm_mappping.items():
                if v == sig: return k
        return algorithm_mappping[algorithm]

    def get_hashed_pw(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(getpass(), 'utf-8'))
        return digest.finalize()

    def get_text_data_padding(self, data) -> bytes:
        size = len(data)
        remiander = size%16
        if remiander != 0: data = data.rjust(size+(16-remiander))
        return data
        
    def encrypt(self, data, algorithm='AES'):
        algo_sig = self.get_algorithm_mappping(algorithm, None)
        data = self.get_text_data_padding(bytes(data, 'utf-8'))
        if algorithm == 'AES':
            cipher = Cipher(algorithms.AES(self.get_hashed_pw()), modes.ECB())
        encryptor = cipher.encryptor()
        return (encryptor.update(data)+encryptor.finalize()).hex() + algo_sig

    def decrypt(self, data):
        algorithm = self.get_algorithm_mappping(None, data[-2:])
        data = bytes.fromhex(data[:-2])
        if algorithm == 'AES':
            cipher = Cipher(algorithms.AES(self.get_hashed_pw()), modes.ECB())
        decryptor = cipher.decryptor()
        return (decryptor.update(data)+decryptor.finalize()
                                                ).decode('utf-8').lstrip()


icrypto = ICrypto()

if __name__ == '__main__':
    ic = ICrypto()
    bb = ic.encrypt("Hello World")
    print('Encrypted:', bb)
    print('Decrypted:', ic.decrypt(bb))


