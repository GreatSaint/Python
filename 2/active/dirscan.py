import requests


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Geocko/20100101 Firefox/60.0'}
url = input('url: ')
txt = input('php.txt: ')

url_list =[]
if txt == '':
    txt = 'php.txt'
try:
    with open(txt, 'r') as f:
        for a in f:
            a = a.replace('\n', '')
            url_list.append(a)
except Exception as e:
    print(e)


for li in url_list:
    conn = 'http://' + url + '/' + li
    try:
        response = requests.get(conn, headers=headers)
        print('%s----------------%s' % (conn, response))
    except Exception as e:
        print('%s----------------%s' % (conn, e.code))