import binascii

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sm4_l(b):
    return b ^ left_rotate(b, 2) ^ left_rotate(b, 10) ^ left_rotate(b, 18) ^ left_rotate(b, 24)

def sm4_l_prime(b):
    return b ^ left_rotate(b, 13) ^ left_rotate(b, 23)

# Custom SBOX from binary
SBOX_HEX = "d690e9fecce13db716b614c228fb2c052b679a762abe04c3aa441326498606999c4250f491ef987a33540b43edcfac62e4b31ca9c908e89580df94fa758f3fa64707a7fcf37317ba83593c19e6854fa8686b81b27164da8bf8eb0f4b70569d351e240e5e6358d1a225227c3b01217887d40046579fd327524c3602e7a0c4c89eeabf8ad240c738b5a3f7f2cef96115a1e0ae5da49b341a55ad933230f58cb1e31df6e22e8266ca60c02923ab0d534e6fd5db39b831110c5acb3e0a45e594775b8d6d484110bd09c14a890d6e97a11d160ad9886a96d16b32023546067d65498cf03e2d7a15ff058e01843c3a3853877b0b2b7e0ff669a85ab54c1b397f088d1c"
SBOX = [int(SBOX_HEX[i:i+2], 16) for i in range(0, len(SBOX_HEX), 2)]

FK = [0xa3b1bac6, 0x56aa3313, 0x671c8797, 0xb742ff7e]
CK = [
    0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
    0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
    0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
    0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
    0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
    0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
    0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
    0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279
]

def sm4_t(val, is_key=False):
    b = [
        SBOX[(val >> 24) & 0xFF],
        SBOX[(val >> 16) & 0xFF],
        SBOX[(val >> 8) & 0xFF],
        SBOX[val & 0xFF]
    ]
    val = (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3]
    if is_key:
        return sm4_l_prime(val)
    return sm4_l(val)

def expand_key(key):
    mk = [
        int.from_bytes(key[0:4], "big"),
        int.from_bytes(key[4:8], "big"),
        int.from_bytes(key[8:12], "big"),
        int.from_bytes(key[12:16], "big")
    ]
    k = [mk[i] ^ FK[i] for i in range(4)]
    rk = []
    for i in range(32):
        k_val = k[i] ^ sm4_t(k[i+1] ^ k[i+2] ^ k[i+3] ^ CK[i], True)
        k.append(k_val)
        rk.append(k_val)
    return rk

def decrypt_block(rk, block):
    x = [
        int.from_bytes(block[0:4], "big"),
        int.from_bytes(block[4:8], "big"),
        int.from_bytes(block[8:12], "big"),
        int.from_bytes(block[12:16], "big")
    ]
    for i in range(32):
        x_val = x[i] ^ sm4_t(x[i+1] ^ x[i+2] ^ x[i+3] ^ rk[31-i])
        x.append(x_val)
    res = b"".join([x[35-i].to_bytes(4, "big") for i in range(4)])
    return res

key = binascii.unhexlify("3011aa21232beb7504432bfa90d32779")
rk = expand_key(key)
cipher_text = binascii.unhexlify("49b351855f211b85bd012f80ce8ed5b3")
plain = decrypt_block(rk, cipher_text)
print(f"Decrypted: {plain}")
