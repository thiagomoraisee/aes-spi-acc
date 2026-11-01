"""
==========================================================================================
SOFTEX @ CIEXPERT 2026 (UFCG/CEEI)                                              2026.10.16 
------------------------------------------------------------------------------------------
Script     : aes.py
Author     : Thiago M. de Oliveira <thiagomoraisee@gmail.com>
Description: A simple AES algorithm validation script.
==========================================================================================
"""
from utils import *

class AESCore:
    def __init__(self, key, text):
        self.key = hex2list(key)
        self.text = hex2list(text)
        self.key_size_bits = 128
        self.num_round_keys = 11
        self.exp_key = []
        self.round = 0
        self.state = [self.text[4*i : 4*(i+1)] for i in range(4)]

    def key_expansion(self):
        N = int(self.key_size_bits/32) # Number of words of 32 bits per key
        for i in range(4*self.num_round_keys):
            if i < N:
                self.exp_key.append(self.key[4*i : 4*(i+1)])
            elif (i >= N) and (i % N == 0):
                rot_cons = rcon(i/N)
                rot_word = rot(self.exp_key[i-1], 1)
                exp_key_item = []
                for j in range(4):
                    lsb = 0x0F & rot_word[j]
                    msb = rot_word[j] >> 4
                    sub_word = SBOX[msb][lsb]
                    exp_key_item.append(self.exp_key[i-N][j] ^ sub_word ^ rot_cons[j])
                self.exp_key.append(exp_key_item)
            else:
                self.exp_key.append( [w1 ^ w2 for w1, w2 in zip(self.exp_key[i-N], self.exp_key[i-1])] )

    def add_round_key(self):
        round_key = self.exp_key[4*self.round : 4*(self.round+1)]
        for i in range(4):
            for j in range(4):
                self.state[i][j] = self.state[i][j] ^ round_key[i][j]

    def sub_bytes(self):
        for i in range(4):
            for j in range(4):
                lsb = 0x0F & self.state[i][j]
                msb = self.state[i][j] >> 4
                self.state[i][j] = SBOX[msb][lsb]

    def shift_rows(self):
        state_t = transpose(self.state)
        for i in range(4):
            self.state[i] = rot(state_t[i], i)
        self.state = transpose(self.state)

    def mix_columns(self):
        result = [[0x00 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] ^= gfmult(self.state[i][k], MMIX[k][j]) 
        self.state = result

class AES:
    def __init__(self, cipherkey, plaintext):
        self.cipherkey  = cipherkey
        self.plaintext  = self._ecb(plaintext)
        self.ciphertext = []
        self.exp_key = []
        self.tsize = len(self.plaintext)
        self.core = AESCore(self.cipherkey, self.plaintext[0])

    def _ecb(self, text):
        ecb_text_list = []
        blocks  = int(len(text)/32) + 1
        padding = len(text)%32
        padding = 32 - padding
        padded_text = text + (int(padding/2))*f"{int(padding/2):02x}"
        for i in range(blocks):
            if i < blocks:
                ecb_text_list.append(padded_text[32*i : 32*(i+1)])
        return ecb_text_list
        
    def encript(self):
        self.core.key_expansion()
        self.exp_key = self.core.exp_key # Save expanded key
        for i in range(self.tsize):
            self.core.__init__(self.cipherkey, self.plaintext[i])
            self.core.exp_key = self.exp_key
            self.core.add_round_key()
            while self.core.round < 9:
                self.core.round += 1
                self.core.sub_bytes()
                self.core.shift_rows()
                self.core.mix_columns()
                self.core.add_round_key()
            self.core.round += 1
            self.core.sub_bytes()
            self.core.shift_rows()
            self.core.add_round_key()
            output = join(self.core.state)
            self.ciphertext.append(output)

def main():
    print("\n-----===[ AES 128 Core Simulator ]===-----\n")

    key = "Thats my Kung Fu".encode('ascii').hex()
    text = "Two One Nine Two".encode('ascii').hex()

    aes = AESCore(key, text)
    aes.key_expansion()

    print(f"Plain Text  : {text}")
    print(f"Cipher Key  : {key}")
    print(f"Expanded Key: ")
    matview(aes.exp_key,
            shift   = 3,
            ljust   = "right",
            llabels = [f"Word {i:02d} :  " for i in range(len(aes.exp_key))],
            rlabels = [f"  : Round {int(i/4):02d}" for i in range(len(aes.exp_key))])

    print(f"             .-------------.")
    print(f"       ---== |  ROUND #{aes.round:02d}  | ==---")
    print(f"             '-------------'")
    print(f"Initial State: ")
    matview(aes.state, shift=14)

    print(f"Add Round Key: ")
    aes.add_round_key()
    matview(aes.state, shift=14)

    while aes.round < 9:

        aes.round += 1

        print(f"             .-------------.")
        print(f"       ---== |  ROUND #{aes.round:02d}  | ==---")
        print(f"             '-------------'")

        print(f"Substitution Bytes:")
        aes.sub_bytes()
        matview(aes.state, shift=14)

        print(f"Shift rows:")
        aes.shift_rows()
        matview(aes.state, shift=14)

        print(f"Mix Columns:")
        aes.mix_columns()
        matview(aes.state, shift=14)

        print(f"Add Round Key: ")
        aes.add_round_key()
        matview(aes.state, shift=14)

    # AES Final Round

    aes.round += 1
    print(f"             .-------------.")
    print(f"       ---== |  ROUND #{aes.round:02d}  | ==---")
    print(f"             '-------------'")

    print(f"Substitution Bytes:")
    aes.sub_bytes()
    matview(aes.state, shift=14)

    print(f"Shift rows:")
    aes.shift_rows()
    matview(aes.state, shift=14)

    print(f"Add Round Key: ")
    aes.add_round_key()
    matview(aes.state, shift=14)

    print(join(aes.state))

if __name__ == "__main__":
    key = "Thats my Kung Fu".encode('ascii').hex()
    text = "This is a long long secret text e".encode('ascii').hex()
    aes = AES(cipherkey=key, plaintext=text)
    aes.encript()
    print(aes.ciphertext)

