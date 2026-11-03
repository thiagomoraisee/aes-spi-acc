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
    def __init__(self, cipherkey, plaintext, opmode=None, verbosity=2):
        self.verbosity = verbosity
        if opmode == None:
            self.plaintext  = [plaintext]
            self.opmode = "None (AES 128 Core)"
        else:
            if opmode.lower() == "ecb":
                self.plaintext  = self._ecb(plaintext)
                self.opmode = "Electronic Codebook (ECB)"
            else:
                raise ValueError("Unsuported operation mode:", opmode)
        self.cipherkey  = cipherkey
        self.ciphertext = []
        self.exp_key = []
        self.tsize = len(self.plaintext)
        self.core = AESCore(self.cipherkey, self.plaintext[0])

        if self.verbosity >= 1:
            print("\n" + 7*" " +"-----===[ AES 128 ]===-----\n")
            print(f"> Operation Mode: {self.opmode}")
            print(f"> Cipher Key: {self.cipherkey}")
            print(f"> Plain Text: ", end="")
            for block in self.plaintext:
                print(block+"\n"+14*" ", end="")
            print("")

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

        # Step 0 : Expand Key
        self.core.key_expansion()
        self.exp_key = self.core.exp_key # Save expanded key
        if self.verbosity >= 2:
            print(15*" "+f"# ROUND {self.core.round} #")
            print(f"> Key Expansion:")
            matview(self.exp_key,
                    shift   = 3,
                    ljust   = "right",
                    llabels = [f"Word {i:02d} :  " for i in range(len(self.exp_key))],
                    rlabels = [f"  : Round {int(i/4):02d}" for i in range(len(self.exp_key))])

        # Iterate rounds loops for each text block:
        for i in range(self.tsize):

            self.core.__init__(self.cipherkey, self.plaintext[i])
            self.core.exp_key = self.exp_key
            if self.verbosity >= 2:
                print(f"> Initial State:")
                matview(self.core.state, shift=14)

            self.core.add_round_key()
            if self.verbosity >= 2:
                print(f"> Add Round Key:")
                matview(self.core.state, shift=14)

            while self.core.round < 9:
                self.core.round += 1
                self.core.sub_bytes()
                if self.verbosity >= 2:
                    print("\n"+15*" "+f"# ROUND {self.core.round} #")
                    print(f"> Sub Bytes:")
                    matview(self.core.state, shift=14)

                self.core.shift_rows()
                if self.verbosity >= 2:
                    print(f"> Shift Rows:")
                    matview(self.core.state, shift=14)

                self.core.mix_columns()
                if self.verbosity >= 2:
                    print(f"> Mix Columns:")
                    matview(self.core.state, shift=14)

                self.core.add_round_key()
                if self.verbosity >= 2:
                    print(f"> Add Round Key:")
                    matview(self.core.state, shift=14)

            self.core.round += 1
            self.core.sub_bytes()
            if self.verbosity >= 2:
                print("\n"+15*" "+f"# ROUND {self.core.round} #")
                print(f"> Sub Bytes:")
                matview(self.core.state, shift=14)

            self.core.shift_rows()
            if self.verbosity >= 2:
                print(f"> Shift Rows:")
                matview(self.core.state, shift=14)

            self.core.add_round_key()
            if self.verbosity >= 2:
                print(f"> Add Round Key:")
                matview(self.core.state, shift=14)

            output = join(self.core.state)
            self.ciphertext.append(output)
            if self.verbosity >= 1:
                print(f"\n> CIPHER BLOCK ({i+1}/{self.tsize}): {output}\n")

def gen_key_text_files(dir="."):
    if dir.find(" ") == -1:
        keyfile  = f"{dir}/key.hex"
        textfile = f"{dir}/text.hex"

        key_msg_ascii  = "Thats my Kung Fu"
        text_msg_ascii = "Two One Nine Two"

        print(f"[INFO] Generating {keyfile} ... ", end="")
        key_msg_hex  = key_msg_ascii.encode("ascii").hex()
        write_hex_file(keyfile, key_msg_hex)
        print("DONE")

        print(f"[INFO] Generating {textfile} ... ", end="")
        text_msg_hex = text_msg_ascii.encode("ascii").hex()
        write_hex_file(textfile, text_msg_hex)
        print("DONE")
    else:
        raise ValueError(f"Invalid directory ('{dir}')")

# MAIN FUNCTION:
if __name__ == "__main__":
    import os
    filedir  = "."
    keyfile  = f"{filedir}/key.hex"
    textfile = f"{filedir}/text.hex"

    if not os.path.isfile(keyfile) or not os.path.isfile(textfile):
        gen_key_text_files(filedir)

    print(f"[INFO] Reading Cipher Key from {keyfile} file...", end="")
    key = read_hex_file(keyfile)
    print("DONE")
    print("HEX  : ",key)
    print("ASCII: ",bytes.fromhex(key).decode("ascii"))

    print(f"[INFO] Reading Plain Text from {textfile} file...", end="")
    text = read_hex_file(textfile)
    print("DONE")
    print("HEX  : ",text)
    print("ASCII: ",bytes.fromhex(text).decode("ascii"))

    aes = AES(cipherkey=key,
              plaintext=text,
              opmode=None,
              verbosity=1)

    aes.encript()
