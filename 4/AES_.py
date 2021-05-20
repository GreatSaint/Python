from Cryptodome.Cipher import AES
import binascii

# 这是密钥
key = b'abcdefghabcdefgh'   # key需为8字节长度.
# 需要加密的数据
text = 'zhusimaji'     # 被加密的数据需要为8字节的倍数.
text = text + (16 - (len(text) % 16)) * '='
print(text)
# 需要去生成一个AES对象
aes = AES.new(key, AES.MODE_ECB)
encrypto_text = aes.encrypt(text.encode())
encryptResult = binascii.b2a_hex(encrypto_text)
print(encryptResult)

encrypto_text = binascii.a2b_hex(encryptResult)
decryptResult = aes.decrypt(encrypto_text)
print(decryptResult)