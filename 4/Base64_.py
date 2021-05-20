
import base64

base64_code = 'aGVsbG8geHhl'
string = base64.b64decode(base64_code).decode('utf-8')
print(string)

string = 'hello xss'
base64_code = base64.b64encode(string.encode('utf-8'))
print(base64_code)