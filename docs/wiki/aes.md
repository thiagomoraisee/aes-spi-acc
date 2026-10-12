# Advanced Encryption Standard (AES/FIPS-197)

## Overview & Mathematical Foundations

The Advanced Encryption Standard (AES) is a symmetric block cipher structured around a substitution-permutation network (SPN). Unlike its predecessor DES, AES operates on a fixed block size of 128 bits (represented as a $4 \times 4$ matrix of bytes called the State) and supports key lengths of 128, 192, or 256 bits, corresponding to 10, 12, or 14 transformation rounds respectively.All algebraic operations in AES are performed within the finite field $\text{GF}(2^8)$, where multiplication is modulo the irreducible polynomial:

$$m(x) = x^8 + x^4 + x^3 + x + 1$$

## Core Transformation Stages

Each standard round of AES consists of four distinct byte-oriented transformations:

### SubBytes (Non-linear Substitution)

A byte-by-byte substitution using a pre-calculated S-box based on the multiplicative inverse in $\text{GF}(2^8)$ followed by an affine transformation. This provides cryptographic confusion.

### ShiftRows (Linear Diffusion)

Cyclic shifting of the rows of the State matrix to the left:

    - Row 0: Unshifted (offset 0);
    - Row 1: Shifted by 1 byte.
    - Row 2: Shifted by 2 bytes.
    - Row 3: Shifted by 3 bytes.

### MixColumns (Column-wise Mixing):
Each column of the State is multiplied modulo $x^4 + 1$ with a fixed polynomial $c(x) = {03}x^3 + {01}x^2 + {01}x + {02}$. This mixes the bytes within each column, providing diffusion. (Note: Omitted in the final round).

### AddRoundKey (Key Mixing):
The round key is combined with the State via a simple bitwise XOR operation.

## Key Expansion Schedule

The Key Expansion algorithm takes the initial cipher key and expands it into a schedule of round keys. For a 128-bit key, it generates 44 32-bit words ($W[0]$ through $W[43]$):

    - Words in positions multiple of 4 undergo RotWord (cyclic byte shift), SubWord (S-box substitution), and an XOR with a round constant ($\text{Rcon}[i]$) before being XORed with the word four positions prior.
    - Intermediate words are derived via simple XOR chaining: $W[i] = W[i-1] \oplus W[i-4]$.
