#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket
#Fill in start
#using localhost 127.0.0.1
serverPort = 8888
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
#Fill in end 

while True:
    #Establish the connection
    print 'Ready to serve...'
    #Fill in start
    connectionSocket, addr = serverSocket.accept()
    #Fill in end
    try:
        #Fill in start
        message = connectionSocket.recv(1024)
        #Fill in end
        filename = message.split()[1]
        f = open(filename[1:])
        #Fill in start
        outputdata = f.read()
        #Fill in end
        
        #Send one HTTP header line into socket
        #Fill in start 
        #http okay
        connectionSocket.send('HTTP/1.1 200 OK\n\n')
        #http response format ^^
        #connectionSocket.send(outputdata)
        #Fill in end 
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        #Fill in start
        connectionSocket.send('HTTP/1.1 404 Not Found\n\n')
        #http response format ^^
        #Fill in end 
        
        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end
serverSocket.close()
