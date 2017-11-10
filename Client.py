import socket
import tkinter as tk

# Create Socket and connect to server
thisSocket = socket.socket()
thisSocket.connect(("127.0.0.1",5001))

def receiveMessage(i):
    ''' Receives multiple messages from server if needed, until server
        sends EndOfMessage and displays the recieved messages on the user
        interface'''
    
    if i == 0:
        global username
        username = "User"
    
    message = thisSocket.recv(1024).decode()
    print(message)
    while (message != "EndOfMessage"):
        if username == "User" and "YOURNAMEWILLBE" in message:
            nameholder = message.split()[1:]
            username = ''.join(nameholder)
            username = username.title()
            thisSocket.send("Received".encode())
            message = thisSocket.recv(1024).decode()
            continue
        chatHistory.configure(state="normal")
        thisSocket.send("Received".encode())
        chatHistory.insert(tk.END, "Jeff: " + message + "\n")
        chatHistory.see(tk.END)
        chatHistory.configure(state="disabled") #prevents user from editing the chat history
        message = thisSocket.recv(1024).decode()

def sendMessage(event=None):
    '''Waits for the user to enter a messasge in the text entry box in the
       interface and then takes this input from the user and feeds it to the
       chatbot/server, allowing it to respond to the input appropriately.'''

    sMessage = ""
    while sMessage is None or sMessage == "": #loops through until user actually says something
        sMessage = userInput.get() #input from user, needs to come from interface

    thisSocket.send(sMessage.encode())
    chatHistory.configure(state="normal")
    chatHistory.insert(tk.END, username + ": " + sMessage + "\n")
    chatHistory.see(tk.END)
    chatHistory.configure(state="disabled")
    userInput.delete(0, tk.END)
    receiveMessage(i)

i = 0

#Creates the main window for the interface
window = tk.Tk()
window.title("Chatbot Jeff")
window.geometry("600x600")
window.configure(background="cornflower blue")

lblTitle = tk.Label(window, text="CHATBOT JEFF", bg="cornflower blue", font=("Helvetica", 24))
lblTitle.pack()

lbl = tk.Label(window, text="\nChatHistory", bg="cornflower blue", font=("Helvetica", 16))
lbl.pack()

chatHistory = tk.Text(window)
chatHistory.pack(padx=30)
chatHistory.configure(state="disabled")

userInput = tk.Entry(window)
userInput.pack(pady=15)
userInput.bind("<Return>", sendMessage)

sendBtn = tk.Button(window, command=sendMessage)
sendBtn.pack(side="left", pady=15)

receiveMessage(i) #Receives the initial message from the chatbot
i = i + 1

tk.mainloop() #Runs the GUI
    
sendMessage() #Allows the user to respond

#Close Socket
thisSocket.close()
print("Conversation between user and ChatBot Ended")

    


