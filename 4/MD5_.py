from hashlib import md5

def encrypt_md5(msg):
    new_md5 = md5()
    new_md5.update(msg.encode(encoding='utf-8'))
    return new_md5.hexdigest()

if __name__ == '__main__':
    print(encrypt_md5('Welcme to the 90s'))