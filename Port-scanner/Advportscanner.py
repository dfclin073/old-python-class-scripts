#!/usr/bin/python
#Import in the sys library for command line arguments
import sys
#Import in the socket library
import socket
#Create new socket object named "sock" using AF_INET (IPv4) and SOCK.STREAM (TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Set response timeout to 1 second for sock object
sock.settimeout(2)

def main():

    if len(sys.argv) == 1:

        print "No hosts were specified, scanning default"
        #for x in 
        hosts = ["24.214.136.175"]

    else:
        hosts = sys.argv[1:]

    for host in hosts:
        scan_host(host)

def scan_host(host):

    print "Scanning host %s:" % host

    #Define the start of the range of ports to scan
    start_port = 1190

    #Define the end of the range of ports to scan
    end_port = 1195

    #Loop over all ports from start to end and stuff into variable "port"
    for port in range(start_port, end_port):

        #Attempt to run the following block of code
        try:
            #Run our test port function
            result = test_port(host, port)
            #Report is the port is open
            print "Port %i is open!" % port

            try:
                #Send some junk data to the open port to see if it response

                sock.send("Goodbye\r\n")

                #Wait for a response then shove it in a variable

                banner = sock.recv(1024)

                #Print the banner the screen

                print '[+]' + str(banner)
                print len(banner)
                banner = banner.strip()
                print len(banner)
                
                #Known banner list
                banner_list = ["SSH-2.0-OpenSSH_7.2", "FTP", "Telnet", "HTTP"]
                
                #Checking against the list
                for x in (banner_list):
                   if banner==(banner_list):
                      print "Jackpot"
                   
            #Look specifically for an error on the banner grabbing

            except Exception, e:

                print '[-] Unable to grab banner: ' + str(e)

        #Run this block of code if the "try:" block of code causes a crash

        except:

            #Do nothing at all, like a boss

            pass


def test_port(host, port):

    #Attempt a 3 way handshake to (host, port), return the success value

    return sock.connect((host, port))


if __name__ == "__main__":

    main()
