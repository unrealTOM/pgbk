#!/usr/bin/python

import subprocess, sys
from urllib.parse import unquote

with subprocess.Popen("http-server -p 8241", shell=True, stdout=subprocess.PIPE) as r:
	while True:
		try:
			s = r.stdout.readline()
			if s == '' and r.poll() != None:
				break
		except:
			print("interrupted")
			r.kill()
			break;

		ls = '\033[0m'
		es = ''
		if b'Error' in s:
			es = '\033[91m'

		st = s.find(b'GET ')
		ed = s.find(b'\" ')
		if st >= 0 and ed >= 0:
			u = s[st : ed]
			print(es + s[0 : st].decode('utf8', 'replace') + unquote(u.decode('latin1')) + s[ed:].decode('latin1') + ls, end='', flush=True)
		else:
			print(es + s.decode('utf8', 'replace') + ls, end='', flush=True)

