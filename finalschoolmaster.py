#10.81.68.126
#10.81.68.124
import os
import socket
import pygame
import pyautogui
import time



host = socket.gethostbyname(socket.gethostname())
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = host, port
s.bind(ADDR)

def screenshare():
    pygame.init()
   
    w, h = pyautogui.size()
   
    win = pygame.display.set_mode((w,h))
   
    def redraw(win, sc):
        win.blit(sc,(0,0))
        pygame.display.update()
    #main loop
    fps = 60
    Clock = pygame.time.Clock()
    def main():
        run = True
        value = 0
        sc = pygame.image.load(r"C:\Users\sigur\Music\connecting_image.png")
        while run:
            s.settimeout(9)
            Clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            try:
                conn.send("send size".encode())
                size = conn.recv(4048).decode()
                print("got size")
                conn.send(size.encode())
                screenshot = conn.recv(int(size))
                print("got image")
                img = open("image.png", "wb")
                img.write(screenshot)
                img.close()
                print("saved image")
            except:
                value +=1
                print("except")
            if value == 100:
                print("connection timed out")
                run = False


            try:
                sc = pygame.image.load(r"C:\Users\sigur\image.png")
            except:
                print("image failed to load")
            print("ja")
       
            redraw(win, sc)
               
        pygame.quit()
       
    main()
   

print("\n Server is currently running @", host)

print("\n Waiting for incomming connections")

s.listen(1)
conn, addr = s.accept()

valid_command = ["make file", "read file", "write file", "stream",]

print("\n", addr, "Has connected to the server succsessfully")

while 1:
    
    command = input("\n Command>>>")
    if command == "make file":
        user_command = input("\n file name>>>")
        conn.send(user_command.encode())
       
    if command == "read file":

        user_command = input("\n file name>>>" )
        conn.send(user_command.encode())
   
    if command == "write file":
        user_command = input("\n file name>>>")
        conn.send(user_command.encode())
       
    if command == "send file":
        conn.send(command.encode())
        file = conn.recv(4128)

    if command == "stream":
        conn.send(command.encode())
        user_command = conn.recv(1024)
        user_command = user_command.decode()
        if user_command == "stream":
            directory = os.getcwd()
            screenshare()
           
           
           

    elif command == "bat":
        conn.send((command.encode()))
        run = True

        while run:
            user_command = input("Bash Command>>>")
            if user_command == "kill" :
                run = False
            conn.send(user_command.encode())
    else:
        print("\n This is not a valid command")
