#!/usr/bin/python
import sys
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
host = "10.0.0.210"
def main():
    sport = 0
    port = 8000
    count = 0
    while  (count < 7):
        count = count + 1
        print count
        print sport
        print port
        sock = socket.create_connection((host, port), 2, ('', sport))
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.bind(('', sport))
        #print host
        
        #sock.connect((host, port))
        
        #try:
                #Send some junk data to the open port to see if it response
            #sock.send("Goodbye\r\n")
                #Wait for a response then shove it in a variable
        banner = sock.recv(1024)
                #Print the banner to the screen
        print '[+]' + str(banner)
        newip = banner.split(',')
                    
        port = int(newip[0])
        sport = int(newip[1])
        sock.close
        #except:
            #pass


if __name__ == "__main__":
    main()
