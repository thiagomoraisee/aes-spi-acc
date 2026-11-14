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

    def encript(self, verbose=False):

        if verbose:
            print(f"> Initial State:")
            matview(self.state, shift=14)

        self.add_round_key()
        if verbose:
            print(f"> Add Round Key:")
            matview(self.state, shift=14)

        while self.round < 9:
            self.round += 1

            self.sub_bytes()
            if verbose :
                print("\n"+15*" "+f"# ROUND {self.round} #")
                print(f"> Sub Bytes:")
                matview(self.state, shift=14)

            self.shift_rows()
            if verbose:
                print(f"> Shift Rows:")
                matview(self.state, shift=14)

            self.mix_columns()
            if verbose:
                print(f"> Mix Columns:")
                matview(self.state, shift=14)

            self.add_round_key()
            if verbose:
                print(f"> Add Round Key:")
                matview(self.state, shift=14)

        self.round += 1

        self.sub_bytes()
        if verbose:
            print("\n"+15*" "+f"# ROUND {self.round} #")
            print(f"> Sub Bytes:")
            matview(self.state, shift=14)

        self.shift_rows()
        if verbose:
            print(f"> Shift Rows:")
            matview(self.state, shift=14)

        self.add_round_key()
        if verbose:
            print(f"> Add Round Key:")
            matview(self.state, shift=14)



class AES:
    def __init__(self, cipherkey, plaintext, iv=None, opmode=None, verbosity=2):
        self.verbosity = verbosity
        self.sup_opmode_dict = {"none" : "None (AES 128 Core)",
                                "ecb"  : "Electronic Codebook (ECB)",
                                "cbc"  : "Cipher Block Chaining (CBC)",
                                "pcbc" : "Propagating Cipher Block Chaining (PCBC)",
                                "cfb"  : "Cipher Feedback Mode (CFB)",
                                "ofb"  : "Output Feedback Mode (OFB)",
                                "ctb"  : "Counter Mode (CTB)"}
        if opmode == None:
            self.plaintext  = [plaintext]
            self.opmode = "none"
        else:
            self.plaintext  = self._format_blocks(plaintext)
            self.opmode = opmode.lower()
            if self.opmode not in self.sup_opmode_dict.keys():
                raise ValueError("Unsuported operation mode:", self.opmode)

        self.cipherkey  = cipherkey
        self.ciphertext = []
        self.exp_key = []
        self.iv = hex2list(iv)
        self.tsize = len(self.plaintext)

        # AES128 core instanciation:
        self.core = AESCore(self.cipherkey, self.plaintext[0])

        if (self.iv is None) and (self.opmode not in ["none", "ecb"]):
            raise ValueError("You must specify input vector")

        if self.verbosity >= 1:
            print("\n" + 7*" " +"-----===[ AES 128 ]===-----\n")
            print(f"> Operation Mode: {self.sup_opmode_dict[self.opmode]}")
            print(f"> Cipher Key: {self.cipherkey}")
            print(f"> Plain Text: ", end="")
            for block in self.plaintext:
                print(block+"\n"+14*" ", end="")
            print("")

    def _format_blocks(self, text):
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

        # Expand Key
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

        # -----=== ELECTRONIC CODEBOOK (ECB) MODE ===----- # 
        if self.opmode in ["ecb", "none"]:
            # Iterate rounds loops for each text block:
            for i in range(self.tsize):

                self.core.__init__(self.cipherkey, self.plaintext[i])
                self.core.exp_key = self.exp_key

                self.core.encript(verbose=self.verbosity >= 2)

                output = join(self.core.state)
                self.ciphertext.append(output)
                if self.verbosity >= 1:
                    print(f"\n> CIPHER BLOCK ({i+1}/{self.tsize}): {output}\n")

        # -----=== CIPHER BLOCK CHAINING (CBC) MODE ===----- # 
        if self.opmode == "cbc":
            # Iterate rounds loops for each text block:
            for i in range(self.tsize):

                self.core.__init__(self.cipherkey, self.plaintext[i])
                self.core.exp_key = self.exp_key

                if i == 0:
                    for j in range(16):
                        self.core.text[j] = self.iv[j] ^ self.core.text[j]
                else:
                    for j in range(16):
                        self.core.text[j] = hex2list(output)[j] ^ self.core.text[j]

                self.core.encript(verbose=self.verbosity >= 2)

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
              opmode="cbc",
              iv=key,
              verbosity=1)

    aes.encript()
